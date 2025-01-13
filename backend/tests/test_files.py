import pytest
from app import create_app, db
from app.models import User
import random
import string
from werkzeug.security import generate_password_hash 
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