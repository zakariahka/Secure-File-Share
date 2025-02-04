from . import file_bp
from flask import jsonify, request, make_response, current_app, send_file
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import base64
import io
import logging
from app.models import File, User
from Crypto.Cipher import AES
import mimetypes

@file_bp.route("/get-files", methods=["GET"])
@jwt_required()
def get_files():
    user_id = get_jwt_identity()

    try:
        files = User.get_all_file_ids(user_id)
    except Exception as e:
        logging.error("Database query failed: %s", str(e))
        return jsonify({"error": "Database query failed"}), 500
    
    return jsonify(files), 200


@file_bp.route("/encrypt", methods=["POST"])
@jwt_required()
def encrypt():
    aes_key = base64.b64decode(current_app.config["AES_KEY"])

    user_id = get_jwt_identity()

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]

    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0)

    MAX_SIZE = 5 * 1024 * 1024   #5 MB

    if file_size > MAX_SIZE:
        return jsonify({"error": "File is too large. Maximum size is 5 MB"}), 400

    if file.filename == "":
        return jsonify({"error": "Did not include file"}), 400
    
    file_content = file.read()
    
    try:
        cipher = AES.new(aes_key, AES.MODE_EAX)
        encrypted_content, auth_tag = cipher.encrypt_and_digest(file_content)
    except Exception as e:
        logging.error("Encryption failed: %s", str(e))
        return jsonify({"error": "Encryption failed"}), 500

    encrypted_file = File(
        name=file.filename,
        encrypted_content=encrypted_content,
        nonce=cipher.nonce,
        auth_tag=auth_tag,
        user_id=user_id
    )

    try:
        db.session.add(encrypted_file)
        db.session.commit()
    except Exception as e:
        logging.error("Database commit failed: %s", str(e))
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

    return jsonify({
        "message": "File encrypted successfully",
        "file_id": encrypted_file.id,
        "user_id": user_id
    }), 200


@file_bp.route("/decrypt", methods=["POST"])
@jwt_required()
def decrypt():
    aes_key = base64.b64decode(current_app.config["AES_KEY"])

    user_id = get_jwt_identity()
    
    body = request.get_json()
    if not body:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    file_id = body.get("file_id")
    if not file_id:
        return jsonify({"error": "Missing 'file_id' in request body"}), 400

    file = User.get_file_by_id(user_id, file_id)
    if not file:
        return jsonify({"error": "File not found"}), 404

    try:
        cipher = AES.new(aes_key, AES.MODE_EAX, nonce=file.nonce)
        decrypted_content = cipher.decrypt(file.encrypted_content)
        cipher.verify(file.auth_tag)
    except (ValueError, KeyError) as e:
        logging.error("Decryption failed: %s", str(e))
        return jsonify({"error": "Key incorrect or message corrupted"}), 400

    try:
        decrypted_text = decrypted_content.decode('utf-8')
        return jsonify({
            "message": "File decrypted successfully",
            "file_content": decrypted_text
        }), 200
    except UnicodeDecodeError:
        decrypted_stream = io.BytesIO(decrypted_content)
        mime_type, _ = mimetypes.guess_type(file.name)
        if mime_type is None:
            mime_type = 'application/octet-stream'

        return send_file(
            decrypted_stream,
            as_attachment=True,
            download_name=file.name,
            mimetype=mime_type
        )