import pytest
from app import create_app
from app.models import User

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_connection_route(client):
    with client.application.app_context():
        user = User.query.first()
        assert user is not None, "No user found in the database"
        user_dict = user.to_dict()
        assert "id" in user_dict
        assert "email" in user_dict
        assert "name" in user_dict 
