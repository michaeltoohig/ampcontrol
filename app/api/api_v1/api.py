from fastapi import APIRouter
from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, charge_points

api_router = APIRouter()

api_router.include_router(auth.auth_router, prefix="/auth/jwt", tags=["auth"])
api_router.include_router(auth.register_router, prefix="/auth", tags=["auth"])
api_router.include_router(auth.reset_password_router, prefix="/auth", tags=["auth"])
api_router.include_router(auth.verify_router, prefix="/auth", tags=["auth"])

api_router.include_router(charge_points.router, prefix="/charge_points", tags=["charge_points"])
