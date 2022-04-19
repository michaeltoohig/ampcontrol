import abc
from typing import Generic, List, Type, TypeVar
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.exceptions import DoesNotExist
from app.schemas.base import BaseSchema

IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
SCHEMA = TypeVar("SCHEMA", bound=BaseSchema)
TABLE = TypeVar("TABLE")


class CRUDBase(Generic[TABLE, IN_SCHEMA, SCHEMA], metaclass=abc.ABCMeta):
    def __init__(self, db_session: AsyncSession, *args, **kwargs) -> None:
        self._db_session: AsyncSession = db_session

    @property
    @abc.abstractmethod
    def _table(self) -> Type[TABLE]:
        ...

    @property
    @abc.abstractmethod
    def _schema(self) -> Type[SCHEMA]:
        ...

    async def create(self, in_schema: IN_SCHEMA) -> SCHEMA:
        item = self._table(id=uuid4(), **in_schema.dict())
        self._db_session.add(item)
        await self._db_session.commit()
        return self._schema.from_orm(item)

    async def update(self, item_id: UUID, update_schema) -> SCHEMA:
        item = await self._get_one(item_id)
        for key, value in update_schema.dict(exclude_unset=True).items():
            setattr(item, key, value)
        self._db_session.add(item)
        await self._db_session.commit()
        return self._schema.from_orm(item)

    async def delete(self, item_id: UUID) -> SCHEMA:
        item = await self._get_one(item_id)
        await self._db_session.delete(item)
        await self._db_session.commit()
        return self._schema.from_orm(item)

    async def _get_one(self, item_id: UUID):
        query = select(self._table).filter(self._table.id == item_id)
        try:
            item = (await self._db_session.execute(query)).scalar_one()
        except NoResultFound:
            item = None
        return item

    async def get_by_id(self, item_id: UUID) -> SCHEMA:
        item = await self._get_one(item_id)
        if not item:
            raise DoesNotExist(
                f"{self._table.__name__}<id:{item_id}> does not exist"
            )
        return self._schema.from_orm(item)

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[SCHEMA]:
        query = (
            select(self._table)
            .offset(skip)
            .limit(limit)
        )
        results = (await self._db_session.execute(query)).scalars()
        return (self._schema.from_orm(item) for item in results)
