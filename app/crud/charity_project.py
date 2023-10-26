from typing import List

from sqlalchemy import true, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate
)


class CRUDCharityProject(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
    """CRUD для благотворительных проектов."""

    async def get_projects_by_completion_rate(
            self, session: AsyncSession) -> List[CharityProject]:
        charity_projects = await session.execute(
            select(self.model).where(self.model.fully_invested == true()))
        charity_projects = charity_projects.scalars().all()
        return sorted(
            charity_projects, key=lambda obj: obj.close_date - obj.create_date)


charity_project_crud = CRUDCharityProject(CharityProject)
