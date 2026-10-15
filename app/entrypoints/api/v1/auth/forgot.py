from fastapi import APIRouter

from app.domain.identity.command_handlers.forgot_password import forgot_password_handler
from app.domain.identity.commands.forgot_password import ForgotPasswordCommand
from app.domain.identity.schemas import ForgotPasswordRequest, MessageResponse

router = APIRouter(tags=["auth"])


@router.post("/auth/forgot", description="Send a password reset code (public).")
def forgot_password(body: ForgotPasswordRequest) -> MessageResponse:
    forgot_password_handler(ForgotPasswordCommand(**body.model_dump()))
    return MessageResponse(message="Password reset code sent")
