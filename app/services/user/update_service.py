from typing import Optional

from fastapi import Header, HTTPException
from starlette import status

from app.core.cognito import Cognito
from app.models.user import UserEmail


def get_token(authorization: Optional[str] = Header(None)):
    return authorization


def update_email_service(data: UserEmail, authorization, cognito: Cognito):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    access_token = authorization.split(" ")[1]
    email = data.email
    return cognito.change_user_email(access_token, email)
