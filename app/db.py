from sqlmodel import Session, create_engine
# add models here to create them in create_db_and tables
import os
from .models import user

sqlite_file_name = os.path.join(os.path.dirname(__file__), "..", "database.db")
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session
