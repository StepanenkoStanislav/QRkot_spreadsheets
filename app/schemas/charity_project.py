from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel, Extra, Field, NonNegativeInt, PositiveInt, root_validator
)


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    @root_validator
    def set_invested_amount(cls, values):
        values['invested_amount'] = 0
        return values


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt]


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
