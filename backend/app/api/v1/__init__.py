from fastapi import APIRouter
from . import auth, dogs, users, uploads

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dogs.router, prefix="/dogs", tags=["dogs"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
