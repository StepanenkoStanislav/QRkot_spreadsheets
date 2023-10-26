from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_charity_project_name_duplicate(
        charity_name: str,
        session: AsyncSession
) -> None:
    """Валидация уникального названия проекта."""
    if await charity_project_crud.get_by_attribute(
            'name', charity_name, session):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


def check_full_amount_not_less_than_invested_amount(
        charity_project: CharityProject,
        full_amount: int
) -> None:
    """
    Валидация, что требуемая сумма не меньше, чем уже собранные
    средства.
    """
    if full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Требуемая сумма проекта не может быть меньше уже '
                   'внесённых средств.'
        )


def check_charity_project_has_no_invested_amount(
        charity_project: CharityProject) -> None:
    """Валидация, что в проекте нет собранных средств."""
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


def check_project_not_full_invested(
        charity_project: CharityProject) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
