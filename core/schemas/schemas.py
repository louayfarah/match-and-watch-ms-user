from pydantic import BaseModel, ConfigDict
import uuid


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
