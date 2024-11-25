from fastapi import APIRouter, Depends
from starlette import status

from app.core.cognito import Cognito
from app.core.dependencies import get_cognito
from app.models.user import UserSignup, UserVerify
from app.services.auth.signup_service import signup_service
from app.services.auth.verify_service import verify_service

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup_user(user: UserSignup, cognito: Cognito = Depends(get_cognito)):
    return signup_service(user, cognito)


@auth_router.post("/verify")
async def verify_user(data: UserVerify, cognito: Cognito = Depends(get_cognito)):
    return verify_service(data, cognito)
