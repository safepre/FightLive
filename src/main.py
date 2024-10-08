import time
from src.config import CHECK_INTERVAL, DB_URL, X_ACCOUNT
from src.twitter_client import TwitterClient
from src.text_processing import extract_scorecard, extract_official_results, finish_by_round_one, extract_fighter_names
from src.discord_client import send_to_discord
from sqlalchemy.orm import Session
from src.database.database import SessionLocal
from src.database.models import Fighter, Scorecard, Fight
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text
from sqlalchemy import and_

processed_tweets = set()

def ufc_fight_message(twitter_client):
    global processed_tweets
    user_tweets = twitter_client.get_tweets(X_ACCOUNT)
    formatted_fights = []
    message = ""
    new_tweets_found = False

    db = SessionLocal()
    print("Database session created")

    try:
        for i, tweet in enumerate(user_tweets):
            tweet_text = tweet.text if hasattr(tweet, 'text') else ""
            tweet_id = tweet.id if hasattr(tweet, 'id') else None

            if tweet_id in processed_tweets:
                continue

            scorecard_line = extract_scorecard(tweet_text)
            official_result = extract_official_results(tweet_text)

            if (scorecard_line or official_result):           
                result_tweets = [tweet]
                for j in range(1, 4):
                    if i + j < len(user_tweets):
                        next_tweet = user_tweets[i + j]
                        next_tweet_text = next_tweet.text if hasattr(next_tweet, 'text') else ""
                        if ((scorecard_line and extract_official_results(next_tweet_text)) or (official_result and extract_scorecard(next_tweet_text))) and not next_tweet.id in processed_tweets: 
                            result_tweets.append(next_tweet)
                            break
                
                if len(result_tweets) > 1:
                    
                    new_tweets_found = True
                    scorecard_tweet = next((t for t in result_tweets if extract_scorecard(t.text)), None)
                    result_tweet = next((t for t in result_tweets if extract_official_results(t.text)), None)
                    print('scorecard_tweet', scorecard_tweet.text)
                    print('result_tweet', result_tweet.text)
                    if scorecard_tweet and result_tweet:
                        print(f"Found scorecard and result tweet: {scorecard_tweet.text[:100]}...")
                        tweet_detail = twitter_client.get_tweet_detail(scorecard_tweet.id)
                        print('tweet_detail', tweet_detail)
                        scorecard_media = []
                        if hasattr(tweet_detail, 'media'):
                            for media in tweet_detail.media:
                                if hasattr(media, 'media_url_https'):
                                    scorecard_media.append({'preview_image_url': media.media_url_https})
                        
                        fighter_names = extract_fighter_names(scorecard_tweet.text) 
                        print(f"Extracted fighter names: {fighter_names}")
                        if fighter_names:
                            fighter1_name, fighter2_name = fighter_names
                            print(f"Extracted fighter names: {fighter1_name} vs {fighter2_name}")

                            try:
                                fighter1 = get_or_create_fighter(db, fighter1_name)
                                fighter2 = get_or_create_fighter(db, fighter2_name)

                                scorecard_link = scorecard_media[0]['preview_image_url'] if scorecard_media else None
                                existing_scorecard = db.query(Scorecard).filter(Scorecard.link == scorecard_link).first()
                                
                                if existing_scorecard:
                                    scorecard = existing_scorecard
                                    print(f"Existing scorecard found with link: {scorecard_link}")
                                else:
                                    scorecard = Scorecard(link=scorecard_link)
                                    db.add(scorecard)
                                    db.flush()
                                    print(f"New scorecard added with link: {scorecard_link}")

                                existing_fight = db.query(Fight).filter(
                                    and_(
                                        Fight.fighter_id == fighter1.id,
                                        Fight.opponent_id == fighter2.id,
                                        Fight.scorecard_id == scorecard.id
                                    )
                                ).first()

                                if existing_fight:
                                    print(f"Fight already exists: {fighter1.full_name} vs {fighter2.full_name}")
                                else:
                                    fight = Fight(fighter_id=fighter1.id, opponent_id=fighter2.id, scorecard_id=scorecard.id)
                                    db.add(fight)
                                    print(f"New fight added: {fighter1.full_name} vs {fighter2.full_name}")

                                db.commit()
                                print("Database changes committed")
                            except SQLAlchemyError as e:
                                db.rollback()
                                print(f"Database error: {str(e)}")
                                print("Database changes rolled back")
                            except Exception as e:
                                db.rollback()
                                print(f"Unexpected error: {str(e)}")
                                print("Database changes rolled back")

                        formatted_fights.append({
                            "result": extract_official_results(result_tweet.text),
                            "scorecard_media": scorecard_media
                        })
                        for t in result_tweets:
                            processed_tweets.add(t.id)
                else:
                    new_tweets_found = True
                    formatted_fights.append({
                        "result": tweet_text,
                        "scorecard_media": "Scorecard not available"
                    })
        if new_tweets_found:
            for fight in formatted_fights:
                message += f"Result: {fight.get('result', 'N/A')}\n"
                if isinstance(fight.get('scorecard_media'), list):
                    for media in fight['scorecard_media']:
                        message += f"Scorecard Image: {media.get('preview_image_url', 'N/A')}\n"
                elif fight.get('scorecard_media') == "Scorecard not available":
                    message += "No scorecard available\n"
                message += "\n"
            return message
        else:
            return "No new fight updates at this time."
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        db.close()
        print("Database session closed")

def get_or_create_fighter(db: Session, name: str) -> Fighter:
    fighter = db.query(Fighter).filter(Fighter.full_name == name).first()
    if fighter:
        print(f"Fighter found in database: {fighter.full_name}")
    else:
        fighter = Fighter(full_name=name)
        db.add(fighter)
        db.flush()
        print(f"New fighter added to database: {fighter.full_name}")
    return fighter

def main():
    print(f"Attempting to connect to database with URL: {DB_URL}")
    engine = create_engine(DB_URL)
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"Database connection successful. Result: {result.fetchone()}")
    except Exception as e:
        print(f"Database connection failed. Error: {str(e)}")

    twitter_client = TwitterClient()
    while True:
        try:
            message = ufc_fight_message(twitter_client)
            print(f"Generated message: {message}")  # Add this line for debugging

            if 'No scorecard available' in message and 'Round 1' not in message:
                time.sleep(300) #5 minutes
                message = ufc_fight_message(twitter_client)
                print("Sending message to Discord after 5 minutes")
                send_to_discord(message)
            elif message != "No new fight updates at this time.":
                print("Sending message to Discord")
                send_to_discord(message)
            else:
                print(message)
        except Exception as e:
            print(f"An error occurred in main loop: {str(e)}")
        time.sleep(CHECK_INTERVAL)
