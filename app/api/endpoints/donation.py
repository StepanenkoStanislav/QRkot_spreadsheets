from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate, DonationDBForUser, DonationDBForSuperuser
)
from app.services.invest_service import invest

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDBForUser,
    response_model_exclude_none=True,
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Сделать пожертвование может любой зарегистрированный пользователь."""
    db_donation = await donation_crud.create(
        donation, session, user, commit=False)
    session.add_all(
        invest(
            db_donation,
            await charity_project_crud.get_all_uninvested(session)
        )
    )
    await session.commit()
    await session.refresh(db_donation)
    return db_donation


@router.get(
    '/my',
    response_model=List[DonationDBForUser],
    response_model_exclude_none=True,
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """
    Зарегистрированный пользователь может просматривать только свои
    пожертвования.
    """
    return await donation_crud.get_multi_by_attribute(
        'user_id', user.id, session)


@router.get(
    '/',
    response_model=List[DonationDBForSuperuser],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)):
    """Только для суперюзеров. Получает все пожертвования."""
    return await donation_crud.get_multi(session)
