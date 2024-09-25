from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import re
from tweety import Twitter
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
auth_token = os.getenv("TWITTER_AUTH_TOKEN")
CHECK_INTERVAL = 600 # Check every 10 minutes (600 seconds )
app = Twitter("session")
app.load_auth_token(auth_token)
formatted_fights = []
keyword = "Official Result:"

def extract_scorecard(tweet_text):
    pattern = r'^.*[Ss]corecard.*$'
    match = re.search(pattern, tweet_text, re.MULTILINE)
    if match:
        return match.group(0)
    return None

def dwcs_fight_message():
    global formatted_fights
    global processed_tweets
    user_tweets = list(app.get_tweets("UFCNews"))
    message = ""
    new_tweets_found = False
    
    for i, tweet in enumerate(user_tweets):
        if keyword.lower() in tweet.text.lower() and tweet.id not in processed_tweets:
            new_tweets_found = True
            tweet_detail = app.tweet_detail(tweet.id)
            scorecard_media = [{
                'preview_image_url': pic.media_url_https
            } for pic in tweet_detail.media]
            
            if scorecard_media:
                formatted_fights.append({
                    "live_detail": tweet.text,
                    "scorecard_media": scorecard_media
                })
            else:
                formatted_fights.append({
                    "live_detail": tweet.text,
                    "scorecard_media": []
                })
            processed_tweets.add(tweet.id) 
        else:
            continue
    if new_tweets_found:
        for fight in formatted_fights:
            message += f"{fight['live_detail']}\n"
            for media in fight['scorecard_media']:
                message += f"Scorecard: {media['preview_image_url']}\n\n"
        return message
    else:
        return "No new fight updates at this time."
def send_to_discord(message):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)
    
    image_urls = re.findall(r'https?://\S+\.jpg', message)

    # Extract and clean the official results
    results = extract_official_results(message)
    
    # Join the results into a single message
    print('results', results)
    cleaned_message = "\n\n".join(results)
    print('cleaned_message', cleaned_message)
    # Find all image URLs in the cleaned message
    print('image_urls', image_urls)
    
    embed = DiscordEmbed(title="Fight Live Update", description=cleaned_message, color="03b2f8")
    
    # Add images to the embed
    for url in image_urls:
        embed.set_image(url=url)

    webhook.add_embed(embed)
    webhook.execute()

def extract_official_results(text):
    # Pattern to match the official result statements
    pattern = r"Dana White's Contender Series Official Result:.*?(?=Dana White's Contender Series Official Result:|$)"
    
    # Find all matches
    matches = re.findall(pattern, text, re.DOTALL)
    
    # Clean up each match
    cleaned_matches = []
    for match in matches:
        # Remove URLs starting with https://t.co
        match = re.sub(r'https://t\.co\S+', '', match)
        # Remove "Week" and following words until the end of the line
        match = re.sub(r'Week.*?(?=\n|$)', '', match)
        # Remove "Scorecard:" and the following URL
        match = re.sub(r'Scorecard:\s*https?://\S+\.jpg', '', match)
        # Remove extra whitespace and newlines
        match = re.sub(r'\s+', ' ', match).strip()
        cleaned_matches.append(match)
    
    return cleaned_matches

def main():
    processed_tweets = set()
    while True:
        message = ufc_fight_message()
        if message != "No new fight updates at this time.":
            send_to_discord(message)
        else:
            print(message)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

