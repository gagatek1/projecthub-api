import os

_TEST_ENV = {
    "APP_ENV_FILE": "",
    "APP_STAGE": "test",
    "REGION_NAME": "eu-central-1",
    "AWS_DEFAULT_REGION": "eu-central-1",
    "AWS_ACCESS_KEY_ID": "testing",
    "AWS_SECRET_ACCESS_KEY": "testing",
    "AWS_COGNITO_APP_CLIENT_ID": "placeholder",
    "AWS_COGNITO_USER_POOL_ID": "placeholder",
    "DYNAMODB_TABLE": "projecthub-test",
}
for _key, _value in _TEST_ENV.items():
    os.environ[_key] = _value

from tests.fixtures.api import client, cognito_users, known_users, tokens  # noqa: E402, F401
from tests.fixtures.aws import aws, cognito, cognito_error, dynamodb  # noqa: E402, F401
