from sqlalchemy.orm import Session

from ..models import tables


def get_user_by_email(db: Session, email: str):
    return db.query(tables.User).filter(tables.User.email == email).first()


def get_salt(user: tables.User):
    return user.salt


def save_refresh_token(db: Session, user_id: int, refresh_token: str, expires_at: str):
    existing_token = (
        db.query(tables.RefreshToken)
        .filter(tables.RefreshToken.user_id == user_id)
        .first()
    )

    if existing_token:
        existing_token.refresh_tokens = refresh_token
        existing_token.expires_at = expires_at
    else:
        new_refresh_token = tables.RefreshToken(
            refresh_tokens=refresh_token, user_id=user_id, expires_at=expires_at
        )
        db.add(new_refresh_token)

    db.commit()


def get_refresh_token_by_user_id(db: Session, user_id: int):
    res = (
        db.query(tables.RefreshToken)
        .filter(tables.RefreshToken.user_id == user_id)
        .first()
    )
    if not res:
        return None
    return res


def get_refresh_token(db: Session, refresh_token: str):
    res = (
        db.query(tables.RefreshToken)
        .filter(tables.RefreshToken.refresh_tokens == refresh_token)
        .first()
    )
    if not res:
        return None
    return res


def get_preferences_by_id(db: Session, user_id: int):
    return db.query(tables.UserPreferences).filter(
        tables.UserPreferences.user_id == user_id
    ).first()
