from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.shared.clients.cognito import CognitoClient
from tests.fixtures.api import Tokens

SUB = str(uuid4())
USER = {"Username": "alice", "Attributes": [{"Name": "sub", "Value": SUB}, {"Name": "email", "Value": "a@x.io"}]}


class TestGetUserEndpoint:
    def test_gets_user_by_sub_without_email(
        self, client: TestClient, tokens: Tokens, cognito: CognitoClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(cognito, "find_user_by_sub", lambda sub: USER if sub == SUB else None)

        response = client.get(f"/api/v1/users/{SUB}", headers=tokens.of("alice"))

        assert response.json()["id"] == "alice"
        assert "email" not in response.json()

    @pytest.mark.usefixtures("cognito")
    def test_unknown_is_404_and_non_uuid_is_422(self, client: TestClient, tokens: Tokens) -> None:
        headers = tokens.of("alice")

        assert client.get(f"/api/v1/users/{uuid4()}", headers=headers).status_code == 404
        assert client.get('/api/v1/users/x"%20or%20sub', headers=headers).status_code == 422
