from sqlalchemy import Column, String, Text

from app.models.abstract_models.abstract_model_invest import (
    AbstractBaseModelInvest
)


class CharityProject(AbstractBaseModelInvest):
    """Модель для благотворительных проектов."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return f'name {self.name[:20]}, ' + super().__repr__()
