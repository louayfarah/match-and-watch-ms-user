import uuid

from typing import List
from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    email: str
    password: str


class UserBase(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    pass


class AuthenticatedUser(BaseModel):
    email: str | None = None
    id: uuid.UUID
    name: str | None = None
    surname: str | None = None
    has_logged_in: bool


class AccessToken(BaseModel):
    access_token: str
    expires_in: int

    
class UserPreferences(BaseModel):
    genres: List[str]
    favorite_type: str
    watching_habits: str
    preferred_language: str
    age_preference: str
    favorite_directors_actors: List[str]
    preferred_length: str
    review_sources: List[str]
    model_config = ConfigDict(from_attributes=True)


class UserPreferencesCreate(UserPreferences):
    pass
