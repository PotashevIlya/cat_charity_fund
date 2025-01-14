from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate, DonationBriefDB, DonationFullDB
)
from app.models import User


router = APIRouter()


@router.post(
    '/',
    response_model=DonationBriefDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    new_donation = await donation_crud.create(donation, session)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationFullDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationBriefDB],
    response_model_exclude_none=True,
    response_model_exclude={'user_id'}
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Получить список пожертвований текущего пользователя."""
    user_donations = await donation_crud.get_user_donations(
        session=session,
        user=user
    )
    return user_donations
