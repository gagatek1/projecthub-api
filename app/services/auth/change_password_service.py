import botocore
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.cognito import Cognito
from app.models.auth import UserChangePassword


def change_password_service(data: UserChangePassword, cognito: Cognito):
    try:
        cognito.change_password(data)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "InvalidParameterException":
            raise HTTPException(
                status_code=400, detail="Access token provided has wrong format"
            )
        elif e.response["Error"]["Code"] == "NotAuthorizedException":
            raise HTTPException(
                status_code=401, detail="Incorrect username or password"
            )
        elif e.response["Error"]["Code"] == "LimitExceededException":
            raise HTTPException(
                status_code=429, detail="Attempt limit exceeded, please try again later"
            )
        else:
            raise HTTPException(status_code=500, detail="Internal Server")
    else:
        return JSONResponse(
            content={"message": "Password changed successfully"}, status_code=200
        )
