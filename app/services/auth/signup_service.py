import botocore
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.cognito import Cognito
from app.models.user import UserSignup


def signup_service(user: UserSignup, cognito: Cognito):
    try:
        response = cognito.user_signup(user)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "UsernameExistsException":
            raise HTTPException(
                status_code=409, detail="An account with the given email already exists"
            )
        else:
            raise HTTPException(status_code=500, detail="Internal Server")
    else:
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            content = {
                "message": "User created successfully",
                "sub": response["UserSub"],
            }
            return JSONResponse(content=content, status_code=201)
