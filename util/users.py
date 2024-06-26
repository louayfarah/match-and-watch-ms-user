import bcrypt

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from core.crud import crud
from core.schemas import schemas
from util.token import create_access_token
from core.models import tables


def login(request: schemas.LoginRequest, db: Session):
    user_email = request.email
    user_password = request.password
    user = crud.get_user_by_email(db, email=user_email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    hashed_password = user.password.encode()
    provided_password = user_password.encode()

    if not bcrypt.checkpw(provided_password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(
        data={
            "sub": user.email,
            "id": str(user.id),
            "name": user.name,
            "surname": user.surname,
        }
    )
    return {"token": access_token}


def register(user: schemas.UserCreate, db: Session):
    db_user_email = crud.get_user_by_email(db, email=user.email)
    if db_user_email:
        raise HTTPException(status_code=409, detail="The email is already registered")

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode(), salt).decode()
    new_user = tables.User(
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=hashed_password,
        salt=salt.decode(),
    )
    db.add(new_user)
    db.commit()
    access_token = create_access_token(
        data={
            "sub": new_user.email,
            "id": str(new_user.id),
            "name": new_user.name,
            "surname": new_user.surname,
        }
    )
    return {"token": access_token}


def create_user_preferences(
    preferences: schemas.UserPreferencesCreate,
    user: schemas.AuthenticatedUser,
    db: Session,
):
    # Check if the user already has preferences
    existing_preferences = crud.get_preferences_by_id(db, user.id)

    if existing_preferences:
        for key, value in preferences.dict().items():
            setattr(existing_preferences, key, value)
        db.commit()
        return existing_preferences
    else:
        db_preferences = tables.UserPreferences(user_id=user.id, **preferences.dict())
        db.add(db_preferences)
        db.commit()
        return db_preferences


def get_user_preferences(user: schemas.AuthenticatedUser, db: Session):
    user_preferences = crud.get_preferences_by_id(db, user.id)
    if not user_preferences:
        raise HTTPException(status_code=404, detail="User preferences not found")

    return user_preferences
