import jwt
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, Body
from sqlalchemy.orm import Session
from dependencies import get_db, get_user
from util import users
from core.schemas import schemas
from core.crud import crud
from util import token

router = APIRouter(tags=["Authentication"])


@router.post("/api/register/")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return users.register(user, db)


@router.post("/api/login")
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    return users.login(request, db)


@router.post("/api/logout")
def logout(
    refresh_token: Annotated[str, Body(embed=True)], db: Session = Depends(get_db)
):
    return users.logout(db, refresh_token)


@router.post("/refresh-token", response_model=schemas.AccessToken)
def regenerate_access_token(
    refresh_token: Annotated[str, Body(embed=True)], db: Session = Depends(get_db)
):
    try:
        res = crud.get_refresh_token(db, refresh_token)
        if res is None:
            raise HTTPException(detail="Invalid refresh token", status_code=400)

        return token.regenerate_access_token(refresh_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(detail="Token has expired", status_code=400)
    except jwt.InvalidTokenError:
        raise HTTPException(detail="Invalid refresh token", status_code=400)


@router.get("/get_token")
def get_token(
    user: schemas.AuthenticatedUser = Depends(get_user), db: Session = Depends(get_db)
):
    refresh_token = crud.get_refresh_token_by_user_id(db, user.id)
    if not refresh_token:
        raise HTTPException(
            status_code=404, detail="Refresh token not found for the user"
        )
    return refresh_token
@router.post("/api/user/preferences/", response_model=schemas.UserPreferences)
def create_user_preferences(
    preferences: schemas.UserPreferencesCreate,
    user: schemas.AuthenticatedUser = Depends(get_user),
    db: Session = Depends(get_db)
):
    return users.create_user_preferences(preferences, user, db)


@router.get("/api/user/preferences/", response_model=schemas.UserPreferences)
def get_user_preferences(
    db: Session = Depends(get_db),
    user: schemas.AuthenticatedUser = Depends(get_user)
):
    return users.get_user_preferences(user, db)
