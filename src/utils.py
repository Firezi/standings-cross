import pytz
from datetime import datetime
from jose import jwt, JWTError

from src.settings import settings
from src.exceptions import AuthException
from src.models import GameInfo


def create_jwt_token(username: str) -> str:
    data = {"usr": username}
    try:
        token = jwt.encode(data, settings.JWT_SECRET_KEY)
    except JWTError:
        raise AuthException

    return token


def get_username_from_jwt(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY)
        username = payload.get("usr")
        if username is None:
            raise AuthException
    except JWTError:
        raise AuthException

    return username


async def is_competition_running(now_dt: datetime) -> bool:
    game_info = await GameInfo.all().first()
    if game_info is None:
        return False
    if game_info.end_dt is None or game_info.start_dt < now_dt < game_info.end_dt:
        return True
    return False
