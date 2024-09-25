import time
from config import CHECK_INTERVAL
from twitter_client import TwitterClient
from text_processing import finish_by_round_one, extract_scorecard
from discord_client import send_to_discord

def ufc_fight_message(twitter_client):
    global processed_tweets
    user_tweets = twitter_client.get_tweets("UFCNews")
    formatted_fights = []
    message = ""
    new_tweets_found = False
    for i, tweet in enumerate(user_tweets):
        scorecard_line = extract_scorecard(tweet.text)
        if scorecard_line and i + 1 < len(user_tweets) and tweet.id not in processed_tweets:
            new_tweets_found = True
            tweet_detail = twitter_client.get_tweet_detail(tweet.id)
            prev_tweet = tweet.text if 'Official Result & Scorecard' not in tweet.text else user_tweets[i + 1]
            scorecard_media = [{
                'preview_image_url': pic.media_url_https
            } for pic in tweet_detail.media]
            
            formatted_fights.append({
                "live_detail": prev_tweet.text,
                "scorecard_media": scorecard_media
            })
            processed_tweets.add(tweet.id) 
        else:
            isRoundOneFinish = finish_by_round_one(tweet.text)
            if isRoundOneFinish:
                formatted_fights.append({
                    "live_detail": tweet.text,
                    "scorecard_media": []
                })
                processed_tweets.add(tweet.id)
          
    if new_tweets_found:
        for fight in formatted_fights:
            message += f"{fight['live_detail']}\n"
            for media in fight['scorecard_media']:
                message += f"Scorecard: {media['preview_image_url']}\n"
        return message
    else:
        return "No new fight updates at this time."

def main():
    processed_tweets = set()
    twitter_client = TwitterClient()
    while True:
        message = ufc_fight_message(twitter_client)
        if message != "No new fight updates at this time.":
            send_to_discord(message)
        else:
            print(message)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

