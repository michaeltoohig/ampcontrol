from typing import Type

from math import cos, asin, sqrt, pi

from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.charge_point import ChargePoint
from app.schemas.charge_point import ChargePointSchemaIn, ChargePointSchema


class CRUDChargePoint(CRUDBase[ChargePointSchemaIn, ChargePointSchema, ChargePoint]):
    @property
    def _in_schema(self) -> Type[ChargePointSchemaIn]:
        return ChargePointSchemaIn

    @property
    def _schema(self) -> Type[ChargePointSchema]:
        return ChargePointSchema

    @property
    def _table(self) -> Type[ChargePoint]:
        return ChargePoint

    def _distance(self, lat1, lng1, lat2, lng2):
        """Use Haversine formula to calculate distance between two points.
        https://en.wikipedia.org/wiki/Haversine_formula
        """
        p = 0.017453292519943295  # pi / 180 gives us factor to convert degrees to radians
        hav = 0.5 - cos((lat2 - lat1) * p) / 2 + \
            cos(lat1 * p) * cos(lat2 * p) * \
            (1 - cos((lng2 - lng1) * p)) / 2
        return 12742 * asin(sqrt(hav))  # R = 6371 km and 2 * R gives us diameter of globe

    async def find_nearest(self, lat: float, lng: float) -> ChargePointSchema:
        """Find nearest charge point to given lat/lng.
        XXX alternative approach would be implementing PostGIS nearest-neighbor search.
        """
        query = select(self._table)  # XXX major performance boost if we can filter down options early here
        results = (await self._db_session.execute(query)).scalars()
        item = min(results, key=lambda i: self._distance(i.lat, i.lng, lat, lng))
        return self._schema.from_orm(item)
