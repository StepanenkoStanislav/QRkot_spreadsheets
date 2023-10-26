from datetime import datetime
from typing import Iterable, List

from app.models.abstract_models.abstract_model_invest import (
    AbstractBaseModelInvest
)


def invest(
        target: AbstractBaseModelInvest,
        sources: Iterable[AbstractBaseModelInvest]
) -> List[AbstractBaseModelInvest]:
    """Сервис для инвестирования пожертвований в проекты."""
    changed = []
    for source in sources:
        changed.append(source)
        investment = min(target.full_amount - target.invested_amount,
                         source.full_amount - source.invested_amount)
        for obj in target, source:
            obj.invested_amount += investment
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()
        if target.fully_invested:
            break
    return changed
