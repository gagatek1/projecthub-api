import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import ProjectEntityFactory, TaskEntityFactory


@pytest.mark.usefixtures("dynamodb")
class TestListTasksEndpoint:
    def test_owner_sees_all_assignee_sees_own(self, client: TestClient, tokens: Tokens) -> None:
        project = ProjectEntityFactory.create()
        own = TaskEntityFactory.create(project_id=project.id)
        bobs = TaskEntityFactory.create(project_id=project.id, assigned_user="bob")
        url = f"/api/v1/projects/{project.id}/tasks"

        assert {t["id"] for t in client.get(url, headers=tokens.of("alice")).json()["items"]} == {own.id, bobs.id}
        assert [t["id"] for t in client.get(url, headers=tokens.of("bob")).json()["items"]] == [bobs.id]

    def test_missing_project_is_404(self, client: TestClient, tokens: Tokens) -> None:
        assert client.get("/api/v1/projects/nope/tasks", headers=tokens.of("alice")).status_code == 404
