from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.api.validators import (
    check_charity_project_exists, check_charity_project_is_open,
    check_charity_project_investments, check_full_amount_update,
    check_charity_project_name_duplicate
)
from app.services.investment_logic import distribute_open_donations_among_project

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_charity_project_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project,
        session
    )
    return await distribute_open_donations_among_project(new_charity_project, session)


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Для любого пользователя."""
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров"""
    charity_project = await check_charity_project_exists(project_id, session)
    charity_project = await check_charity_project_is_open(project_id, session)
    if obj_in.full_amount:
        await check_full_amount_update(charity_project.invested_amount, obj_in.full_amount)
    if obj_in.name:
        await check_charity_project_name_duplicate(obj_in.name, session)
    charity_project = await charity_project_crud.update(charity_project, obj_in, session)
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    charity_project = await check_charity_project_is_open(
        project_id, session
    )
    charity_project = await check_charity_project_investments(
        project_id, session
    )
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
