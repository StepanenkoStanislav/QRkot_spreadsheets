from datetime import datetime
from typing import Generic, Optional, List, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

CreateSchema = TypeVar('CreateSchema', bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)
ModelType = TypeVar('ModelType', bound=Base)


class CRUDBase(Generic[ModelType, CreateSchema, UpdateSchema]):
    """Общий CRUD для моделей."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
            self, obj_id: int, session: AsyncSession) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_by_attribute(
            self,
            attr_name: str,
            attr_value: Union[str, int, bool, datetime],
            session: AsyncSession
    ) -> ModelType:
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.scalars().first()

    async def get_multi_by_attribute(
            self,
            attr_name: str,
            attr_value: Union[str, int, bool, datetime],
            session: AsyncSession,
    ) -> List[ModelType]:
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value))
        return db_obj.scalars().all()

    async def get_all_uninvested(
            self, session: AsyncSession) -> List[ModelType]:
        """
        Получает все неивестированные объекты модели, начиная с
        самых ранних.
        """
        db_objects = await session.execute(
            select(self.model).where(
                self.model.fully_invested == false()).order_by(
                self.model.create_date)
        )
        return db_objects.scalars().all()

    async def get_multi(self, session: AsyncSession) -> List[ModelType]:
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def create(
            self,
            obj_in: CreateSchema,
            session: AsyncSession,
            user: Optional[User] = None,
            commit: bool = True
    ) -> ModelType:
        obj_in_data = obj_in.dict()
        if user:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj: ModelType,
            obj_in: UpdateSchema,
            session: AsyncSession
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True, exclude_none=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self, db_obj: ModelType, session: AsyncSession) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
