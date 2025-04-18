from flask import Flask, send_from_directory
from config import ProductionConfig, DevelopmentConfig, TestConfig
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os
from flask_jwt_extended import JWTManager


db = SQLAlchemy()

def create_app():
    HERE = os.path.abspath(os.path.dirname(__file__))  
    BUILD_DIR = os.path.abspath(os.path.join(HERE, '..', '..', 'frontend', 'build'))

    env = os.getenv("env", "development")
    if env == "production":
        app = Flask(
            __name__,
            static_folder=os.path.join(BUILD_DIR, 'static'),
            static_url_path='/static'
        )
        app.config.from_object(ProductionConfig)
    elif env == "development":
        app = Flask(__name__)
        app.config.from_object(DevelopmentConfig)
        CORS(app, supports_credentials=True, origins=app.config["CLIENT_URL"])
    elif env == "testing":
        app = Flask(__name__)
        app.config.from_object(TestConfig)


    db.init_app(app)
    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    with app.app_context():
        from . import models

    from .blueprints.user import user_bp
    from .blueprints.file import file_bp
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(file_bp, url_prefix="/file")
    if env == "production":
        from .blueprints.frontend import frontend_bp
        app.register_blueprint(frontend_bp)

    return app