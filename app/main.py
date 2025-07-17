from fastapi import FastAPI
from app.api import auth, users, setup

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(setup.router, prefix="/setup", tags=["Setup"])
app.include_router(users.router, prefix="/users", tags=["Users"])
