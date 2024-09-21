import time
import os
import re
from discord_webhook import DiscordWebhook, DiscordEmbed
from tweety import Twitter

DISCORD_WEBHOOK_URL = os.getenv("WEBHOOK_URL")
auth_token = os.getenv("AUTH_TOKEN")
CHECK_INTERVAL = 600 
app = Twitter("session")
app.load_auth_token(auth_token)
formatted_fights = []
processed_tweets = set() 

def extract_official_results(text):
    pattern = r"(#UFC\w+\s+Official\s+Result(?:\s+&\s+Scorecard)?.*?)(?=\n|$)"
    match = re.search(pattern, text)
    if match:
        return [match.group(1).strip()]
    return []
def extract_scorecard(tweet_text):
    pattern = r"(#UFC\d+\s+(?:Official\s+)?(?:Result|Scorecard).*?)(?=\n|$)"
    match = re.search(pattern, tweet_text, re.MULTILINE)
    if match:
        return match.group(0).strip()
    return None

def ufc_fight_message():
    global formatted_fights
    global processed_tweets
    user_tweets = list(app.get_tweets("UFCNews"))
    message = ""
    new_tweets_found = False
    
    for i, tweet in enumerate(user_tweets):
        scorecard_line = extract_scorecard(tweet.text)
        if scorecard_line and i + 1 < len(user_tweets) and tweet.id not in processed_tweets:
            new_tweets_found = True
            tweet_detail = app.tweet_detail(tweet.id)
            prev_tweet = user_tweets[i + 1]
            scorecard_media = [{
                'preview_image_url': pic.media_url_https
            } for pic in tweet_detail.media]
            
            if scorecard_media:
                formatted_fights.append({
                    "live_detail": prev_tweet.text,
                    "scorecard_media": scorecard_media
                })
            else:
                formatted_fights.append({
                    "live_detail": prev_tweet.text,
                    "scorecard_media": []
                })
            processed_tweets.add(tweet.id) 
        else:
            continue
    if new_tweets_found:
        for fight in formatted_fights:
            message += f"{fight['live_detail']}\n"
            for media in fight['scorecard_media']:
                message += f"Scorecard: {media['preview_image_url']}\n"
        return message
    else:
        return "No new fight updates at this time."

def send_to_discord(message):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)
    image_urls = re.findall(r'https?://\S+\.jpg', message)
    results = extract_official_results(message)
    cleaned_message = "\n\n".join(results)
    if cleaned_message == "":
        return
    embed = DiscordEmbed(title="Fight Live Update", description=cleaned_message, color="03b2f8")
    
    for url in image_urls:
        embed.set_image(url=url)

    webhook.add_embed(embed)
    webhook.execute()

def main():
    while True:
        message = ufc_fight_message()
        if message != "No new fight updates at this time.":
            send_to_discord(message)
        else:
            print(message)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
  main()

