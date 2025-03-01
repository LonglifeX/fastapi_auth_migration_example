from fastapi import APIRouter

from ..config import settings

router = APIRouter()


@router.get("/")
async def root():
    welcome_str = f"Welcome {settings.app_name}!"
    return {
        "message": welcome_str,
        "app_version": settings.app_version
    }
