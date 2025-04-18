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

@pytest.fixture
def client():
    app = create_app()
    os.environ["env"] = "testing" 
    with app.app_context():
        db.create_all()
        yield app.test_client()

def random_word_generator():
    return ''.join(random.choices(string.ascii_letters, k=8))

def random_email_generator():
    username = random_word_generator()
    domain = random.choice(['gmail', 'outlook', 'icloud', 'hotmail', 'yahoo', 'aol'])
    return f'{username}@{domain}.com'

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

def mock_jwt_required(f):
    return f

@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", new=lambda*args, **kwargs: None)
@patch('app.blueprints.file.file_routes.get_jwt_identity', return_value=1)
def test_get_files(mock_get_jwt_identity, client, test_user):
    response = client.get("file/get-files")
    
    assert response.status_code == 200


def test_unauthorized(client):
    request = client.post('/file/encrypt')

    assert request.status_code == 401
    assert request.get_json()["msg"] == "Missing cookie \"access_token_cookie\""