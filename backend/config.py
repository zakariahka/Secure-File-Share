import os
from dotenv import load_dotenv

load_dotenv()

class DevelopmentConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    CLIENT_URL = os.getenv("CLIENT_URL")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    PORT = int(os.getenv("DEV_PORT", 5001))
    AES_KEY = os.getenv("AES_KEY")
    HMAC_KEY = os.getenv("HMAC_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_COOKIE_NAME = "token"
    JWT_COOKIE_CSRF_PROTECT = False

class ProductionConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    PORT = int(os.getenv("PROD_PORT", 5001))
    AES_KEY = os.getenv("AES_KEY")
    HMAC_KEY = os.getenv("HMAC_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_COOKIE_NAME =  "token"
    JWT_COOKIE_CSRF_PROTECT = False
    
class TestConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    PORT = int(os.getenv("TEST_PORT", 5001))
    AES_KEY = os.getenv("AES_KEY")
    HMAC_KEY = os.getenv("HMAC_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_CSRF_PROTECT = False