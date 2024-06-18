from jose import JWTError, jwt

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from fastapi import status, Security

from ..core.schemas import schemas
from .const import JWT_ALGORITHM, SECRET_KEY


def get_user_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        payload["email"] = payload.pop("sub")
        payload["has_logged_in"] = True
        return schemas.AuthenticatedUser(**payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def get_user(
    authorization: HTTPAuthorizationCredentials = Security(HTTPBearer()),
) -> schemas.AuthenticatedUser:
    if authorization.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")

    token = authorization.credentials
    return get_user_from_token(token)
