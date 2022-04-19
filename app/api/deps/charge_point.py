from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.db import get_db
from app.crud.charge_point import CRUDChargePoint
from app.db.exceptions import DoesNotExist
from app.schemas.charge_point import ChargePointSchema


async def get_charge_point_or_404(
        db: AsyncSession = Depends(get_db),
        *,
        id: UUID,
    ) -> ChargePointSchema:
        crud_cp = CRUDChargePoint(db)
        try:
            return await crud_cp.get_by_id(id)
        except DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
