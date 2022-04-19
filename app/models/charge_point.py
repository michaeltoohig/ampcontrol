from sqlalchemy import Column, Float, String

from app.db.base_class import Base


class ChargePoint(Base):
    __tablename__ = "charge_point"

    lat = Column("longitude", Float, nullable=False)
    lng = Column("latitude", Float, nullable=False)
    location = Column(String, nullable=False)
