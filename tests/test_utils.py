from src.utils import create_jwt_token, get_username_from_jwt
from src.api.schemas import UserInStandings


def test_jwt_token_creation():
    username = "test-user"
    token = create_jwt_token(username)

    assert get_username_from_jwt(token) == username
