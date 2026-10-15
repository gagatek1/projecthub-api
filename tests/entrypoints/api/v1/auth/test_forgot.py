import pytest
from fastapi.testclient import TestClient

from tests.fixtures.aws import CognitoFailure


class TestForgotEndpoint:
    @pytest.mark.parametrize("code", ["UserNotFoundException", "InvalidParameterException"])
    def test_same_answer_whether_or_not_account_exists(
        self, client: TestClient, cognito_error: CognitoFailure, code: str
    ) -> None:
        cognito_error("forgot_password", code)

        response = client.post("/api/v1/auth/forgot", json={"email": "a@x.io"})

        assert response.status_code == 200
