from . import file_bp
from flask import jsonify, request, make_response, current_app
from cryptography.fernet import Fernet
import os
from app import db
from flask_jwt_extended import jwt_required, decode_token
import jwt
from app.models import File, User

@file_bp.route("/encrypt", methods=["POST"])
def encrypt():
    key = current_app.config["ENCRYPTION_KEY"]

    token = request.cookies.get("token")
    if not token:
        return jsonify({"error": "Unauthorized"}), 401

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"] 

    if file.filename == "":
        return jsonify({"error": "Did not include file"}), 400
    
    file_content = file.read()
    
    fernet = Fernet(key)
    encrypted_content = fernet.encrypt(file_content)

    decoded_token = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
    user_id = decoded_token["id"]

    encrypted_file = File(name=file.filename, encrypted_file=encrypted_content, user_id=user_id)

    try:
        db.session.add(encrypted_file)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500


    return jsonify({
        "message": "File encrypted successfully",
        "file_id": encrypted_file.id,
        "encrypted_content": encrypted_content.decode("utf-8"),
        "user_id": user_id
    }), 200

@file_bp.route("/decrypt", methods=["GET"])
def decrypt():
    return None