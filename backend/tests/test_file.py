import pytest
from app import create_app, db
from app.models import User
import random
import string
from werkzeug.security import generate_password_hash 
import os
from unittest.mock import patch
from unittest import mock
from flask_jwt_extended.view_decorators import verify_jwt_in_request
import io
from app.blueprints.file.file_routes import File, db

@pytest.fixture
def client():
    app = create_app()
    os.environ["env"] = "testing" 
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def test_user():
    email = random_email_generator()
    password = random_word_generator()
    hashed_password = generate_password_hash(password) 
    user = User(email=email, name=random_word_generator(), password=hashed_password)
    
    db.session.add(user)
    db.session.commit()
    
    return {
        "id": user.id,
        "email": email,
        "password": password,
    }
        

def random_word_generator():
    return ''.join(random.choices(string.ascii_letters, k=8))


def random_email_generator():
    username = random_word_generator()
    domain = random.choice(['gmail', 'outlook', 'icloud', 'hotmail', 'yahoo', 'aol'])
    return f'{username}@{domain}.com'


@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", new=lambda*args, **kwargs: None)
@patch("app.blueprints.file.file_routes.get_jwt_identity", return_value=1)
def test_get_files(mock_get_jwt_identity, client, test_user):
    response = client.get("file/get-files")

    assert response.status_code == 200


@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", new=lambda*args, **kwargs: None)
@patch("app.blueprints.file.file_routes.get_jwt_identity", return_value=1)
def test_encrypt_txt(mock_jwt_identity, client, test_user):
    with open("utils/test_file.txt", "rb") as test_file:
        file_data = {
            "file": (test_file, "test_file.txt")
        }
        response = client.post("/file/encrypt", data=file_data, content_type="multipart/form-data")
        body = response.get_json()

        assert response.status_code == 200
        assert body["message"] == "File encrypted successfully"

        encrypted_file = db.session.get(File, body["file_id"])
        assert encrypted_file is not None
        assert encrypted_file.user_id == 1
        assert encrypted_file.name == "test_file.txt"
        assert encrypted_file.id == body["file_id"]


@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", new=lambda*args, **kwargs: None)
@patch("app.blueprints.file.file_routes.get_jwt_identity", return_value=1)
def test_encrypt_pdf(mock_jwt_identity, client, test_user):
    with open("utils/test_file.pdf", "rb") as test_file:
        file_data = {
            "file": (test_file, "test_file.pdf")
        }
        response = client.post("/file/encrypt", data=file_data, content_type="multipart/form-data")
        body = response.get_json()

        assert response.status_code == 200
        assert body["message"] == "File encrypted successfully"

        encrypted_file = db.session.get(File, body["file_id"])
        assert encrypted_file is not None
        assert encrypted_file.user_id == 1
        assert encrypted_file.name == "test_file.pdf"
        assert encrypted_file.id == body["file_id"]


@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", new=lambda*args, **kwargs: None)
@patch("app.blueprints.file.file_routes.get_jwt_identity", return_value=1)
def test_encrypt_csv(mock_jwt_identity, client, test_user):
    with open("utils/test_file.csv", "rb") as test_file:
        file_data = {
            "file": (test_file, "test_file.csv")
        }
        response = client.post("/file/encrypt", data=file_data, content_type="multipart/form-data")
        body = response.get_json()

        assert response.status_code == 200
        assert body["message"] == "File encrypted successfully"

        encrypted_file = db.session.get(File, body["file_id"])
        assert encrypted_file is not None
        assert encrypted_file.user_id == 1
        assert encrypted_file.name == "test_file.csv"
        assert encrypted_file.id == body["file_id"]
        assert encrypted_file.user_id == test_user["id"]


def test_unauthorized(client):
    request = client.post('/file/encrypt')

    assert request.status_code == 401
    assert request.get_json()["msg"] == "Missing cookie \"access_token_cookie\""