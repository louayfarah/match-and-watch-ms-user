from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from util import users
from core.schemas import schemas
from dependencies import dependencies
from core.crud import crud

router = APIRouter()


@router.post("/api/register/", tags=["Authentication"])
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return users.register(user, db)


@router.post("/api/login", tags=["Authentication"])
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    return users.login(request, db)


@router.post("/api/user/preferences/", response_model=schemas.UserPreferences)
def create_user_preferences(
    preferences: schemas.UserPreferencesCreate,
    user: schemas.AuthenticatedUser = Depends(dependencies.get_user),
    db: Session = Depends(get_db)
):
    return users.create_user_preferences(preferences, user, db)


@router.get("/api/user/preferences/", response_model=schemas.UserPreferences)
def get_user_preferences(
    db: Session = Depends(get_db),
    user: schemas.AuthenticatedUser = Depends(dependencies.get_user)
):
    return users.get_user_preferences(user, db)
