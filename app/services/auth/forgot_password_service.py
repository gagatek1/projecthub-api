import botocore
import botocore.exceptions
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.cognito import Cognito
from app.models.user import UserForgotPassword


def forgot_password_service(data: UserForgotPassword, cognito: Cognito):
    try:
        cognito.forgot_password(data)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "UserNotFoundException":
            raise HTTPException(status_code=404, detail="User does not exist")
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            raise HTTPException(status_code=403, detail="Unverified account")
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")

    return JSONResponse(
        content={"message": "password reset code sent"}, status_code=200
    )
