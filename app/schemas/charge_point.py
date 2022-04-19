import uuid
from typing import Optional

from pydantic import Field

from app.schemas.base import BaseSchema


class ChargePointSchemaBase(BaseSchema):
    lat: Optional[float] = None
    lng: Optional[float] = None
    location: Optional[str] = None


class ChargePointSchemaUpdate(ChargePointSchemaBase):
    pass


class ChargePointSchemaIn(ChargePointSchemaBase):
    lat: float
    lng: float
    location: str


class ChargePointSchema(ChargePointSchemaBase):
    id: uuid.UUID


class ChargePointSchemaOut(ChargePointSchema):
    pass