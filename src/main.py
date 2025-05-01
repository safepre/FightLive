import time
from src.config import DB_URL, CHECK_INTERVAL, X_ACCOUNT
from src.twitter_client import TwitterClient
from src.text_processing import extract_scorecard, extract_official_results, finish_by_round_one,extract_first_names, extract_scorecard_names, extract_result_names, is_first_round_finish,extract_result_fighters
from src.discord_client import send_to_discord
from sqlalchemy.orm import Session
from src.database.database import SessionLocal
from src.database.models import Fighter, Scorecard, Fight
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text
from sqlalchemy import and_
from src.utils import is_new_fight_update
import asyncio

processed_fights = set()
formatted_fights = []
result_tweets = {
    'scorecard_id': None,
    'scorecard': None,  
    'result': None,   
    'has_scorecard': False,  
    'has_result': False,     
}
processed_tweet_ids = set()

def get_or_create_fighter(db: Session, name: str) -> Fighter:
    fighter = db.query(Fighter).filter(Fighter.full_name == name).first()
    if not fighter:
        fighter = Fighter(full_name=name)
        db.add(fighter)
        db.flush()
    return fighter

async def process_fight_tweets(result_tweets, is_single_tweet, tweet, single_scorecard_media, db, twitter_client):
    new_tweets_found = False
    formatted_fights = []
    
    if result_tweets['has_scorecard'] and result_tweets['has_result']:
        new_tweets_found = True
        scorecard_tweet = result_tweets['scorecard']
        scorecard_first_name = extract_first_names(scorecard_tweet)
        result_tweet = result_tweets['result']
        result_first_name = extract_first_names(result_tweet)
        scorecard_id = result_tweets['scorecard_id']
        if scorecard_first_name == result_first_name:
            await process_scorecard_result(scorecard_id, scorecard_tweet, result_tweet, db, twitter_client, formatted_fights)
            
    elif is_single_tweet:
        new_tweets_found = True
        process_single_tweet(tweet, single_scorecard_media, db, formatted_fights)
        
    elif is_first_round_finish(tweet.text):
        new_tweets_found = True
        result_tweet = result_tweets['result']
        result_tweets['result'] = None
        result_tweets['has_result'] = False

        formatted_fights.append({
            "result": result_tweet,
            "scorecard_media": "Scorecard not available"
        })
    else:
        return False, []

    return new_tweets_found, formatted_fights

async def process_scorecard_result(scorecard_id, scorecard_tweet, result_tweet, db, twitter_client, formatted_fights):
    tweet_detail = await twitter_client.tweet_detail(scorecard_id)
    scorecard_media = []
    if hasattr(tweet_detail, 'media'):
        for media in tweet_detail.media:
            if hasattr(media, 'media_url_https'):
                scorecard_media.append({'preview_image_url': media.media_url_https})
    
    fighter_names_scorecard = extract_scorecard_names(scorecard_tweet)
    if fighter_names_scorecard:
        fighter1_name_scorecard, fighter2_name_scorecard = fighter_names_scorecard
        scorecard_link = scorecard_media[0]['preview_image_url'] if scorecard_media else None

        if not (check_scorecard_in_db(scorecard_link, db)):
            save_fight_to_db(fighter1_name_scorecard, fighter2_name_scorecard, scorecard_media, db)
            formatted_fights.append({
                "result": extract_official_results(result_tweet),
                "scorecard_media": scorecard_media
            })
        else:
            formatted_fights.append({
                "result": extract_official_results(result_tweet),
                "scorecard_media": "Scorecard not available"
            })

def process_single_tweet(tweet, single_scorecard_media, db, formatted_fights):
    fighter_names = extract_result_names(tweet.text)
    if fighter_names:
        fighter1_name, fighter2_name = fighter_names
        save_fight_to_db(fighter1_name, fighter2_name, single_scorecard_media, db)
        
    formatted_fights.append({
        "result": extract_official_results(tweet.text),
        "scorecard_media": single_scorecard_media
    })

def check_scorecard_in_db(scorecard_link, db):
    """
    Check if scorecard exists in the database.
    Returns True if scorecard exists, False otherwise.
    """
    try:
        scorecard_exists = db.query(Scorecard).filter(Scorecard.link == scorecard_link).first() is not None

        return scorecard_exists

    except Exception as e:
        return False

