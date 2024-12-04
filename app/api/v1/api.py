from fastapi import APIRouter
from app.api.v1.endpoints import auth, checkout

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(checkout.router, prefix="/checkout", tags=["checkout"])
