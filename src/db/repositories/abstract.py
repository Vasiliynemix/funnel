import abc
from typing import Generic, TypeVar, Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Base

AbstractModel = TypeVar("AbstractModel")


class Repository(Generic[AbstractModel]):
    type_model: type[Base]
    session: AsyncSession

    def __init__(self, type_model: type[Base], session: AsyncSession):
        self.type_model = type_model
        self.session = session

    async def get(self, ident: int | str) -> AbstractModel:
        """Get ONE model from database this Primary Key.
        :param ident: Primary Key which need to find entry in database
        :return:
        """
        return await self.session.get(entity=self.type_model, ident=ident)

    # async def get_by_where(self, condition) -> AbstractModel | None:
    #     """Get ONE model from database this condition.
    #     :param condition: example (User.user_id == <user_id>)
    #     :return:
    #     """
    #     statement = select(self.type_model).where(condition).limit(1)
    #
    #     return (await self.session.execute(statement)).one_or_none()

    async def get_many(
        self, condition, limit: int = 100, order_by=None
    ) -> Sequence[Base]:
        """get MANY models from database this condition.
        :param condition: example (User.user_id == <user_id>)
        :param limit: (Optional, default = 100) Limit count of result.
        :param order_by: (Optional, default = None) Order by column.
        :return:
        """
        statement = select(self.type_model).where(condition).limit(limit)
        if order_by:
            statement = statement.order_by(order_by)

        return (await self.session.scalars(statement)).all()

    async def delete(self, condition) -> None:
        statement = delete(self.type_model).where(condition)
        await self.session.execute(statement)

    @abc.abstractmethod
    async def new(self, *args, **kwargs) -> None:
        """Add new row of model to the database
        :param args:
        :param kwargs:
        :return:
        """
        pass
