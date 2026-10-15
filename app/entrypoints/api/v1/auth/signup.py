from fastapi import APIRouter, status

from app.domain.identity.command_handlers.sign_up import sign_up_handler
from app.domain.identity.commands.sign_up import SignUpCommand
from app.domain.identity.schemas import SignUpRequest, SignUpResponse

router = APIRouter(tags=["auth"])


@router.post("/auth/signup", status_code=status.HTTP_201_CREATED, description="Sign up a new user (public).")
def signup(body: SignUpRequest) -> SignUpResponse:
    return sign_up_handler(SignUpCommand(**body.model_dump()))
