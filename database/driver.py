from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os


# GRAB SENSITIVE CREDENTIALS & DATABASE INFORMATION FROM THE ENVIRONMENT CONFIGURATION
MYSQL_USER: str = os.environ.get('MYSQL_USER')
MYSQL_PASS: str = os.environ.get('MYSQL_PASS')
MYSQL_ENDPOINT: str = os.environ.get('MYSQL_ENDPOINT')
MYSQL_PORT: int = int(os.environ.get('MYSQL_PORT'))

DATABASE_NAME: str = 'app'

def get_session() -> Session:
    SESSION = Session(
        create_engine(f"mysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_ENDPOINT}/{DATABASE_NAME}?charset=utf8mb4", encoding='utf8', convert_unicode=True))
    return SESSION
