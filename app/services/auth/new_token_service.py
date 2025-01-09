import botocore
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.cognito import Cognito
from app.models.auth import UserRefreshToken


def new_token_service(data: UserRefreshToken, cognito: Cognito):
    try:
        response = cognito.new_token(data)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "InvalidParameterException":
            raise HTTPException(
                status_code=400, detail="Refresh token provided has wrong format"
            )
        elif e.response["Error"]["Code"] == "NotAuthorizedException":
            raise HTTPException(
                status_code=401, detail="Invalid refresh token provided"
            )
        elif e.response["Error"]["Code"] == "LimitExceededException":
            raise HTTPException(
                status_code=429, detail="Attempt limit exceeded, please try again later"
            )
        else:
            raise HTTPException(status_code=500, detail="Internal Server")
    else:
        content = {
            "AccessToken": response["AuthenticationResult"]["AccessToken"],
            "ExpiresIn": response["AuthenticationResult"]["ExpiresIn"],
        }
        return JSONResponse(content=content, status_code=200)
