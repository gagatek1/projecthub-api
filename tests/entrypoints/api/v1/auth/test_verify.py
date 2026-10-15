from fastapi.testclient import TestClient

from tests.fixtures.aws import CognitoFailure


class TestVerifyEndpoint:
    def test_wrong_code_is_400(self, client: TestClient, cognito_error: CognitoFailure) -> None:
        cognito_error("confirm_sign_up", "CodeMismatchException")

        response = client.post("/api/v1/auth/verify", json={"email": "a@x.io", "confirmation_code": "123456"})

        assert response.status_code == 400

    def test_unknown_user_looks_like_wrong_code(self, client: TestClient, cognito_error: CognitoFailure) -> None:
        cognito_error("confirm_sign_up", "UserNotFoundException")

        response = client.post("/api/v1/auth/verify", json={"email": "a@x.io", "confirmation_code": "123456"})

        assert response.status_code == 400
