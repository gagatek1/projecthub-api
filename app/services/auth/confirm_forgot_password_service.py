import botocore
import botocore.exceptions
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.cognito import Cognito
from app.models.user import UserConfirmForgotPassword


def confirm_forgot_password_service(data: UserConfirmForgotPassword, cognito: Cognito):
    try:
        cognito.confirm_forgot_password(data)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "ExpiredCodeException":
            raise HTTPException(status_code=403, detail="Code expired.")
        elif e.response["Error"]["Code"] == "CodeMismatchException":
            raise HTTPException(status_code=400, detail="Code does not match.")
        else:
            raise HTTPException(status_code=500, detail="Internal Server")
    else:
        return JSONResponse(
            content={"message": "password change"}, status_code=200
        )
