import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens

PROJECT = {"name": "Apollo", "description": "Moon", "max_users": 3}


@pytest.mark.usefixtures("dynamodb")
class TestCreateProjectEndpoint:
    def test_creates_project_owned_by_caller(self, client: TestClient, tokens: Tokens) -> None:
        response = client.post("/api/v1/projects", json=PROJECT, headers=tokens.of("alice"))

        assert response.status_code == 201
        assert response.json()["project_owner"] == "alice"

    @pytest.mark.parametrize(
        "body",
        [
            {**PROJECT, "id": "victim-project"},
            {**PROJECT, "project_owner": "someone"},
            {**PROJECT, "max_users": 0},
            {**PROJECT, "name": ""},
            {"name": "x"},
        ],
    )
    def test_rejects_invalid_body(self, client: TestClient, tokens: Tokens, body: dict[str, object]) -> None:
        assert client.post("/api/v1/projects", json=body, headers=tokens.of("alice")).status_code == 422
