from fastapi import APIRouter, Request, status

from app.domain.identity.command_handlers.change_email import change_email_handler
from app.domain.identity.commands.change_email import ChangeEmailCommand
from app.domain.identity.schemas import ChangeEmailRequest, MessageResponse
from app.shared.auth.authorize import authorize_user

router = APIRouter(tags=["users"])


@router.put(
    "/users/me/email",
    status_code=status.HTTP_202_ACCEPTED,
    description="Change the caller's email; Cognito sends a verification code to the new address.",
)
def update_email(body: ChangeEmailRequest, request: Request) -> MessageResponse:
    with authorize_user(request.headers) as user:
        change_email_handler(ChangeEmailCommand(access_token=user.access_token, email=body.email))
    return MessageResponse(message="Verification code sent to the new email")
