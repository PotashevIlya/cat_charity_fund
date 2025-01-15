from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_by_name(
            self,
            project_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        charity_project = await session.execute(
            select(CharityProject).where(
                CharityProject.name == project_name)
        )
        return charity_project.scalars().first()

    async def get_all_open_projects(
            self,
            session: AsyncSession
    ):
        open_projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested == 0
                                         ).order_by(CharityProject.create_date)
        )
        return open_projects.scalars().all()

    async def update(self, db_obj, obj_in, session):
        if obj_in.full_amount:
            if obj_in.full_amount == db_obj.invested_amount:
                setattr(db_obj, 'fully_invested', True)
                setattr(db_obj, 'close_date', datetime.utcnow())
        return await super().update(db_obj, obj_in, session)


charity_project_crud = CRUDCharityProject(CharityProject)
