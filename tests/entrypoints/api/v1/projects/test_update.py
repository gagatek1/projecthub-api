import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import ProjectEntityFactory

PROJECT = {"name": "Artemis", "description": "Moon", "max_users": 3}


@pytest.mark.usefixtures("dynamodb")
class TestUpdateProjectEndpoint:
    def test_owner_updates(self, client: TestClient, tokens: Tokens) -> None:
        project = ProjectEntityFactory.create()

        response = client.put(f"/api/v1/projects/{project.id}", json=PROJECT, headers=tokens.of("alice"))

        assert response.status_code == 200
        assert response.json()["name"] == "Artemis"

    def test_other_user_is_forbidden(self, client: TestClient, tokens: Tokens) -> None:
        project = ProjectEntityFactory.create()

        assert client.put(f"/api/v1/projects/{project.id}", json=PROJECT, headers=tokens.of("bob")).status_code == 403

    def test_missing_is_404(self, client: TestClient, tokens: Tokens) -> None:
        assert client.put("/api/v1/projects/missing", json=PROJECT, headers=tokens.of("alice")).status_code == 404
