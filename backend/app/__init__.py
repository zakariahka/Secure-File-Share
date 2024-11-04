from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from . import models

    from .blueprints.user import user_routes as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')
    
    return app