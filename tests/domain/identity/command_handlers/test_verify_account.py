import pytest

from app.domain.identity.command_handlers.verify_account import verify_account_handler
from app.domain.identity.commands.verify_account import VerifyAccountCommand
from app.domain.identity.exceptions import InvalidCodeError, TooManyAttemptsError
from app.shared.errors import ExternalServiceError
from tests.fixtures.aws import CognitoFailure


class TestVerifyAccountHandler:
    @pytest.mark.parametrize(
        ("code", "error"),
        [
            ("CodeMismatchException", InvalidCodeError),
            ("ExpiredCodeException", InvalidCodeError),
            ("UserNotFoundException", InvalidCodeError),
            ("LimitExceededException", TooManyAttemptsError),
            ("InternalErrorException", ExternalServiceError),
        ],
    )
    def test_maps_provider_errors(self, cognito_error: CognitoFailure, code: str, error: type[Exception]) -> None:
        cognito_error("confirm_sign_up", code)

        with pytest.raises(error):
            verify_account_handler(VerifyAccountCommand(email="a@x.io", confirmation_code="123456"))
