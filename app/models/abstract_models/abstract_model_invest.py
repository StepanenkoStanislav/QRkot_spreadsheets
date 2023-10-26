from datetime import datetime

from sqlalchemy import Boolean, Column, CheckConstraint, DateTime, Integer

from app.core.db import Base


class AbstractBaseModelInvest(Base):
    """Добавляет общие поля к моделям CharityProject и Donation."""
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount <= full_amount')
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    close_date = Column(DateTime, nullable=True, default=None)

    def __repr__(self) -> str:
        return (f'full_amount {self.full_amount}, '
                f'invested_amount {self.invested_amount}, '
                f'fully_invested {self.fully_invested}, '
                f'created {self.create_date}')
