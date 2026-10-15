import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import ProjectEntityFactory, TaskEntityFactory


@pytest.mark.usefixtures("dynamodb")
class TestDeleteProjectEndpoint:
    def test_owner_deletes(self, client: TestClient, tokens: Tokens) -> None:
        project = ProjectEntityFactory.create()
        headers = tokens.of("alice")

        assert client.delete(f"/api/v1/projects/{project.id}", headers=headers).status_code == 204
        assert client.get(f"/api/v1/projects/{project.id}", headers=headers).status_code == 404

    def test_other_user_is_forbidden(self, client: TestClient, tokens: Tokens) -> None:
        project = ProjectEntityFactory.create()

        assert client.delete(f"/api/v1/projects/{project.id}", headers=tokens.of("bob")).status_code == 403

    def test_project_with_tasks_is_409(self, client: TestClient, tokens: Tokens) -> None:
        task = TaskEntityFactory.create()

        assert client.delete(f"/api/v1/projects/{task.project_id}", headers=tokens.of("alice")).status_code == 409
