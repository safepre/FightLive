import os
from dotenv import load_dotenv

load_dotenv()  

DISCORD_WEBHOOK_URL = os.getenv("WEBHOOK_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
CHECK_INTERVAL = 900 

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")

db_host = os.getenv("DB_HOST", "localhost")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{db_host}:5432/{DB_NAME}"
DB_PORT = 5432  
