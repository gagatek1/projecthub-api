from fastapi import APIRouter

from app.domain.identity.command_handlers.sign_in import sign_in_handler
from app.domain.identity.commands.sign_in import SignInCommand
from app.domain.identity.schemas import SignInRequest, TokenResponse

router = APIRouter(tags=["auth"])


@router.post("/auth/signin", response_model_exclude_none=True, description="Sign in and get tokens (public).")
def signin(body: SignInRequest) -> TokenResponse:
    return sign_in_handler(SignInCommand(**body.model_dump()))
