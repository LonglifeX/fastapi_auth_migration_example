from datetime import datetime, timezone, timedelta
from typing import Annotated
import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel
from .config import settings
from .models.user import User
from sqlmodel import select
from .db import get_session

SECRET_KEY = settings.jwt_secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Auth:

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def get_password_hash(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def get_user(username: str):
        session = next(get_session())
        db_user = session.exec(select(User).where(User.username == username)).first()
        if db_user:
            return db_user
        return None

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)], ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        user = self.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
