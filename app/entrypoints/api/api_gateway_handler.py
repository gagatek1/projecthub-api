from collections.abc import Awaitable, Callable
from http import HTTPStatus

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from mangum import Mangum

from app.entrypoints.api.v1.auth import routers as auth_routers
from app.entrypoints.api.v1.health_status import router as health_router
from app.entrypoints.api.v1.projects import routers as projects_routers
from app.entrypoints.api.v1.tasks import routers as tasks_routers
from app.entrypoints.api.v1.users import routers as users_routers
from app.settings import app_settings
from app.shared.errors import (
    AlreadyExistsError,
    BusinessRuleError,
    ConflictError,
    DomainError,
    ExternalServiceError,
    InvalidInputError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitedError,
    UnauthenticatedError,
)

ROUTERS = [
    *auth_routers,
    *projects_routers,
    *tasks_routers,
    *users_routers,
    health_router,
]

STATUS_BY_ERROR: dict[type[DomainError], HTTPStatus] = {
    NotFoundError: HTTPStatus.NOT_FOUND,
    AlreadyExistsError: HTTPStatus.CONFLICT,
    ConflictError: HTTPStatus.CONFLICT,
    BusinessRuleError: HTTPStatus.UNPROCESSABLE_ENTITY,
    PermissionDeniedError: HTTPStatus.FORBIDDEN,
    ExternalServiceError: HTTPStatus.BAD_GATEWAY,
    InvalidInputError: HTTPStatus.BAD_REQUEST,
    RateLimitedError: HTTPStatus.TOO_MANY_REQUESTS,
    UnauthenticatedError: HTTPStatus.UNAUTHORIZED,
}

SECURITY_HEADERS: dict[str, str] = {
    "Strict-Transport-Security": "max-age=63072000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
    "Referrer-Policy": "no-referrer",
    "Cache-Control": "no-store",
}
DOCS_PATH = "/api-docs"

docs = app_settings.docs_enabled
app = FastAPI(
    title="ProjectHub API",
    description="API to manage projects and tasks",
    version="0.7.0",
    docs_url=DOCS_PATH if docs else None,
    redoc_url=None,
    openapi_url="/openapi.json" if docs else None,
)
for router in ROUTERS:
    app.include_router(router, prefix="/api/v1")


def status_for(error: DomainError) -> HTTPStatus:
    for cls in type(error).__mro__:
        if issubclass(cls, DomainError) and cls in STATUS_BY_ERROR:
            return STATUS_BY_ERROR[cls]
    return HTTPStatus.BAD_REQUEST


@app.middleware("http")
async def _security_headers(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    response = await call_next(request)
    headers = SECURITY_HEADERS
    if request.url.path.startswith(DOCS_PATH):
        headers = {k: v for k, v in SECURITY_HEADERS.items() if k != "Content-Security-Policy"}
    response.headers.update(headers)
    return response


@app.exception_handler(DomainError)
async def _domain_error(_: Request, error: DomainError) -> JSONResponse:
    message = ExternalServiceError.default_message if isinstance(error, ExternalServiceError) else error.message
    headers = {"WWW-Authenticate": "Bearer"} if isinstance(error, UnauthenticatedError) else None
    return JSONResponse(status_code=status_for(error), content={"message": message}, headers=headers)


@app.exception_handler(RequestValidationError)
async def _validation_error(_: Request, error: RequestValidationError) -> JSONResponse:
    errors = [{"loc": list(e["loc"]), "msg": e["msg"], "type": e["type"]} for e in error.errors()]
    return JSONResponse(status_code=422, content={"message": "Invalid request", "errors": errors})


lambda_handler = Mangum(app, lifespan="off")
