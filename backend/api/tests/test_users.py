import pytest
from django.urls import reverse
from uuid import UUID

from api.models.user import User
from api.schemas.users import UserCreate, UserUpdate

@pytest.mark.django_db
class TestUserAPI:
    def test_create_user_success(self, client, test_user_data, auth_headers):
        """Test successful user creation"""
        # Use different username
        test_user_data = test_user_data.copy()
        test_user_data["username"] = "newuser"
        test_user_data["email"] = "new@example.com"

        response = client.post("/users", json=test_user_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == test_user_data["username"]
        assert data["email"] == test_user_data["email"]
        assert data["role"] == test_user_data["role"]
        assert data["full_name"] == test_user_data["full_name"]
        assert "password" not in data  # Ensure password is not returned

    def test_create_user_duplicate_username(self, client, test_user, test_user_data, auth_headers):
        """Test creating user with duplicate username"""
        response = client.post("/users", json=test_user_data, headers=auth_headers)
        assert response.status_code == 409
        assert "username" in response.json()["message"].lower()

    def test_create_user_invalid_data(self, client, auth_headers):
        """Test creating user with invalid data"""
        invalid_data = {
            "username": "test",  # Missing required fields
            "email": "invalid-email",  # Invalid email format
            "role": "invalid-role"  # Invalid role format
        }
        response = client.post("/users", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422

    def test_get_user_list(self, client, test_user, auth_headers):
        """Test getting user list"""
        response = client.get("/users", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["username"] == test_user.username

    def test_get_user_list_pagination(self, client, auth_headers):
        """Test user list pagination"""
        # Create multiple users
        for i in range(15):
            User.objects.create_user(
                username=f"user{i}",
                email=f"user{i}@example.com",
                password="testpass123",
                role="applicant",
                full_name=f"User {i}"
            )

        # Test first page
        response = client.get("/users?page=1&page_size=10", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 10
        assert data["count"] > 10

        # Test second page
        response = client.get("/users?page=2&page_size=10", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) > 0

    def test_get_user_detail(self, client, test_user, auth_headers):
        """Test getting user details"""
        response = client.get(f"/users/{test_user.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == test_user.username
        assert data["email"] == test_user.email

    def test_get_nonexistent_user(self, client, auth_headers):
        """Test getting non-existent user"""
        response = client.get(f"/users/{UUID('00000000-0000-0000-0000-000000000000')}", headers=auth_headers)
        assert response.status_code == 404

    def test_update_user_success(self, client, test_user, auth_headers):
        """Test successful user update"""
        update_data = {
            "full_name": "Updated Name",
            "email": "updated@example.com"
        }
        response = client.put(f"/users/{test_user.id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == update_data["full_name"]
        assert data["email"] == update_data["email"]

    def test_update_user_password(self, client, test_user, auth_headers):
        """Test updating user password"""
        update_data = {
            "password": "newpassword123"
        }
        response = client.put(f"/users/{test_user.id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200

        # Verify password has been updated
        user = User.objects.get(id=test_user.id)
        assert user.check_password("newpassword123")

    def test_update_nonexistent_user(self, client, auth_headers):
        """Test updating non-existent user"""
        response = client.put(
            f"/users/{UUID('00000000-0000-0000-0000-000000000000')}",
            json={"full_name": "New Name"},
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_delete_user_success(self, client, test_user, auth_headers):
        """Test successful user deletion"""
        response = client.delete(f"/users/{test_user.id}", headers=auth_headers)
        assert response.status_code == 204

        # Verify user is soft deleted
        user = User.objects.get(id=test_user.id)
        assert not user.is_active

    def test_delete_nonexistent_user(self, client, auth_headers):
        """Test deleting non-existent user"""
        response = client.delete(f"/users/{UUID('00000000-0000-0000-0000-000000000000')}", headers=auth_headers)
        assert response.status_code == 404