import os
import pytest
import django
from django.contrib.auth import get_user_model
from terminals.models import Terminal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "truck2terminal_api.settings")
django.setup()

User = get_user_model()


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "password2": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "1234567890",
    }


@pytest.fixture
def create_user(user_data):
    user_data_copy = user_data.copy()
    user_data_copy.pop("password2")
    user = User.objects.create_user(**user_data_copy)
    return user


@pytest.fixture
def terminal_data():
    return {
        "name": "Main Terminal",
        "location": "City Center",
        "capacity": 100,
    }


@pytest.fixture
def create_terminal(terminal_data):
    terminal = Terminal.objects.create(**terminal_data)
    return terminal
