import re
from discord_webhook import DiscordWebhook, DiscordEmbed
from src.config import DISCORD_WEBHOOK_URL
from src.text_processing import extract_official_results, extract_finish_method

def send_to_discord(message):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)
    finishes = extract_finish_method(message)

    image_urls = re.findall(r'https?://\S+\.jpg', message)
    if message == "":
        return "No new fight updates at this time."
    
    official_result = extract_official_results(message)
    
    embed = DiscordEmbed(title="Fight Live Update", description=official_result, color="03b2f8")
    if image_urls:
        embed.set_image(url=image_urls[0])

    webhook.add_embed(embed)
    webhook.execute()
