from . import file_bp
from flask import jsonify, request, make_response, current_app
from app import db
from flask_jwt_extended import jwt_required, decode_token
import jwt
from app.models import File, User
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import base64
import zlib

@file_bp.route("/encrypt", methods=["POST"])
@jwt_required()
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

    # compressing the file, although it doesnt make much of a difference :(
    compressed_file = zlib.compress(file_content, level=5)
    
    cipher = AES.new(aes_key, AES.MODE_CTR)
    encrypted_content = cipher.encrypt(compressed_file)
    
    hmac = HMAC.new(hmac_key, digestmod=SHA256)
    hmac.update(cipher.nonce + encrypted_content).digest()
    tag = hmac.digest()
    
    try:
        decoded_token = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        user_id = decoded_token["id"]
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    encrypted_file = File(name=file.filename, encrypted_file=encrypted_content, nonce=cipher.nonce, hmac_tag=tag, user_id=user_id)

    try:
        db.session.add(encrypted_file)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

    return jsonify({
        "message": "File encrypted successfully",
        "file_id": encrypted_file.id,
        "regular_file": base64.b64encode(file_content).decode("utf-8"),
        "compressed_file": base64.b64encode(compressed_file).decode("utf-8"),
        "user_id": user_id
    }), 200

@file_bp.route("/get-files", methods=["GET"])
@jwt_required()
def get_files():
    try:
        files = db.session.query(File).all()
        files_list = [file.to_dict() for file in files]
    except Exception as e:
        return jsonify({"error": "Database query failed" , "details": str(e)}), 500
    
    return files_list, 200