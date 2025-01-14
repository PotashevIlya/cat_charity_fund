from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == project_name)
        )
        return db_charity_project_id.scalars().first()
    
    
    async def get_sorted_by_create_date_open_projects(
            self,
            session: AsyncSession
    ):
        sorted_by_create_date_open_projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested ==
                                         False).order_by(CharityProject.create_date)
        )
        return sorted_by_create_date_open_projects.scalars().all()

    async def update(self, db_obj, obj_in, session):
        if obj_in.full_amount:
            if obj_in.full_amount == db_obj.invested_amount:
                setattr(db_obj, 'fully_invested', True)
                setattr(db_obj, 'close_date', datetime.utcnow())
        return await super().update(db_obj, obj_in, session)

charity_project_crud = CRUDCharityProject(CharityProject)
