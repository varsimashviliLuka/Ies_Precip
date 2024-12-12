import pytest
from flask import Flask, url_for
from unittest.mock import patch

# Fixtures for test setup
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
@patch('flask_jwt_extended.get_jwt_identity')
def admin_user(mock_get_jwt_identity):
    mock_get_jwt_identity.return_value = 'admin-uuid'
    return {'uuid': 'admin-uuid', 'role': 'admin'}

@pytest.fixture
@patch('src.models.User.query.filter_by')
def mock_admin_permission(mock_filter_by, admin_user):
    class MockAdmin:
        def check_permission(self):
            return True

    mock_filter_by.return_value.first.return_value = MockAdmin()
    return mock_filter_by

# Test cases for Registration API
def test_registration_success(client, mock_admin_permission):
    with patch('src.models.User.query.filter_by') as mock_user_query, \
         patch('src.models.Role.query.filter_by') as mock_role_query:
        
        # Mock data
        mock_user_query.return_value.first.return_value = None
        mock_role_query.return_value.first.return_value = type('Role', (), {'id': 1})()
        
        data = {
            "email": "test@example.com",
            "password": "password123",
            "passwordRepeat": "password123",
            "role_name": "user"
        }
        
        response = client.post(url_for('registrationapi'), json=data)
        
        assert response.status_code == 200
        assert response.get_json()["message"] == "მომხმარებელი წარმატებით დარეგისტრირდა"

# Test cases for Authorization API
def test_login_success(client):
    with patch('src.models.User.query.filter_by') as mock_user_query:
        # Mock data
        mock_user = type('User', (), {
            'uuid': 'user-uuid',
            'check_password': lambda x: x == 'password123'
        })()
        mock_user_query.return_value.first.return_value = mock_user
        
        data = {
            "email": "test@example.com",
            "password": "password123"
        }

        response = client.post(url_for('authorizationapi'), json=data)
        
        assert response.status_code == 200
        response_data = response.get_json()
        assert "access_token" in response_data
        assert "refresh_token" in response_data

# Test cases for Token Refresh API
def test_refresh_token(client):
    with patch('flask_jwt_extended.get_jwt_identity') as mock_get_identity:
        mock_get_identity.return_value = 'user-uuid'
        
        response = client.post(url_for('accesstokenrefreshapi'))
        
        assert response.status_code == 200
        assert "access_token" in response.get_json()
