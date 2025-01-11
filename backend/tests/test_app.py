import pytest
from app import create_app, db
from app.models import User
import random
import string
from werkzeug.security import generate_password_hash 
from config import TestConfig
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import os

@pytest.fixture
def client():
    app = create_app()
    os.environ["env"] = "testing" 
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

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


def test_signup(client):
    password = random_word_generator()

    user = {
        "email": random_email_generator(),
        "name": random_word_generator(),
        "password": password,
        "confirmed_password": password
    }

    response = client.post('/user/signup', json=user)

    assert response.status_code == 200
    assert response.get_json()["message"] == "User has successfully signed up"
    assert response.get_json()["user"]["email"] == user["email"]


@pytest.mark.parametrize("invalid_email", [
    # different types of invalid emails
    # TODO: make dynamic parameters
    "invalidemail.com",         
    "invalidemail@",            
    "@domain.com",              
    "invalid@@domain.com",      
    "invalidemail@domain",      
    "invalid email@domain.com",
    "invalid()email@domain.com"
])
def test_signup_with_invalid_email(client, invalid_email):
    response = client.post('/user/signup', json={
        "email": invalid_email,
        "name": "Test User",
        "password": "password123",
        "confirmed_password": "password123"
    })
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid email address"


def test_signup_with_existing_email(client, test_user):
    response = client.post('/user/signup', json={
        "email": test_user["email"],
        "name": "Test User",
        "password": "password123",
        "confirmed_password": "password123"
    })

    assert response.status_code == 400
    assert response.get_json()["error"] == "User already exists"


def test_signup_with_mismatch_password(client):
    password = random_word_generator()
    confirmed_password = random_word_generator()

    user = {
        "email": random_email_generator(),
        "name": random_word_generator(),
        "password": password,
        "confirmed_password": confirmed_password
    }

    response = client.post('user/signup', json=user)

    assert response.status_code == 400
    assert response.get_json()["error"] == "Passwords don't match"


def test_signup_with_missing_field(client):
    password = random_word_generator()

    user = {
        "email": random_email_generator(),
        "name": random_word_generator(),
        "password": password,
        "confirmed_password": password
    }

    random_field = random.choice(list(user.keys()))
    user[random_field] = None

    response = client.post('/user/signup', json=user)

    assert response.status_code == 400
    assert response.get_json()["error"] == "One or more of the required feilds are missing"


def test_login(client, test_user):
    response = client.post('/user/login', json=test_user)

    assert response.status_code == 200
    assert response.get_json()["message"] == "User has successfully logged in"
    assert response.get_json()["user"]["email"] == test_user["email"]


def test_login_with_incorrect_email_or_password(client, test_user):
    field = random.choice(["password", "email"])
    test_user[field] = random_word_generator()

    response = client.post('/user/login', json=test_user)

    assert response.status_code == 400
    assert response.get_json()["error"] == "Email or Password is incorrect"


def test_login_with_missing_email_or_password(client, test_user):
    field = random.choice(["email", "password"])
    test_user[field] = None

    response = client.post('/user/login', json=test_user)

    assert response.status_code == 400
    assert response.get_json()["error"] == "Email or Password is missing"
