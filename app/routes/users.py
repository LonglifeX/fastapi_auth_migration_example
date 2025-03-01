from datetime import timedelta
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from ..auth import Token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..models.user import User
from ..dependencies import SessionDep, get_current_active_user, auth
from fastapi import status

router = APIRouter()


@router.get("/user/", response_model=List[User])
async def read_users(session: SessionDep, my_user: Annotated[User, Depends(get_current_active_user)]):
    user = session.exec(select(User)).all()
    return user


@router.get("/user/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)], ):
    return current_user


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], ) -> Token:
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
