from sqlalchemy import Column, Integer, String

from ..databases.postgres.postgres import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255))
    surname = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    salt = Column(String(255))
