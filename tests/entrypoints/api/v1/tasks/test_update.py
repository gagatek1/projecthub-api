import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import ProjectEntityFactory, TaskEntityFactory

TASK = {"name": "T2", "description": ""}


@pytest.mark.usefixtures("dynamodb", "known_users")
class TestUpdateTaskEndpoint:
    def test_assignee_updates_and_reassigns(self, client: TestClient, tokens: Tokens) -> None:
        task = TaskEntityFactory.create()
        url = f"/api/v1/projects/{task.project_id}/tasks/{task.id}"

        response = client.put(url, json={**TASK, "assigned_user": "bob"}, headers=tokens.of("alice"))

        assert response.status_code == 200
        assert (response.json()["name"], response.json()["assigned_user"]) == ("T2", "bob")

    def test_non_assignee_is_forbidden(self, client: TestClient, tokens: Tokens) -> None:
        task = TaskEntityFactory.create(assigned_user="bob")
        url = f"/api/v1/projects/{task.project_id}/tasks/{task.id}"

        assert client.put(url, json=TASK, headers=tokens.of("alice")).status_code == 403

    def test_missing_is_404(self, client: TestClient, tokens: Tokens) -> None:
        url = f"/api/v1/projects/{ProjectEntityFactory.create().id}/tasks/missing"

        assert client.put(url, json=TASK, headers=tokens.of("alice")).status_code == 404
