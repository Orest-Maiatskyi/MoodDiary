from contextlib import asynccontextmanager
from typing import Optional, Any, AsyncGenerator, Union

from pydantic import MySQLDsn
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from .model import BaseModel


class DBBaseException(Exception):

    def __init__(self, cause: Union[str, Exception]) -> None:
        super().__init__(f'DB Exception, cause:\n\n{cause}')


class DBException(DBBaseException):

    def __init__(self, cause: Union[str, Exception]):
        super().__init__(cause)


class DB:
    __instance: Optional['DB'] = None

    def __init__(self, dsn: MySQLDsn, **engine_params: Any) -> None:
        if DB.__instance is not None:
            raise DBException('The database has already been initialized!')
        DB.__instance = self

        try:
            self.__a_engine = create_async_engine(
                dsn.encoded_string(),
                **engine_params,
            )

            self.__a_sessionmaker = async_sessionmaker(
                bind=self.__a_engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )
        except Exception as e:
            raise DBException(e)

    @staticmethod
    def get() -> 'DB':
        if DB.__instance is None:
            raise DBException('The database is not initialized!')
        return DB.__instance

    @staticmethod
    @asynccontextmanager
    async def get_a_session() -> AsyncGenerator[AsyncSession, None]:
        if DB.__instance is None:
            raise DBException('The database is not initialized!')

        async with DB.__instance.__a_sessionmaker() as a_session:
            try:
                yield a_session
            except Exception as e:
                await a_session.rollback()
                raise DBException(e)
            finally:
                await a_session.close()

    @staticmethod
    async def create_all() -> None:
        if DB.__instance is None:
            raise DBException('The database is not initialized!')

        async with DB.__instance.__a_engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

    @staticmethod
    async def drop_all() -> None:
        if DB.__instance is None:
            raise DBException('The database is not initialized!')

        async with DB.__instance.__a_engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
