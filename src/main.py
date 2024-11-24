import time
from src.config import DB_URL, CHECK_INTERVAL, X_ACCOUNT
from src.twitter_client import TwitterClient
from src.text_processing import extract_scorecard, extract_official_results, finish_by_round_one, extract_fighter_names, extract_result_names, is_first_round_finish
from src.discord_client import send_to_discord
from sqlalchemy.orm import Session
from src.database.database import SessionLocal
from src.database.models import Fighter, Scorecard, Fight
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text
from sqlalchemy import and_
from src.utils import is_new_fight_update

processed_fights = set()
formatted_fights = []
result_tweets = []
processed_tweet_ids = set()

def get_or_create_fighter(db: Session, name: str) -> Fighter:
    fighter = db.query(Fighter).filter(Fighter.full_name == name).first()
    fighter = Fighter(full_name=name)
    db.add(fighter)
    db.flush()
    return fighter

def process_fight_tweets(result_tweets, is_single_tweet, tweet, single_scorecard_media, db, twitter_client):
    new_tweets_found = False
    formatted_fights = []
    
    if len(result_tweets) > 1:
        new_tweets_found = True
        scorecard_tweet = next((t for t in result_tweets if extract_scorecard(t.text)), None)
        result_tweet = next((t for t in result_tweets if extract_official_results(t.text)), None)
        
        if scorecard_tweet and result_tweet:
            process_scorecard_result(scorecard_tweet, result_tweet, db, twitter_client, formatted_fights)
            
    elif is_single_tweet:
        new_tweets_found = True
        process_single_tweet(tweet, single_scorecard_media, db, formatted_fights)
        
    elif is_first_round_finish(tweet.text):
        new_tweets_found = True
        formatted_fights.append({
            "result": tweet.text,
            "scorecard_media": "Scorecard not available"
        })
    else:
        return False, []

    return new_tweets_found, formatted_fights

def process_scorecard_result(scorecard_tweet, result_tweet, db, twitter_client, formatted_fights):
    tweet_detail = twitter_client.get_tweet_detail(scorecard_tweet.id)
    scorecard_media = []
    if hasattr(tweet_detail, 'media'):
        for media in tweet_detail.media:
            if hasattr(media, 'media_url_https'):
                scorecard_media.append({'preview_image_url': media.media_url_https})
    
    fighter_names = extract_fighter_names(scorecard_tweet.text)
    if fighter_names:
        fighter1_name, fighter2_name = fighter_names
        save_fight_to_db(fighter1_name, fighter2_name, scorecard_media, db)
        
    formatted_fights.append({
        "result": extract_official_results(result_tweet.text),
        "scorecard_media": scorecard_media
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

def ufc_fight_message(twitter_client):
    global result_tweets
    global formatted_fights
    global processed_tweet_ids
    single_scorecard_media = []
    MAX_NUMBER_OF_TWEETS = 3
    new_tweets_found = False
    is_single_tweet = False
    db = SessionLocal()
    try:
        collected_tweets = []
        async for _, tweet_batch in twitter_client.iter_tweets("UFCNews"):
            for i, tweet in enumerate(tweet_batch, 1):
                print(f"Tweet: {tweet.text[:200]}...")
                print(f"Tweet ID: {tweet.id}")

                tweet_text = tweet.text if hasattr(tweet, 'text') else ""
                tweet_id = tweet.id if hasattr(tweet, 'id') else None
                
                if tweet_id and str(tweet_id) in processed_tweet_ids:
                    return "No new fight updates at this time."

                if len(result_tweets) == 2: 
                    result_tweets = []
                    
                collected_tweets.append(tweet)
                scorecard_line = extract_scorecard(tweet_text)
                official_result = extract_official_results(tweet_text)
                
                if (scorecard_line or official_result):           
                    if official_result and 'Complete Scorecards' in tweet_text:
                        is_single_tweet = True
                        single_scorecard_media = []
                        single_tweet_detail = twitter_client.get_tweet_detail(tweet.id)
                        if hasattr(single_tweet_detail, 'media'):
                            for media in single_tweet_detail.media:
                                if hasattr(media, 'media_url_https'):
                                    single_scorecard_media.append({'preview_image_url': media.media_url_https})
                                    break

                    if not is_single_tweet:
                        if (scorecard_line or official_result and not is_first_round_finish(tweet.text)): 
                            result_tweets.append(tweet)
                    
                    new_tweets_found, formatted_fights = process_fight_tweets(
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
                            print('processed_tweet_ids', processed_tweet_ids)

                    if new_tweets_found and formatted_fights:
                        print('new_tweets_found detected')
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
    print(f"Attempting to connect to database with URL: {DB_URL}")
    engine = create_engine(DB_URL)
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"Database connection successful. Result: {result.fetchone()}")
    except Exception as e:
        print(f"Database connection failed. Error: {str(e)}")

    twitter_client = await TwitterClient().initialize()
    
    while True:
        try:
            message = await ufc_fight_message(twitter_client)
            print(f"\nReceived message: {message}")
            if is_new_fight_update(message) and message not in processed_fights:
                await send_to_discord(message)
                processed_fights.add(message)
                if len(processed_fights) > 1000:
                    processed_fights.clear()
            else:
                print('No new updates to process')
                
        except Exception as e:
            print(f"An error occurred in main loop: {str(e)}")
            await asyncio.sleep(30)
            continue
            
        await asyncio.sleep(180)

if __name__ == "__main__":
    asyncio.run(main())