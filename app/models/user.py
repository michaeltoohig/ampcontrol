from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.db.base_class import Base


class User(Base, SQLAlchemyBaseUserTable):
    pass