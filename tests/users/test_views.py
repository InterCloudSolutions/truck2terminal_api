import pytest
from rest_framework import status
from rest_framework.test import APIClient

from users.models import CustomUser


@pytest.mark.django_db
class TestRegistrationView:
    client = APIClient()
    register_url = "/api/users/register/"

    def test_successful_registration(self, user_data):
        """Test successful user registration."""
        response = self.client.post(self.register_url, user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert CustomUser.objects.count() == 1
        assert CustomUser.objects.get().username == user_data["username"]

    def test_password_mismatch(self, user_data):
        """Test registration with mismatched passwords."""
        user_data["password2"] = "differentpass"
        response = self.client.post(self.register_url, user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data

    def test_missing_required_fields(self, user_data):
        """Test registration with missing required fields."""
        del user_data["first_name"]
        response = self.client.post(self.register_url, user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "first_name" in response.data

    def test_duplicate_username(self, user_data, create_user):
        """Test registration with duplicate username."""
        response = self.client.post(self.register_url, user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data
