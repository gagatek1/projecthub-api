from fastapi import APIRouter, Request

from app.domain.identity.command_handlers.change_password import change_password_handler
from app.domain.identity.commands.change_password import ChangePasswordCommand
from app.domain.identity.schemas import ChangePasswordRequest, MessageResponse
from app.shared.auth.authorize import authorize_user

router = APIRouter(tags=["auth"])


@router.post("/auth/change", description="Change the caller's password.")
def change_password(body: ChangePasswordRequest, request: Request) -> MessageResponse:
    with authorize_user(request.headers) as user:
        change_password_handler(ChangePasswordCommand(access_token=user.access_token, **body.model_dump()))
    return MessageResponse(message="Password changed successfully")
