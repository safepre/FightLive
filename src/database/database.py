import sys
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import DB_URL 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Attempting to connect to database with URL: {DB_URL}")

try:
    engine = create_engine(DB_URL)
    logger.info("Database engine created successfully")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("SessionLocal created")
    Base = declarative_base()
    logger.info("Base created")
except Exception as e:
    logger.error(f"Error creating database connection: {str(e)}")
    raise
