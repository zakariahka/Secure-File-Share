import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.commit()

def test_connection_route(client):
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

@pytest.mark.parametrize("invalid_email", [
    "invalidemail.com",         # Missing '@'
    "invalidemail@",            # Missing domain
    "@domain.com",              # Missing local part
    "invalid@@domain.com",      # Extra '@'
    "invalidemail@domain",      # No TLD
    "invalid email@domain.com", # Whitespace
    "invalid()email@domain.com" # Special characters without quotes
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
