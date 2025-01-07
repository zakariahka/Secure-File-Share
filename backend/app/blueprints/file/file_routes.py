from . import file_bp
from flask import jsonify, request, make_response, current_app
from cryptography.fernet import Fernet
import os

@file_bp.route("/encrypt", methods=["POST"])
def encrypt():
    key = current_app.config["ENCRYPTION_KEY"]

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"] 

    if file.filename == "":
        return jsonify({"error": "Did not include file"}), 400
    
    file_content = file.read()
    
    fernet = Fernet(key)
    encrypted_file = fernet.encrypt(file_content)

    return jsonify({
        "message": "File encrypted successfully",
        "encrypted_content": encrypted_file.decode("utf-8")
    }), 200