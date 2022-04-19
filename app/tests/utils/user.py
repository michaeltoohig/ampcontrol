from typing import Dict
import contextlib
from app.models.user import User

from httpx import AsyncClient
from fastapi import status

from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string


async def create_user(
    async_client: AsyncClient,
    email: str = None,
    password: str = None,
) -> User:
    if not email:
        email = random_email()
    if not password:
        password = random_lower_string()
    data = {
        "email": email,
        "password": password,
        "is_active": True,
        "is_superuser": False,
        "is_verified": False
        }
    resp = await async_client.post(f"{settings.API_V1_STR}/auth/register", json=data)
    user = resp.json()
    return user


async def user_authentication_headers(
    async_client: AsyncClient,
) -> Dict[str, str]:
    email = random_email()
    password = random_lower_string()
    await create_user(async_client, email, password)
    data = {"username": email, "password": password}

    resp = await async_client.post(f"{settings.API_V1_STR}/auth/jwt/login", json=data)
    assert resp.status_code == status.HTTP_200_OK
    response = resp.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
