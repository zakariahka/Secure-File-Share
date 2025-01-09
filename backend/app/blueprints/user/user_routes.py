from . import user_bp
from flask import jsonify, request, make_response, current_app
from app.models import User
from email_validator import validate_email, EmailNotValidError
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import psycopg2
from datetime import timedelta, datetime
import jwt
from sqlalchemy.exc import IntegrityError

def create_jwt_token(user):
    payload = {
        "sub": user.id,
        "email": user.email,
        "id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=60),
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")
    return token


@user_bp.route('/test', methods=['GET'])
def test():
    first_user = User.query.first()
    if first_user:
        return first_user.to_dict(), 200


@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be a JSON"}), 400

    email = data.get("email")
    name = data.get("name")
    password = data.get("password")
    confirmed_password = data.get("confirmed_password")

    required_fields = ["email", "name", "password", "confirmed_password"]

    if not all(data.get(field) for field in required_fields):
        return jsonify({"error": "One or more of the required feilds are missing"}), 400

    password = password.strip()
    confirmed_password = confirmed_password.strip()

    if password != confirmed_password:
        return jsonify({"error": "Passwords don't match"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password length is too small"}), 400

    try:
        email_info = validate_email(email)
        email = email_info.normalized
    except EmailNotValidError:
        return jsonify({"error": "Invalid email address"}), 400

    hashed_password = generate_password_hash(password)
    user = User(email, name, hashed_password)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "User already exists"}), 400

    return (
        jsonify(
            {"message": "User has successfully signed up", "user": user.to_dict()}
        ),
        200,
    )

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email or Password is missing"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Email or Password is incorrect"}), 400

    token = create_jwt_token(user)

    response = make_response(jsonify(message="User has successfully logged in", user=user.to_dict()))
    response.set_cookie(
        "token", token, httponly=True, samesite="Lax", secure=False, max_age=86400
    )

    return response, 200

@user_bp.route("/auth", methods=["GET"])
def check_auth():
    token = request.cookies.get("token")

    if not token:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        decoded_token = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        user_id = decoded_token.get("sub")

        if not user_id:
            return jsonify({"error": "Unauthorized - Missing 'sub' claim"}), 401

        user_data = User.query.filter_by(id=user_id).first()

        if not user_data:
            return jsonify({"error": "Unauthorized - User not found"}), 401
        
        user = {
            "name": user_data.name,
            "email": user_data.email
        }
        
        return jsonify({"message": "Authorized", "user": user}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Unauthorized - Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Unauthorized - Token expired"}), 401
    

@user_bp.route("/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"message": "User successfully logged out"}))
    response.set_cookie("token", "", httpOnly=True, max_age=0)
    return response, 200