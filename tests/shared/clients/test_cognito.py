from app.shared.clients.cognito import CognitoClient


class TestCognitoClient:
    def test_secret_hash_is_omitted_for_clients_without_secret(self, cognito: CognitoClient) -> None:
        cognito._client_secret = ""

        assert cognito.secret_hash("a@x.io") == {}

    def test_secret_hash_is_sent_for_clients_with_secret(self, cognito: CognitoClient) -> None:
        assert set(cognito.secret_hash("a@x.io")) == {"SecretHash"}
