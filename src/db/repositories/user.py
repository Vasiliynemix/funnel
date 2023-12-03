from datetime import datetime, timedelta

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.role import Role
from src.configuration import conf
from src.db.models import User
from src.db.repositories.abstract import Repository


class UserRepo(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(type_model=User, session=session)

    async def new(
        self,
        user_id: int,
        user_name: str | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        language_code: str | None = None,
        is_premium: bool | None = False,
        role: Role | None = Role.USER,
    ) -> None:
        await self.session.merge(
            User(
                user_id=user_id,
                user_name=user_name,
                language_code=language_code,
                role=role,
            )
        )

    async def get_by_user_id(self, user_id: int):
        return await self.session.scalar(select(User).where(User.user_id == user_id))

    async def get_by_role(self):
        moderators = await self.session.scalars(
            select(User).filter(User.role == Role.ADMINISTRATOR)
        )
        return moderators.all()

    async def update_role(self, user_id: int) -> bool:
        if user_id == conf.admin.admin_id:
            user = await self.get_by_user_id(user_id=user_id)
            user.role = Role.ADMINISTRATOR
            await self.session.commit()
        return True

    async def update_at(self, user_id: int) -> bool:
        user = await self.get_by_user_id(user_id=user_id)
        if user is not None:
            user.updated_at = datetime.now()
            await self.session.commit()
        return True

    async def update_state(self, user_id: int, state: int) -> bool:
        user = await self.get_by_user_id(user_id=user_id)
        user.state = state
        await self.session.commit()
        return True

    async def get_users_for_answer(self, delta_hours: int, count_spam: int):
        users = await self.session.scalars(
            select(User)
            .where(User.count_spam == count_spam)
            .where(User.created_at > datetime.now() - timedelta(days=90))
            .where(User.updated_at < datetime.now() - timedelta(hours=delta_hours))
        )
        return users.all()

    async def update_count_spam(self, user_id: int) -> bool:
        user = await self.get_by_user_id(user_id=user_id)
        user.count_spam += 1
        await self.session.commit()
        return True

    async def check_state(self, user_id: int, state: int) -> User | None:
        return await self.session.scalar(
            select(User).where(User.user_id == user_id).where(User.state == state)
        )

    async def get_all(self):
        users = await self.session.scalars(select(User))
        return users.all()

    async def update_end_at(self, user_id: int) -> bool:
        user = await self.get_by_user_id(user_id=user_id)
        user.end_funnel_at = datetime.now()
        await self.session.commit()
        return True

    async def delete_users(self) -> bool:
        await self.session.execute(delete(User))
        await self.session.commit()
        return True
