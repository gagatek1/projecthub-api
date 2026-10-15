import os
from typing import Literal

from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

REGION_PATTERN = r"^[a-z]{2}(-[a-z]+)+-\d$"
_REGION_ENV = AliasChoices("REGION_NAME", "AWS_REGION", "AWS_DEFAULT_REGION")


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.getenv("APP_ENV_FILE", ".env") or None, extra="ignore", frozen=True)


class AppSettings(_Settings):
    model_config = SettingsConfigDict(env_prefix="APP_")

    stage: Literal["dev", "test", "staging", "prod"] = Field(default="dev", description="Deployment stage")

    @property
    def docs_enabled(self) -> bool:
        return self.stage != "prod"


class CognitoSettings(_Settings):
    model_config = SettingsConfigDict(env_prefix="AWS_COGNITO_")

    region: str = Field(pattern=REGION_PATTERN, validation_alias=_REGION_ENV, description="Cognito region")
    app_client_id: str = Field(min_length=1, max_length=128, description="Cognito app client id")
    app_client_secret: SecretStr = Field(
        default=SecretStr(""), description="App client secret; blank for clients without a secret"
    )
    user_pool_id: str = Field(min_length=1, max_length=55, description="Cognito user pool id")


class DynamoDBSettings(_Settings):
    model_config = SettingsConfigDict(env_prefix="DYNAMODB_")

    table: str = Field(default="projecthub", min_length=3, max_length=255, description="Single-table name")
    region: str = Field(pattern=REGION_PATTERN, validation_alias=_REGION_ENV, description="AWS region of the table")
    host: str | None = Field(default=None, description="Endpoint override, only for DynamoDB Local")


app_settings = AppSettings()
cognito_settings = CognitoSettings()
dynamodb_settings = DynamoDBSettings()
