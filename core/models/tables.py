import uuid
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy import Column, String

from ..databases.postgres.postgres import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key= True, default=uuid.uuid4)
    name = Column(String(255))
    surname = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    salt = Column(String(255))
