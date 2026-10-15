from fastapi import APIRouter

from app.domain.identity.command_handlers.refresh_token import refresh_token_handler
from app.domain.identity.commands.refresh_token import RefreshTokenCommand
from app.domain.identity.schemas import RefreshTokenRequest, TokenResponse

router = APIRouter(tags=["auth"])


@router.post(
    "/auth/token", response_model_exclude_none=True, description="Get a new access token from a refresh token (public)."
)
def refresh_token(body: RefreshTokenRequest) -> TokenResponse:
    return refresh_token_handler(RefreshTokenCommand(**body.model_dump()))
