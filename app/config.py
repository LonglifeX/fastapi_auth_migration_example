from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    app_name: str
    admin_email: str
    app_version: str
    jwt_secret_key: str

    class Config:
        env_file: str = os.path.join(os.path.dirname(__file__), ".." , ".env")


settings = Settings()
