from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True, origins=app.config["CLIENT_URL"])
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from . import models

    from .blueprints.user import user_bp

    app.register_blueprint(user_bp, url_prefix="/user")

    return app