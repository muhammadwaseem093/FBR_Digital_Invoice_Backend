from fastapi import FastAPI
from app.api import auth, users, credentials, invoices

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(credentials.router, prefix="/credentials", tags=["Credentials"])
app.include_router(invoices.router, prefix="/invoices", tags=["Invoices"])

