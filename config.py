import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DB_URL = os.getenv("DB_URL", "") #add your own harperdb cloud database url
    DB_USER = os.getenv("DB_USER", "") #add your own user for the harperdb cloud databse
    DB_PASSWORD = os.getenv("DB_PASSWORD", "") #add your own password for the harperdb cloud database
    DB_SCHEMA = os.getenv("DB_SCHEMA", "highlight_repo")
    DB_TABLE = os.getenv("DB_TABLE", "highlights")
    DB_TABLE_TODAY = os.getenv("DB_TABLE_TODAY", "highlight_today")

    # API
    API_KEYS = os.getenv("API_KEYS", "valid-key").split(",")
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")