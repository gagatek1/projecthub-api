import pytest
from fastapi.testclient import TestClient

PASSWORD = "Passw0rd!x"


@pytest.mark.usefixtures("cognito")
class TestSignupEndpoint:
    def test_creates_account(self, client: TestClient) -> None:
        response = client.post("/api/v1/auth/signup", json={"email": "c@x.io", "password": PASSWORD})

        assert response.status_code == 201
        assert response.json()["sub"]

    def test_duplicate_is_409(self, client: TestClient) -> None:
        client.post("/api/v1/auth/signup", json={"email": "c@x.io", "password": PASSWORD})

        assert client.post("/api/v1/auth/signup", json={"email": "c@x.io", "password": PASSWORD}).status_code == 409

    def test_short_password_is_422(self, client: TestClient) -> None:
        assert client.post("/api/v1/auth/signup", json={"email": "c@x.io", "password": "short"}).status_code == 422
