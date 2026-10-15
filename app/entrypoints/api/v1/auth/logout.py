from fastapi import APIRouter, Request, Response, status

from app.domain.identity.command_handlers.sign_out import sign_out_handler
from app.domain.identity.commands.sign_out import SignOutCommand
from app.shared.auth.authorize import authorize_user

router = APIRouter(tags=["auth"])


@router.post(
    "/auth/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    description="Global sign-out: revokes every token of the caller.",
)
def logout(request: Request) -> None:
    with authorize_user(request.headers) as user:
        sign_out_handler(SignOutCommand(access_token=user.access_token))
