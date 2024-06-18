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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="email and password combination is incorrect",
        )

    password = user_password.encode()
    salt = crud.get_salt(user).encode()
    hashed = bcrypt.hashpw(password, salt)
    if user.password != hashed.decode():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="email and password combination is incorrect",
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
    return "user has been registerd "
