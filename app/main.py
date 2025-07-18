from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ Import CORS

from app.api import auth, users, setup

app = FastAPI()

origins = [
        "http://localhost:8000",
        "https://www.paktaxtools.com",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(setup.router, prefix="/setup", tags=["Setup"])
app.include_router(users.router, prefix="/users", tags=["Users"])
