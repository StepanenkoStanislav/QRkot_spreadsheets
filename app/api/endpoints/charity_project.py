from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_name_duplicate,
    check_charity_project_has_no_invested_amount,
    check_full_amount_not_less_than_invested_amount,
    check_project_not_full_invested
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.invest_service import invest

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров. Создает благотворительный проект."""
    await check_charity_project_name_duplicate(charity_project.name, session)
    db_charity_project = await charity_project_crud.create(
        charity_project, session, commit=False)
    session.add_all(
        invest(
            db_charity_project,
            await donation_crud.get_all_uninvested(session)
        )
    )
    await session.commit()
    await session.refresh(db_charity_project)
    return db_charity_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    """Получает все благотворительные проекты."""
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def parially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров. Можно менять название и описание
    существующего проекта, устанавливать для него новую требуюмую сумму
    (но не меньше уже внесённой).
    """
    db_charity_project = await charity_project_crud.get(
        charity_project_id, session)
    check_project_not_full_invested(db_charity_project)
    if obj_in.name:
        await check_charity_project_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        check_full_amount_not_less_than_invested_amount(
            db_charity_project, obj_in.full_amount)
    return await charity_project_crud.update(
        db_charity_project, obj_in, session)


@router.delete(
    '/{charity_project_id}',
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров. Можно удалить проект, если в него не было
    внесено средств.
    """
    db_charity_project = await charity_project_crud.get(
        charity_project_id, session)
    check_charity_project_has_no_invested_amount(db_charity_project)
    return await charity_project_crud.remove(db_charity_project, session)
