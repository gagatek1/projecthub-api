from typing import Optional

from fastapi import Depends, Header, HTTPException, status

from app.core.cognito import Cognito
from app.core.dependencies import get_cognito


def get_token(
    authorization: Optional[str] = Header(None), cognito: Cognito = Depends(get_cognito)
):
    return authorize_user(cognito, authorization)


def authorize_user(cognito: Cognito, authorization: Optional[str]):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    token = authorization.split(" ")[1]

    try:
        user = cognito.get_user(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    return user
