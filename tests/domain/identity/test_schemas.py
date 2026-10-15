from app.domain.identity.commands.sign_in import SignInCommand
from app.domain.identity.schemas import SignUpRequest


class TestPasswordModels:
    def test_passwords_are_not_whitespace_stripped(self) -> None:
        assert SignUpRequest(email="a@x.io", password=" Passw0rd! ").password == " Passw0rd! "
        assert SignInCommand(email="a@x.io", password=" Passw0rd! ").password == " Passw0rd! "
