import os

from dotenv import load_dotenv

load_dotenv()


DB_HOSTNAME = os.getenv("DB_HOSTNAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
