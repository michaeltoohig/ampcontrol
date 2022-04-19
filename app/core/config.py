from typing import Any
from typing import Dict
from typing import Optional

from pydantic import BaseSettings, EmailStr
from pydantic import PostgresDsn
from pydantic import validator


class Config(BaseSettings):
    SERVICE_NAME: str
    SERVICE_SLUG: str
    SECRET_KEY: str
    API_V1_STR: str = '/api/v1'

    ACCESS_TOKEN_EXPIRE_SECONDS: int = 3600

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_DATABASE_ECHO: bool = False

    @validator('SQLALCHEMY_DATABASE_URI', pre=True)
    def assemble_db_connection(
        cls,
        v: Optional[str],
        values: Dict[str, Any],
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_SERVER'),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    @property
    def ASYNC_SQLALCHEMY_DATABASE_URI(self) -> Optional[str]:
        return (
            self.SQLALCHEMY_DATABASE_URI.replace(
                'postgresql://', 'postgresql+asyncpg://',
            )
            if self.SQLALCHEMY_DATABASE_URI
            else self.SQLALCHEMY_DATABASE_URI
        )

    class Config:
        case_sensitive = True


settings = Config()
