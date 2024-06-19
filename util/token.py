from datetime import datetime, timedelta, timezone
from jose import jwt

from config import Config

conf = Config()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=conf.get_access_token_expire_minutes()
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, conf.get_secret_key(), algorithm=conf.get_jwt_algorithm()
    )
    return encoded_jwt
