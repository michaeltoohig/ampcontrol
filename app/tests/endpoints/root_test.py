import pytest
from httpx import AsyncClient
from fastapi import status

pytestmark = pytest.mark.asyncio


async def test_main(async_client: AsyncClient) -> None:
    resp = await async_client.get("/")

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["status"] == "ok"
