from . import file_bp
from flask import jsonify, request, make_response, current_app
from cryptography.fernet import Fernet
import os
from app import db
from flask_jwt_extended import jwt_required, decode_token
import jwt
from app.models import File, User
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import base64

@file_bp.route("/encrypt", methods=["POST"])
def encrypt():
    aes_key = base64.b64decode(current_app.config["AES_KEY"])
    hmac_key = base64.b64decode(current_app.config["HMAC_KEY"])

    token = request.cookies.get("token")
    if not token:
        return jsonify({"error": "Unauthorized"}), 401

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"] 

    if file.filename == "":
        return jsonify({"error": "Did not include file"}), 400
    
    file_content = file.read()
    
    cipher = AES.new(aes_key, AES.MODE_CTR)
    encrypted_content = cipher.encrypt(file_content)

    hmac = HMAC.new(hmac_key, digestmod=SHA256)
    hmac.update(cipher.nonce + encrypted_content).digest()
    tag = hmac.digest()
    
    try:
        decoded_token = jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
        user_id = decoded_token["id"]
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    encrypted_file = File(name=file.filename, encrypted_file=encrypted_content, nonce=cipher.nonce, hmac_tag=tag, user_id=user_id)

    try:
        db.session.add(encrypted_file)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500


    return jsonify({
        "message": "File encrypted successfully",
        "file_id": encrypted_file.id,
        "encrypted_content": base64.b64encode(encrypted_content).decode("utf-8"),
        "user_id": user_id
    }), 200