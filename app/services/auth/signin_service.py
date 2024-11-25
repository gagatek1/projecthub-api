import botocore
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.cognito import Cognito
from app.models.user import UserSignin


def signin_service(data: UserSignin, cognito: Cognito):
    try:
        response = cognito.user_signin(data)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "UserNotFoundException":
            raise HTTPException(status_code=404, detail="User does not exist")
        elif e.response["Error"]["Code"] == "UserNotConfirmedException":
            raise HTTPException(status_code=403, detail="Please verify your account")
        elif e.response["Error"]["Code"] == "NotAuthorizedException":
            raise HTTPException(
                status_code=401, detail="Incorrect username or password"
            )
        else:
            raise HTTPException(status_code=500, detail="Internal Server")
    else:
        content = {
            "AccessToken": response["AuthenticationResult"]["AccessToken"],
            "RefreshToken": response["AuthenticationResult"]["RefreshToken"],
            "ExpiresIn": response["AuthenticationResult"]["ExpiresIn"],
        }

        return JSONResponse(content=content, status_code=200)
