import pytest
from app import create_app, db
from app.models import User
import random
import string

@pytest.fixture
def client():
    # TODO: rollback changes
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.commit()

def test_connection(client):
    """
    Test connecting to the db.
    """
    with client.application.app_context():
        user = User.query.first()
        assert user is not None, "No user found in the database"
        user_dict = user.to_dict()
        assert "id" in user_dict
        assert "email" in user_dict
        assert "name" in user_dict 

def random_word_generator():
    return ''.join(random.choices(string.ascii_letters, k=8))

def random_email_generator():
    username = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
    domain = random.choice(['gmail', 'outlook', 'hotmail', 'yahoo', 'icloud', 'aol'])
    return f'{username}@{domain}.com'

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

def test_mismatch_password(client):
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
def test_invalid_email_signup(client, invalid_email):
    """
    Test signup with invalid email addresses.
    """
    response = client.post('/user/signup', json={
        "email": invalid_email,
        "name": "Test User",
        "password": "password123",
        "confirmed_password": "password123"
    })
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid email address"

