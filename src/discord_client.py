import re
from discord_webhook import DiscordWebhook, DiscordEmbed
from config import DISCORD_WEBHOOK_URL
from text_processing import extract_official_results

def send_to_discord(message):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)
    image_urls = re.findall(r'https?://\S+\.jpg', message)
    results = extract_official_results(message)
    cleaned_message = "\n\n".join(results)
    if cleaned_message == "":
        return "No new fight updates at this time."
    embed = DiscordEmbed(title="Fight Live Update", description=cleaned_message, color="03b2f8")
    
    for url in image_urls:
        embed.set_image(url=url)

    webhook.add_embed(embed)
    webhook.execute()
