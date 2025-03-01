from fastapi import FastAPI
from .routes import users, index

app = FastAPI()
app.include_router(index.router)
app.include_router(users.router)

