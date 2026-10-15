import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import ProjectEntityFactory, TaskEntityFactory


@pytest.mark.usefixtures("dynamodb")
class TestGetTaskEndpoint:
    def test_owner_and_assignee_can_read(self, client: TestClient, tokens: Tokens) -> None:
        task = TaskEntityFactory.create(assigned_user="bob")
        url = f"/api/v1/projects/{task.project_id}/tasks/{task.id}"

        assert client.get(url, headers=tokens.of("alice")).json()["id"] == task.id
        assert client.get(url, headers=tokens.of("bob")).json()["id"] == task.id

    def test_outsider_is_forbidden(self, client: TestClient, tokens: Tokens) -> None:
        task = TaskEntityFactory.create()

        assert (
            client.get(f"/api/v1/projects/{task.project_id}/tasks/{task.id}", headers=tokens.of("bob")).status_code
            == 403
        )

    def test_missing_is_404(self, client: TestClient, tokens: Tokens) -> None:
        project = ProjectEntityFactory.create()

        assert client.get(f"/api/v1/projects/{project.id}/tasks/missing", headers=tokens.of("alice")).status_code == 404
