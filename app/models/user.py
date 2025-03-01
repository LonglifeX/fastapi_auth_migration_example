from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    full_name: str
    hashed_password: str
    disabled: bool
    admin: bool = False
