from fastapi import APIRouter, Depends
from starlette import status

from app.core.cognito import Cognito
from app.core.dependencies import get_cognito
from app.models.auth import (UserChangePassword, UserConfirmForgotPassword,
                             UserForgotPassword, UserLogout, UserRefreshToken,
                             UserSignin, UserSignup, UserVerify)
from app.services.auth.change_password_service import change_password_service
from app.services.auth.confirm_forgot_password_service import \
    confirm_forgot_password_service
from app.services.auth.forgot_password_service import forgot_password_service
from app.services.auth.logout_service import logout_service
from app.services.auth.new_token_service import new_token_service
from app.services.auth.signin_service import signin_service
from app.services.auth.signup_service import signup_service
from app.services.auth.verify_service import verify_service

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup_user(user: UserSignup, cognito: Cognito = Depends(get_cognito)):
    return signup_service(user, cognito)


@auth_router.post("/verify")
async def verify_user(data: UserVerify, cognito: Cognito = Depends(get_cognito)):
    return verify_service(data, cognito)


@auth_router.post("/signin")
async def signin_user(data: UserSignin, cognito: Cognito = Depends(get_cognito)):
    return signin_service(data, cognito)


@auth_router.post("/token")
async def generate_new_token(
    data: UserRefreshToken, cognito: Cognito = Depends(get_cognito)
):
    return new_token_service(data, cognito)


@auth_router.post("/change")
async def change_password(
    data: UserChangePassword, cognito: Cognito = Depends(get_cognito)
):
    return change_password_service(data, cognito)


@auth_router.post("/forgot")
async def forgot_password(
    data: UserForgotPassword, cognito: Cognito = Depends(get_cognito)
):
    return forgot_password_service(data, cognito)


@auth_router.post("/confirm")
async def confirm_forgot_password(
    data: UserConfirmForgotPassword, cognito: Cognito = Depends(get_cognito)
):
    return confirm_forgot_password_service(data, cognito)


@auth_router.post("/logout")
async def logout(data: UserLogout, cognito: Cognito = Depends(get_cognito)):
    return logout_service(data, cognito)
