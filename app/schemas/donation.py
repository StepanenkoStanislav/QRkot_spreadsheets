from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel, Extra, NonNegativeInt, PositiveInt, root_validator
)


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    @root_validator
    def set_invested_amount(cls, values):
        values['invested_amount'] = 0
        return values


class DonationUpdate(BaseModel):
    class Config:
        extra = Extra.forbid


class DonationDBForUser(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBForSuperuser(DonationDBForUser):
    user_id: PositiveInt
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: Optional[datetime]
