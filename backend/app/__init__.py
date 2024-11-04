from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .blueprints.user import user_routes as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')
    
    return app