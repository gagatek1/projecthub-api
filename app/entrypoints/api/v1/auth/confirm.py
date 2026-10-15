from fastapi import APIRouter

from app.domain.identity.command_handlers.confirm_forgot_password import confirm_forgot_password_handler
from app.domain.identity.commands.confirm_forgot_password import ConfirmForgotPasswordCommand
from app.domain.identity.schemas import ConfirmForgotPasswordRequest, MessageResponse

router = APIRouter(tags=["auth"])


@router.post("/auth/confirm", description="Reset the password with the emailed code (public).")
def confirm_forgot_password(body: ConfirmForgotPasswordRequest) -> MessageResponse:
    confirm_forgot_password_handler(ConfirmForgotPasswordCommand(**body.model_dump()))
    return MessageResponse(message="Password changed successfully")
