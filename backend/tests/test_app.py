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

def random_email_generator():
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(5, 10)))
    domain = ''.join(random.choices(string.ascii_letters, k=random.randint(5,10)))

    top_level_domain = ['.com', '.org', '.gov', '.edu', '.dev']
    tld = random.choice(top_level_domain)

    return f'{username}@{domain}.{tld}'

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

