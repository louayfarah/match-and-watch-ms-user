from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security
from fastapi.exceptions import HTTPException

import core
import core.databases
import core.databases.postgres
import core.databases.postgres.postgres
import core.schemas
import core.schemas.schemas
from util.auth import get_user_from_token


def get_db():
    db = core.databases.postgres.postgres.session_local()
    try:
        yield db
    finally:
        db.close()


def get_user(
    authorization: HTTPAuthorizationCredentials = Security(HTTPBearer()),
) -> core.schemas.schemas.AuthenticatedUser:
    if authorization.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")

    token = authorization.credentials
    return get_user_from_token(token)
