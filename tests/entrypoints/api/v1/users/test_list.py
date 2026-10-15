from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.shared.clients.cognito import CognitoClient
from tests.fixtures.api import Tokens

USER: dict[str, Any] = {
    "Username": "alice",
    "Attributes": [{"Name": "sub", "Value": "s1"}, {"Name": "email", "Value": "a@x.io"}],
}


class TestListUsersEndpoint:
    def test_lists_public_fields_with_cursor(
        self, client: TestClient, tokens: Tokens, cognito: CognitoClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        calls: list[tuple[int, str | None]] = []

        def list_users(limit: int, pagination_token: str | None = None) -> tuple[list[dict[str, Any]], str | None]:
            calls.append((limit, pagination_token))
            return [USER], "next-page"

        monkeypatch.setattr(cognito, "list_users", list_users)

        response = client.get("/api/v1/users?limit=5&cursor=page-1", headers=tokens.of("alice")).json()

        assert calls == [(5, "page-1")]
        assert response == {
            "items": [{"id": "alice", "sub": "s1", "status": None, "enabled": None}],
            "next_cursor": "next-page",
        }

    @pytest.mark.usefixtures("cognito")
    def test_rejects_limit_above_cognito_maximum(self, client: TestClient, tokens: Tokens) -> None:
        assert client.get("/api/v1/users?limit=61", headers=tokens.of("alice")).status_code == 422
