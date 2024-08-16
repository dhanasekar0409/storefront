from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework import status as status
import pytest


@pytest.mark.django_Db
class TestCreateCollection:
    def test_if_user_is_anonymous_user_returns_401(self):
        # Arrange

        # Act
        client = APIClient()
        client.post("/store/collections/", {"title": "a"})

        # Assert
        assert Response.status_code == status.HTTP_401_UNAUTHORIZED
