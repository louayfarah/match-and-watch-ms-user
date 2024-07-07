from sqlalchemy.orm import Session

from ..models import tables


def get_user_by_email(db: Session, email: str):
    return db.query(tables.User).filter(tables.User.email == email).first()


def get_salt(user: tables.User):
    return user.salt


def get_preferences_by_id(db: Session, user_id: int):
    return db.query(tables.UserPreferences).filter(
        tables.UserPreferences.user_id == user_id
    ).first()
