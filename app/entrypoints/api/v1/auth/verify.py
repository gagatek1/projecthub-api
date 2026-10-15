from fastapi import APIRouter

from app.domain.identity.command_handlers.verify_account import verify_account_handler
from app.domain.identity.commands.verify_account import VerifyAccountCommand
from app.domain.identity.schemas import MessageResponse, VerifyAccountRequest

router = APIRouter(tags=["auth"])


@router.post("/auth/verify", description="Confirm an account with the emailed code (public).")
def verify(body: VerifyAccountRequest) -> MessageResponse:
    verify_account_handler(VerifyAccountCommand(**body.model_dump()))
    return MessageResponse(message="Account verification successful")
