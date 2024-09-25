import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("WEBHOOK_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
CHECK_INTERVAL = 600
