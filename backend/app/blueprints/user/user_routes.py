from . import user_bp
from flask import Blueprint, jsonify
from app.models import User

@user_bp.route('/test', methods=['GET'])
def test():
    first_user = User.query.first()

    if first_user:
        return jsonify({"message": "successfully connected to postgres!"}), 200

@user_bp.route('/signup', methods=['POST'])
def signup():
    return