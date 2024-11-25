import base64
import hashlib
import hmac
from os import getenv

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from app.models.user import UserSignup

load_dotenv()

REGION_NAME = getenv("REGION_NAME")
AWS_COGNITO_APP_CLIENT_ID = getenv("AWS_COGNITO_APP_CLIENT_ID")
AWS_COGNITO_APP_CLIENT_SECRET = getenv("AWS_COGNITO_APP_CLIENT_SECRET")
AWS_COGNITO_USER_POOL_ID = getenv("AWS_COGNITO_USER_POOL_ID")


class Cognito:
    def __init__(self):
        self.client = boto3.client("cognito-idp", region_name=REGION_NAME)

    def _generate_secret_hash(self, username: str) -> str:
        message = username + AWS_COGNITO_APP_CLIENT_ID
        secret = AWS_COGNITO_APP_CLIENT_SECRET
        digest = hmac.new(
            secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        return base64.b64encode(digest).decode()

    def user_signup(self, user: UserSignup):
        try:
            secret_hash = self._generate_secret_hash(user.email)
            response = self.client.sign_up(
                ClientId=AWS_COGNITO_APP_CLIENT_ID,
                Username=user.email,
                Password=user.password,
                SecretHash=secret_hash,
            )
            return response
        except ClientError as e:
            error_message = e.response.get("Error", {}).get("Message", "Unknown error")
            raise ValueError(f"Cognito sign-up failed: {error_message}")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {e}")
