import ast
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from tests.fixtures.api import Tokens
from tests.fixtures.aws import CognitoFailure

API_DIR = Path(__file__).resolve().parents[3] / "app" / "entrypoints" / "api"
HTTP_METHODS = {"get", "post", "put", "patch", "delete"}
PROJECT = {"name": "Apollo", "description": "Moon", "max_users": 3}
TASK = {"name": "T", "description": ""}
PUBLIC_ROUTES = {
    "health_status",
    "signup",
    "verify",
    "signin",
    "refresh_token",
    "forgot_password",
    "confirm_forgot_password",
}
PROTECTED = [
    ("get", "/api/v1/projects", None),
    ("post", "/api/v1/projects", PROJECT),
    ("get", "/api/v1/projects/p1", None),
    ("put", "/api/v1/projects/p1", PROJECT),
    ("delete", "/api/v1/projects/p1", None),
    ("get", "/api/v1/projects/p1/tasks", None),
    ("post", "/api/v1/projects/p1/tasks", TASK),
    ("get", "/api/v1/projects/p1/tasks/t1", None),
    ("put", "/api/v1/projects/p1/tasks/t1", TASK),
    ("delete", "/api/v1/projects/p1/tasks/t1", None),
    ("get", "/api/v1/users", None),
    ("get", f"/api/v1/users/{uuid4()}", None),
    ("put", "/api/v1/users/me/email", {"email": "new@x.io"}),
    ("post", "/api/v1/auth/change", {"old_password": "Passw0rd!x", "new_password": "N3wPassw0rd!"}),
    ("post", "/api/v1/auth/logout", None),
]


def _route_sources() -> dict[str, str]:
    routes: dict[str, str] = {}
    for file in sorted(API_DIR.rglob("*.py")):
        for node in ast.walk(ast.parse(file.read_text())):
            if isinstance(node, ast.FunctionDef) and any(
                isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr in HTTP_METHODS
                for d in node.decorator_list
            ):
                routes[node.name] = ast.unparse(node)
    return routes


ROUTES = _route_sources()


class TestRouteSecurity:
    @pytest.mark.parametrize("name", sorted(ROUTES))
    def test_route_requires_auth_unless_public(self, name: str) -> None:
        assert "authorize_user" in ROUTES[name] or name in PUBLIC_ROUTES

    def test_public_allowlist_has_no_stale_entries(self) -> None:
        assert set(PUBLIC_ROUTES) <= set(ROUTES)

    @pytest.mark.usefixtures("tokens")
    @pytest.mark.parametrize(("method", "path", "body"), PROTECTED)
    @pytest.mark.parametrize("header", [None, "Bearer not-a-token", "Basic abc"])
    def test_protected_routes_reject_missing_or_invalid_token(
        self, client: TestClient, method: str, path: str, body: dict[str, object] | None, header: str | None
    ) -> None:
        headers = {"Authorization": header} if header else {}

        response = client.request(method, path, headers=headers, json=body)

        assert response.status_code == 401
        assert response.headers["WWW-Authenticate"] == "Bearer"


class TestErrorHandling:
    def test_provider_failures_are_generic_502(self, client: TestClient, cognito_error: CognitoFailure) -> None:
        cognito_error("forgot_password", "InternalErrorException")

        response = client.post("/api/v1/auth/forgot", json={"email": "a@x.io"})

        assert response.status_code == 502
        assert "InternalErrorException" not in response.text

    def test_validation_errors_do_not_echo_values(self, client: TestClient, tokens: Tokens) -> None:
        response = client.post("/api/v1/projects", json={**PROJECT, "id": "victim-project"}, headers=tokens.of("alice"))

        assert response.status_code == 422
        assert "victim" not in response.text

    @pytest.mark.usefixtures("dynamodb")
    def test_invalid_cursor_is_400(self, client: TestClient, tokens: Tokens) -> None:
        assert client.get("/api/v1/projects?cursor=garbage", headers=tokens.of("alice")).status_code == 400


class TestSecurityHeaders:
    def test_headers_are_set(self, client: TestClient) -> None:
        response = client.get("/api/v1/health")

        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["Cache-Control"] == "no-store"
