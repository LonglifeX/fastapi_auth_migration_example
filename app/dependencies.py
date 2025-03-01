from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import Session
from app.db import get_session
from .auth import Auth
from .models.user import User

SessionDep = Annotated[Session, Depends(get_session)]
auth = Auth()


async def get_current_active_user(current_user: Annotated[User, Depends(auth.get_current_user)], ):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
