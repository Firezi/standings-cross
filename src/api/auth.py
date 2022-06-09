from fastapi import Depends, APIRouter
from fastapi.security import APIKeyHeader

from src.models import User, UserSchema
from src.exceptions import AuthException
from src.utils import create_jwt_token, get_username_from_jwt
from .schemas import UserTokenResponse, UserCredentials


router = APIRouter()

oauth2_schema = APIKeyHeader(name="Authorization")


async def get_authorized_user(token: str = Depends(oauth2_schema)) -> User:
    user = await User.get_or_none(username=get_username_from_jwt(token))
    return user


@router.post("/auth", response_model=UserTokenResponse)
async def login(credentials: UserCredentials = Depends()):
    user = await User.get_or_none(username=credentials.username)
    if not user or not user.verify_password(credentials.password.get_secret_value()):
        raise AuthException
    token = create_jwt_token(user.username)
    return {"access_token": token}
