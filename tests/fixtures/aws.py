from collections.abc import Callable, Iterator

import boto3
import pytest
from moto import mock_aws
from pydantic import SecretStr

from app.settings import CognitoSettings
from app.shared.clients import cognito as cognito_module
from app.shared.clients.cognito import CognitoClient, CognitoError, get_cognito
from app.shared.entities.base import BaseEntity

REGION = "eu-central-1"


@pytest.fixture
def aws() -> Iterator[None]:
    with mock_aws():
        yield


@pytest.fixture
def dynamodb(aws: None) -> None:
    BaseEntity.create_table(wait=True)


@pytest.fixture
def cognito(aws: None, monkeypatch: pytest.MonkeyPatch) -> Iterator[CognitoClient]:
    idp = boto3.client("cognito-idp", region_name=REGION)
    pool_id = idp.create_user_pool(PoolName="test", UsernameAttributes=["email"])["UserPool"]["Id"]
    app_client = idp.create_user_pool_client(
        UserPoolId=pool_id,
        ClientName="api",
        GenerateSecret=True,
        ExplicitAuthFlows=["ALLOW_USER_PASSWORD_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"],
    )["UserPoolClient"]
    settings = CognitoSettings(
        region=REGION,
        app_client_id=app_client["ClientId"],
        app_client_secret=SecretStr(app_client["ClientSecret"]),
        user_pool_id=pool_id,
    )
    monkeypatch.setattr(cognito_module, "cognito_settings", settings)
    get_cognito.cache_clear()
    yield get_cognito()
    get_cognito.cache_clear()


CognitoFailure = Callable[[str, str], None]


@pytest.fixture
def cognito_error(cognito: CognitoClient, monkeypatch: pytest.MonkeyPatch) -> CognitoFailure:
    def fail(method: str, code: str) -> None:
        def raise_error(*_: object, **__: object) -> None:
            raise CognitoError(code)

        monkeypatch.setattr(cognito, method, raise_error)

    return fail
