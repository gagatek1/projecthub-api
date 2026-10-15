from pydantic import BaseModel, ConfigDict

from app.shared.types import ConfirmationCode, Email


class VerifyAccountCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    email: Email
    confirmation_code: ConfirmationCode