def save_fight_to_db(fighter1_name, fighter2_name, scorecard_media, db):
    try:
        fighter1 = get_or_create_fighter(db, fighter1_name)
        fighter2 = get_or_create_fighter(db, fighter2_name)

        scorecard_link = scorecard_media[0]['preview_image_url'] if scorecard_media else None
        existing_scorecard = db.query(Scorecard).filter(Scorecard.link == scorecard_link).first()
        
        if existing_scorecard:
            scorecard = existing_scorecard
        else:
            scorecard = Scorecard(link=scorecard_link)
            db.add(scorecard)
            db.flush()

        existing_fight = db.query(Fight).filter(
            and_(
                Fight.fighter_id == fighter1.id,
                Fight.opponent_id == fighter2.id,
                Fight.scorecard_id == scorecard.id
            )
        ).first()

        if not existing_fight:
            fight = Fight(fighter_id=fighter1.id, opponent_id=fighter2.id, scorecard_id=scorecard.id)
            db.add(fight)

        db.commit()
    except (SQLAlchemyError, Exception) as e:
        db.rollback()

async def ufc_fight_message(twitter_client):
    global result_tweets
    global formatted_fights
    global processed_tweet_ids
    single_scorecard_media = []
    MAX_NUMBER_OF_TWEETS = 4
    new_tweets_found = False
    is_single_tweet = False
    db = SessionLocal()
    
    try:
        collected_tweets = []
        async for _, tweet_batch in twitter_client.iter_tweets("UFCNews"):
            for i, tweet in enumerate(tweet_batch, 1):
                if len(collected_tweets) >= MAX_NUMBER_OF_TWEETS:
                    break

                tweet_text = tweet.text if hasattr(tweet, 'text') else ""
                tweet_id = tweet.id if hasattr(tweet, 'id') else None
                
                if tweet_id and str(tweet_id) in processed_tweet_ids:
                    return "No new fight updates at this time."
                 
                if result_tweets['has_scorecard'] and result_tweets['has_result']:    
                    result_tweets = {
                        'scorecard': None,
                        'result': None,
                        'has_scorecard': False,
                        'has_result': False,
                        'scorecard_id': None
                    }

                    
                collected_tweets.append(tweet)


                scorecard_line = extract_scorecard(tweet_text)
                official_result = extract_official_results(tweet_text)

                if (scorecard_line or official_result):           
                    if official_result and 'Complete Scorecards' in tweet_text:
                        is_single_tweet = True
                        single_scorecard_media = []
                        single_tweet_detail = await twitter_client.tweet_detail(tweet.id)
                        if hasattr(single_tweet_detail, 'media'):
                            for media in single_tweet_detail.media:
                                if hasattr(media, 'media_url_https'):
                                    single_scorecard_media.append({'preview_image_url': media.media_url_https})
                                    break

                    if not is_single_tweet:
                        if (official_result or is_first_round_finish(tweet.text)): 
                            result_tweets['result'] = tweet.text
                            result_tweets['has_result'] = True
                        else:
                            result_tweets['scorecard'] = tweet.text
                            result_tweets['scorecard_id'] = tweet.id
                            result_tweets['has_scorecard'] = True
                    
                    new_tweets_found, formatted_fights = await process_fight_tweets(
                        result_tweets,
                        is_single_tweet,
                        tweet,
                        single_scorecard_media,
                        db,
                        twitter_client
                    )

                    for t in collected_tweets:
                        if hasattr(t, 'id'):
                            processed_tweet_ids.add(str(t.id))

                    if new_tweets_found and formatted_fights:
                        message = ""
                        for fight in formatted_fights:
                            result = fight.get('result', 'N/A')
                            message += f"Result: {result}\n"
                            if isinstance(fight.get('scorecard_media'), list):
                                for media in fight['scorecard_media']:
                                    message += f"Scorecard Image: {media.get('preview_image_url', 'N/A')}\n"
                            elif fight.get('scorecard_media') == "Scorecard not available" and is_first_round_finish(result):
                                return message
                            elif fight.get('scorecard_media') == "Scorecard not available":
                                message += "Three Minutes Until Next Update\n"
                        
                        return message
            break
        return "No new fight updates at this time."

    finally:
        db.close()

async def main():
    engine = create_engine(DB_URL)
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
    except Exception as e:
        print(f"Database connection failed. Error: {str(e)}")

    twitter_client = await TwitterClient().initialize()
    
    while True:
        try:
            message = await ufc_fight_message(twitter_client)
            print(f"\nReceived message: {message}")
            if is_new_fight_update(message) and message not in processed_fights:
                send_to_discord(message)
                processed_fights.add(message)
                if len(processed_fights) > 1000:
                    processed_fights.clear()
                
        except Exception as e:
            await asyncio.sleep(30)
            continue
            
        await asyncio.sleep(180)

if __name__ == "__main__":
    asyncio.run(main())