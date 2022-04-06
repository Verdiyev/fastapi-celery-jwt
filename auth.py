from typing import Optional
from models import User
from fastapi.security import OAuth2PasswordBearer
from database import db
from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return PWD_CONTEXT.verify(plain_password, hashed_password)

def get_password_hash(password):
    return PWD_CONTEXT.hash(password)


def authenticate(
    username: str,
    password: str):
    user = User.filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):  # 1
        return False
    return user
