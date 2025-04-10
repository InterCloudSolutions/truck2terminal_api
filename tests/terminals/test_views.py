import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from terminals.models import Terminal


@pytest.mark.django_db
class TestTerminalViews:
    client = APIClient()

    def test_create_terminal(self, terminal_data):
        url = reverse("terminals:terminal-list")
        response = self.client.post(url, terminal_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "Main Terminal"
        assert Terminal.objects.count() == 1

    def test_list_terminals(self, create_terminal):
        url = reverse("terminals:terminal-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Main Terminal"

    def test_retrieve_terminal(self, create_terminal):
        url = reverse(
            "terminals:terminal-detail", kwargs={"slug": create_terminal.slug}
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Main Terminal"
        assert response.data["capacity"] == 100

    def test_update_terminal(self, create_terminal):
        url = reverse(
            "terminals:terminal-detail", kwargs={"slug": create_terminal.slug}
        )
        data = {"name": "Updated Terminal", "capacity": 150}
        response = self.client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        updated_terminal = Terminal.objects.get()
        assert updated_terminal.name == "Updated Terminal"
        assert updated_terminal.capacity == 150

    def test_delete_terminal(self, create_terminal):
        url = reverse(
            "terminals:terminal-detail", kwargs={"slug": create_terminal.slug}
        )
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Terminal.objects.count() == 0
