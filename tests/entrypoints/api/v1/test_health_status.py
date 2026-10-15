from fastapi.testclient import TestClient


class TestHealthStatusEndpoint:
    def test_ok(self, client: TestClient) -> None:
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
