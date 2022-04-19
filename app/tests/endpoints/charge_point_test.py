from unittest import mock
import uuid
import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.charge_point import CRUDChargePoint
from app.schemas.charge_point import ChargePointSchemaIn
from app.tests.utils.user import user_authentication_headers

pytestmark = pytest.mark.asyncio


# TODO fix creating user for testing
# async def test_charge_point_create(
#     async_client: AsyncClient,
#     db_session: AsyncSession,
# ) -> None:

#     crud_cp = CRUDChargePoint(db_session)
#     payload = {
#         "lat": -17,
#         "lng": 168,
#         "location": "Port Vila, Vanuatu",
#     }
    
#     headers = await user_authentication_headers(async_client)
#     resp = await async_client.post(
#         f"{settings.API_V1_STR}/charge_points/",
#         json=payload,
#         headers=headers,
#     )
#     assert resp.status_code == status.HTTP_201_CREATED
#     charge_point = await crud_cp.get_by_id(resp.json()["id"])

#     assert resp.json() == {
#         "id": str(charge_point.id),
#         "lat": payload["lat"],
#         "lng": payload["lng"],
#         "location": payload["location"],
#     }


async def test_charge_point_get_by_id(
    async_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    payload = {
        "lat": -17,
        "lng": 168,
        "location": "Port Vila, Vanuatu",
    }
    crud_cp = CRUDChargePoint(db_session)
    charge_point = await crud_cp.create(ChargePointSchemaIn(**payload))

    resp = await async_client.get(
        f"{settings.API_V1_STR}/charge_points/{charge_point.id}",
    )

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {
        "id": mock.ANY,
        "lat": payload["lat"],
        "lng": payload["lng"],
        "location": payload["location"],
    }


async def test_charge_point_get_by_id__fails_id(
    async_client: AsyncClient,
) -> None:
    random_uuid = uuid.uuid4()
    resp = await async_client.get(
        f"{settings.API_V1_STR}/charge_points/{random_uuid}",
    )
    assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_charge_point_nearest(
    async_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    # Vanuatu Charge Point
    payload = {
        "lat": -17,
        "lng": 168,
        "location": "Port Vila, Vanuatu",
    }
    crud_cp = CRUDChargePoint(db_session)
    cp_vu = await crud_cp.create(ChargePointSchemaIn(**payload))
    # New York Charge Point
    payload = {
        "lat": "40.7453297",
        "lng": "-73.9929523",
        "location": "Ampcontrol Office",
    }
    crud_cp = CRUDChargePoint(db_session)
    cp_ny = await crud_cp.create(ChargePointSchemaIn(**payload))
    # Find Nearest (NY)
    resp = await async_client.get(
        f"{settings.API_V1_STR}/charge_points/nearest",
        params={
            "lat": 40,
            "lng": -70,
        },
    )
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {
        "id": str(cp_ny.id),
        "lat": cp_ny.lat,
        "lng": cp_ny.lng,
        "location": cp_ny.location,
    }
    # Find Nearest - absolute values (NY)
    resp = await async_client.get(
        f"{settings.API_V1_STR}/charge_points/nearest",
        params={
            "lat": 90,
            "lng": -180,
        },
    )
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {
        "id": str(cp_ny.id),
        "lat": cp_ny.lat,
        "lng": cp_ny.lng,
        "location": cp_ny.location,
    }
    # Find Nearest (VU)
    resp = await async_client.get(
        f"{settings.API_V1_STR}/charge_points/nearest",
        params={
            "lat": -10,
            "lng": 150,
        },
    )
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {
        "id": str(cp_vu.id),
        "lat": cp_vu.lat,
        "lng": cp_vu.lng,
        "location": cp_vu.location,
    }
    # Find Nearest - absolute values(VU)
    resp = await async_client.get(
        f"{settings.API_V1_STR}/charge_points/nearest",
        params={
            "lat": -90,
            "lng": 180,
        },
    )
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {
        "id": str(cp_vu.id),
        "lat": cp_vu.lat,
        "lng": cp_vu.lng,
        "location": cp_vu.location,
    }


async def test_charge_point_nearest__fails_params(
    async_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    # null param
    resp = await async_client.get(
        f"{settings.API_V1_STR}/charge_points/nearest",
        params={
            "lat": 40,
            "lng": None,
        },
    )
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # missing param
    resp = await async_client.get(
        f"{settings.API_V1_STR}/charge_points/nearest",
        params={
            "lat": 40,
        },
    )
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # no params
    resp = await async_client.get(
        f"{settings.API_V1_STR}/charge_points/nearest",
    )
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # invalid lat value
    resp = await async_client.get(
        f"{settings.API_V1_STR}/charge_points/nearest",
        params={
            "lat": 91,
            "lng": 180,
        }
    )
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # invalid lat/lng values
    resp = await async_client.get(
        f"{settings.API_V1_STR}/charge_points/nearest",
        params={
            "lat": 1_000_000,
            "lng": 1_000_000,
        }
    )
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY