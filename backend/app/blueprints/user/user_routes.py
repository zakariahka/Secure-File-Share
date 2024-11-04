from . import user_bp
from flask import jsonify, request
from app.models import User
from email_validator import validate_email, EmailNotValidError
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, create_app
import psycopg2 
from datetime import timedelta, datetime
import jwt

def create_jwt_token(email):
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=60) 
    }
    token = jwt.encode(payload, create_app.config["JWT_SECRET"], algorithm="HS256")
    return token


@user_bp.route('/test', methods=['GET'])
def test():
    first_user = User.query.first()

    if first_user:
        return jsonify({"message": "Successfully connected to postgres!"}), 200

@user_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
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

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email or password is missing"}), 400
    
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User doesn't exist"}), 401
    elif not check_password_hash(user.password, password):
        return jsonify({"error", "Password is incorrect"})
    
