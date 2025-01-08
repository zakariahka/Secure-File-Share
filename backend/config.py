import os
from dotenv import load_dotenv

load_dotenv()

class DevelopmentConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.getenv("JWT_SECRET")
    CLIENT_URL = os.getenv("CLIENT_URL")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    PORT = os.getenv("DEV_PORT")
    AES_KEY=os.getenv("AES_KEY")
    HMAC_KEY=os.getenv("HMAC_KEY")

class ProductionConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.getenv("JWT_SECRET")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    PORT = os.getenv("PROD_PORT")
    AES_KEY=os.getenv("AES_KEY")
    HMAC_KEY=os.getenv("HMAC_KEY")

class TestConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.getenv("JWT_SECRET")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    PORT = os.getenv("TEST_PORT")
    AES_KEY=os.getenv("AES_KEY")
    HMAC_KEY=os.getenv("HMAC_KEY")