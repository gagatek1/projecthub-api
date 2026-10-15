import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.factories import ProjectEntityFactory


@pytest.mark.usefixtures("dynamodb")
class TestListProjectsEndpoint:
    def test_lists_only_callers_projects_paginated(self, client: TestClient, tokens: Tokens) -> None:
        mine = {p.id for p in ProjectEntityFactory.create_batch(3)}
        ProjectEntityFactory.create(project_owner="bob")
        headers = tokens.of("alice")

        first = client.get("/api/v1/projects?limit=2", headers=headers).json()
        second = client.get(f"/api/v1/projects?limit=2&cursor={first['next_cursor']}", headers=headers).json()

        assert len(first["items"]) == 2
        assert {p["id"] for p in first["items"] + second["items"]} == mine

    @pytest.mark.parametrize("limit", [0, 101])
    def test_rejects_invalid_limit(self, client: TestClient, tokens: Tokens, limit: int) -> None:
        assert client.get(f"/api/v1/projects?limit={limit}", headers=tokens.of("alice")).status_code == 422
