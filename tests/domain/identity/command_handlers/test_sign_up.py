from uuid import UUID

import pytest

from app.domain.identity.command_handlers.sign_up import sign_up_handler
from app.domain.identity.commands.sign_up import SignUpCommand
from app.domain.identity.exceptions import EmailTakenError

PASSWORD = "Passw0rd!x"


@pytest.mark.usefixtures("cognito")
class TestSignUpHandler:
    def test_returns_sub(self) -> None:
        result = sign_up_handler(SignUpCommand(email="a@x.io", password=PASSWORD))

        assert UUID(result.sub)

    def test_duplicate_email_is_conflict(self) -> None:
        sign_up_handler(SignUpCommand(email="a@x.io", password=PASSWORD))

        with pytest.raises(EmailTakenError):
            sign_up_handler(SignUpCommand(email="a@x.io", password=PASSWORD))
