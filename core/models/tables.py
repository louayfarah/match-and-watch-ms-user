import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ARRAY, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    surname = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    salt = Column(String(255))
    preferences = relationship(
        "UserPreferences", backref="user", cascade="all,delete-orphan"
    )


class UserPreferences(Base):
    __tablename__ = "user_preferences"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    genres = Column(ARRAY(String))
    favorite_type = Column(String)
    watching_habits = Column(String)
    preferred_language = Column(String)
    age_preference = Column(String)
    favorite_directors_actors = Column(ARRAY(String))
    preferred_length = Column(String)
    review_sources = Column(ARRAY(String))
