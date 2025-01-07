# backend/app/__init__.py

from flask import Flask, send_from_directory
from config import ProductionConfig, DevelopmentConfig, TestConfig
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os

db = SQLAlchemy()

def create_app(config_object=None):
    HERE = os.path.abspath(os.path.dirname(__file__))  
    BUILD_DIR = os.path.abspath(os.path.join(HERE, '..', '..', 'frontend', 'build'))
    

    if config_object is not None:
        app = Flask(__name__)
        app.config.from_object(config_object)
    else:
        env = os.getenv("env", "development")
        if env == "production":
            app = Flask(
                __name__,
                static_folder=os.path.join(BUILD_DIR, 'static'),
                static_url_path='/static'
            )
            app.config.from_object(ProductionConfig)
        else:
            app = Flask(__name__)
            app.config.from_object(DevelopmentConfig)
            CORS(app, supports_credentials=True, origins=app.config["CLIENT_URL"])

    db.init_app(app)
    migrate = Migrate(app, db)

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