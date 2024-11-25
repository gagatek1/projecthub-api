import botocore
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.cognito import Cognito
from app.models.user import UserVerify


def verify_service(data: UserVerify, cognito: Cognito):
    try:
        cognito.verify_account(data)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "CodeMismatchException":
            raise HTTPException(
                status_code=400,
                detail="The provided code does not match the expected value.",
            )
        elif e.response["Error"]["Code"] == "ExpiredCodeException":
            raise HTTPException(
                status_code=400, detail="The provided code has expired."
            )
        elif e.response["Error"]["Code"] == "UserNotFoundException":
            raise HTTPException(status_code=404, detail="User not found")
        else:
            raise HTTPException(status_code=500, detail="Internal Server")
    else:
        return JSONResponse(
            content={"message": "Account verification successful"}, status_code=200
        )
