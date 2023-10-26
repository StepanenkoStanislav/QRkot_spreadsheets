from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.abstract_models.abstract_model_invest import (
    AbstractBaseModelInvest
)


class Donation(AbstractBaseModelInvest):
    """Модель для пожертвований."""
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)

    def __repr__(self) -> str:
        return (f'user_id {self.user_id}, '
                f'comment {self.comment[:20]}' + super().__repr__())
