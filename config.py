from dotenv import load_dotenv
from os import getenv
load_dotenv()  # Automatically loads .env file

# Config example
class Config:
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
    DEBUG = getenv('DEBUG') == 'True'
