from fastapi.testclient import TestClient

from tests.fixtures.aws import CognitoFailure

BODY = {"email": "a@x.io", "confirmation_code": "123456", "new_password": "N3wPassw0rd!"}


class TestConfirmEndpoint:
    def test_wrong_code_is_400(self, client: TestClient, cognito_error: CognitoFailure) -> None:
        cognito_error("confirm_forgot_password", "CodeMismatchException")

        assert client.post("/api/v1/auth/confirm", json=BODY).status_code == 400

    def test_unknown_user_looks_like_wrong_code(self, client: TestClient, cognito_error: CognitoFailure) -> None:
        cognito_error("confirm_forgot_password", "UserNotFoundException")

        assert client.post("/api/v1/auth/confirm", json=BODY).status_code == 400
