from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from core.databases.postgres.postgres import get_db
from util import users
from core.schemas import schemas


router = APIRouter()


@router.post("/api/register/", tags=["Authentication"])
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return users.register(user, db)


@router.post("/api/login", tags=["Authentication"])
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    return users.login(request, db)
