import os

from dotenv import load_dotenv

load_dotenv()


SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = 36 * 60
