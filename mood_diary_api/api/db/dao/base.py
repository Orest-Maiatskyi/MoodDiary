from typing import Union, Any

from sqlalchemy import ScalarResult, Result, CursorResult
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAOException(Exception):

    def __init__(self, cause: Union[str, Exception]) -> None:
        super().__init__(f'DAO Exception, cause:\n\n{cause}')


class DAOException(BaseDAOException):

    def __init__(self, cause: Union[str, Exception]) -> None:
        super().__init__(cause)


class Base:

    @staticmethod
    async def execute(a_session: AsyncSession, stmt) -> Result[Any] | CursorResult[Any]:
        try:
            return await a_session.execute(stmt)
        except Exception as e:
            raise DAOException(e)

    @staticmethod
    async def a_scalar(a_session: AsyncSession, stmt) -> Any:
        try:
            return await a_session.scalar(stmt)
        except Exception as e:
            raise DAOException(e)

    @staticmethod
    async def a_scalars(a_session: AsyncSession, stmt) -> ScalarResult[Any]:
        try:
            return await a_session.scalars(stmt)
        except Exception as e:
            raise DAOException(e)
