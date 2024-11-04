from . import user_bp
from flask import jsonify
from app.models import User
from email_validator import validate_email, EmailNotValidError
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import psycopg2 

@user_bp.route('/test', methods=['GET'])
def test():
    first_user = User.query.first()

    if first_user:
        return jsonify({"message": "Successfully connected to postgres!"}), 200

@user_bp.route('/signup', methods=['POST'])
def signup():
    data = requests.get_json()
    if not data:
        return jsonify({"message": "Request body must be a JSON"}), 400
    
    email = data.get("email")
    name = data.get("name")
    password = data.get("password")
    confirmed_password = data.get("confirmed_password")

    required_fields = ["email", "name", "password", "confirmed_password"]
    all(data.get(field) for field in required_fields)

    if not all(data.get(field) for field in required_fields):
        return jsonify({"error": "One or more of the required feilds are missing"}), 401
    
    if password != confirmed_password:
        return jsonify({"error": "Passwords don't match"}), 402
    
    if len(password) < 8:
        return jsonify({"error": "Password length is too small"}), 403
    
    try:
        email_info = validate_email(email, check_deliverability=True)
        email = email_info.normalized
    except EmailNotValidError as e:
        return jsonify({"error": str(e)}), 404
    
    hashed_password = generate_password_hash(password)
    user = User(email, name, hashed_password)

    try:
        db.session.add(user)
        db.session.commit()
    except psycopg2.IntegrityError:
        db.session.rollback()
        return jsonify({"error": "User already exists"})
    
    return jsonify({"messages": "User has successfully signed up", "user": user}), 200