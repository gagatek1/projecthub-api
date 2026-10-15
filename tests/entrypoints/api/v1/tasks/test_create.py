import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import ProjectEntityFactory

TASK = {"name": "T", "description": ""}


@pytest.mark.usefixtures("dynamodb", "known_users")
class TestCreateTaskEndpoint:
    def test_creates_task_assigned_to_caller(self, client: TestClient, tokens: Tokens) -> None:
        project = ProjectEntityFactory.create()

        response = client.post(f"/api/v1/projects/{project.id}/tasks", json=TASK, headers=tokens.of("alice"))

        assert response.status_code == 201
        assert (response.json()["assigned_user"], response.json()["project_id"]) == ("alice", project.id)

    def test_assigns_existing_user_only(self, client: TestClient, tokens: Tokens) -> None:
        url = f"/api/v1/projects/{ProjectEntityFactory.create().id}/tasks"
        headers = tokens.of("alice")

        assert client.post(url, json={**TASK, "assigned_user": "bob"}, headers=headers).status_code == 201
        assert client.post(url, json={**TASK, "assigned_user": "ghost"}, headers=headers).status_code == 404

    def test_project_rules(self, client: TestClient, tokens: Tokens) -> None:
        project = ProjectEntityFactory.create()

        assert client.post("/api/v1/projects/nope/tasks", json=TASK, headers=tokens.of("alice")).status_code == 404
        assert (
            client.post(f"/api/v1/projects/{project.id}/tasks", json=TASK, headers=tokens.of("bob")).status_code == 403
        )

    def test_project_id_in_body_is_rejected(self, client: TestClient, tokens: Tokens) -> None:
        url = f"/api/v1/projects/{ProjectEntityFactory.create().id}/tasks"

        assert client.post(url, json={**TASK, "project_id": "x"}, headers=tokens.of("alice")).status_code == 422
