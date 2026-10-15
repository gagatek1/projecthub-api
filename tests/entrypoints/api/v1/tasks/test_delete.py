import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import TaskEntityFactory


@pytest.mark.usefixtures("dynamodb")
class TestDeleteTaskEndpoint:
    def test_assignee_deletes(self, client: TestClient, tokens: Tokens) -> None:
        task = TaskEntityFactory.create()
        url = f"/api/v1/projects/{task.project_id}/tasks/{task.id}"

        assert client.delete(url, headers=tokens.of("alice")).status_code == 204
        assert client.delete(url, headers=tokens.of("alice")).status_code == 404

    def test_outsider_is_forbidden(self, client: TestClient, tokens: Tokens) -> None:
        task = TaskEntityFactory.create()

        assert (
            client.delete(f"/api/v1/projects/{task.project_id}/tasks/{task.id}", headers=tokens.of("bob")).status_code
            == 403
        )
