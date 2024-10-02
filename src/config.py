import os
from dotenv import load_dotenv

load_dotenv()  

DISCORD_WEBHOOK_URL = os.getenv("WEBHOOK_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
CHECK_INTERVAL = 900 

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")


DB_URL = os.getenv("DATABASE_URL")
print(f"Database URL: {DB_URL}") 
DB_PORT = 5432  
