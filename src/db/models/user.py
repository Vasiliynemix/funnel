from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import func, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.bot.structures.role import Role
from src.db.models import Base


class User(Base):
    user_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True, nullable=False)
    user_name: Mapped[str] = mapped_column(sa.Text, unique=False, nullable=True)

    language_code: Mapped[str] = mapped_column(sa.Text, unique=False, nullable=True)

    role: Mapped[Role] = mapped_column(sa.Enum(Role), default=Role.USER)

    waiting_for_continue: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )

    state: Mapped[int] = mapped_column(sa.Integer, default=0, nullable=False)
    count_spam: Mapped[int] = mapped_column(sa.Integer, default=0, nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
