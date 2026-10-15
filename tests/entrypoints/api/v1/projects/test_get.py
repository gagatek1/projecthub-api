import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import ProjectEntityFactory


@pytest.mark.usefixtures("dynamodb")
class TestGetProjectEndpoint:
    def test_owner_gets_project(self, client: TestClient, tokens: Tokens) -> None:
        project = ProjectEntityFactory.create()

        response = client.get(f"/api/v1/projects/{project.id}", headers=tokens.of("alice"))

        assert response.status_code == 200
        assert response.json()["id"] == project.id

    def test_other_user_is_forbidden(self, client: TestClient, tokens: Tokens) -> None:
        project = ProjectEntityFactory.create()

        assert client.get(f"/api/v1/projects/{project.id}", headers=tokens.of("bob")).status_code == 403

    def test_missing_is_404_and_invalid_id_is_422(self, client: TestClient, tokens: Tokens) -> None:
        headers = tokens.of("alice")

        assert client.get("/api/v1/projects/missing", headers=headers).status_code == 404
        assert client.get("/api/v1/projects/a%20b", headers=headers).status_code == 422
