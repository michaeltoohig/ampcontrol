from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.deps.db import get_db
from app.api.deps.user import current_active_user
from app.api.deps.charge_point import get_charge_point_or_404
from app.crud.charge_point import CRUDChargePoint
from app.models.user import User
from app.schemas.charge_point import ChargePointSchema, ChargePointSchemaOut, ChargePointSchemaIn, ChargePointSchemaUpdate

router = APIRouter()


@router.get("/nearest", status_code=status.HTTP_200_OK, response_model=ChargePointSchemaOut)
async def find_nearest_charge_point(
    db: AsyncSession = Depends(get_db),
    *,
    lat: float = Query(...),
    lng: float = Query(...),
) -> ChargePointSchemaOut:
    crud_cp = CRUDChargePoint(db)
    charge_point = await crud_cp.find_nearest(lat, lng)
    return ChargePointSchemaOut(**charge_point.dict())


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ChargePointSchemaOut,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user.",
        },
    },
)
async def create_charge_point(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_active_user),
    *,
    payload: ChargePointSchemaIn = Body(
        ...,
        example={
            "lat": "40.7453297",
            "lng": "-73.9929523",
            "location": "Ampcontrol Office",
        },
    ),
) -> ChargePointSchemaOut:
    crud_cp = CRUDChargePoint(db)
    charge_point = await crud_cp.create(payload)
    return ChargePointSchemaOut(**charge_point.dict())


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[ChargePointSchemaOut],
)
async def read_charge_points(
    db: AsyncSession = Depends(get_db),
    *,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
) -> List[ChargePointSchemaOut]:
    crud_cp = CRUDChargePoint(db)
    charge_points = await crud_cp.get_multi(skip=skip, limit=limit)
    return [ChargePointSchemaOut(**cp.dict()) for cp in charge_points]


@router.get(
    "/{id:uuid}",
    status_code=status.HTTP_200_OK,
    response_model=ChargePointSchemaOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "The charge point does not exist.",
        },
    },
)
async def read_charge_point(
    charge_point: ChargePointSchema = Depends(get_charge_point_or_404),
) -> ChargePointSchemaOut:
    return ChargePointSchemaOut(**charge_point.dict())


@router.put(
    "/{id:uuid}",
    status_code=status.HTTP_200_OK,
    response_model=ChargePointSchemaOut,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The charge point does not exist.",
        },
    },
)
async def update_charge_point(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_active_user),
    *,
    charge_point: ChargePointSchema = Depends(get_charge_point_or_404),
    payload: ChargePointSchemaUpdate = Body(
        ...,
        example={
            "lat": "40.7453297",
            "lng": "-73.9929523",
            "location": "Ampcontrol Office",
        },
    ),
) -> ChargePointSchemaOut:
    crud_cp = CRUDChargePoint(db)
    charge_point = await crud_cp.update(charge_point.id, payload)
    return ChargePointSchemaOut(**charge_point.dict())


@router.delete(
    "/{id:uuid}",
    status_code=status.HTTP_200_OK,
    response_model=ChargePointSchemaOut,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The charge point does not exist.",
        },
    },
)
async def remove_charge_point(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_active_user),
    *,
    charge_point: ChargePointSchema = Depends(get_charge_point_or_404),
) -> ChargePointSchemaOut:
    crud_cp = CRUDChargePoint(db)
    charge_point = await crud_cp.delete(charge_point.id)
    return ChargePointSchemaOut(**charge_point.dict())
