from fastapi import APIRouter, Depends
from starlette import status

from app.core.cognito import Cognito
from app.core.dependencies import get_cognito
from app.models.user import UserSignup
from app.services.auth.signup_service import signup_service

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup_user(user: UserSignup, cognito: Cognito = Depends(get_cognito)):
    return signup_service(user, cognito)
