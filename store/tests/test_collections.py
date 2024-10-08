from urllib import response
import pytest
from model_bakery import baker
from rest_framework import status
from store.models import Collection1, Product


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post("/store/collections/", collection)

    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_user_returns_401(
        self, authenticate, create_collection
    ):
        authenticate()
        response = create_collection({"title": "a"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_collection):
        authenticate()
        response = create_collection({"title": "a"})

        assert response.status_code == status.HTTP_403_FORBIDDEN  # type: ignore

    def test_data_is_invalid_returns_400(self, authenticate, create_collection):
        authenticate(is_staff=True)
        response = create_collection({"title": ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collecton_exists_returns_200(self, api_client):
        collection = baker.make(Collection1)

        response = api_client.get(f"/store/collections/{collection.id}/")  # type: ignore

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": collection.id,  # type: ignore
            "title": collection.title,
            "products_count": 0,
        }
