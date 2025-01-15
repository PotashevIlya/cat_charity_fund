from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


def set_close_attributes_to_object(
        object: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    """Устанавливаем атрибуты, означающие, что проект или донат закрыты."""
    setattr(object, 'invested_amount', object.full_amount)
    setattr(object, 'fully_invested', True)
    setattr(object, 'close_date', datetime.utcnow())
    return object


def set_invested_amount_attribute_to_object(
        object: Union[CharityProject, Donation],
        amount: int
) -> Union[CharityProject, Donation]:
    """Устанавливаем вложенную сумму для открытого проекта или доната."""
    setattr(object, 'invested_amount', object.invested_amount + amount)
    return object


async def distribute_open_donations_among_new_project(
        project: CharityProject,
        session: AsyncSession
) -> CharityProject:
    """Процесс распределения денег при создании нового проекта."""
    open_donations = await donation_crud.get_all_open_donations(session)
    if not open_donations:
        return project
    for donation in open_donations:
        missing_project_sum = project.full_amount - project.invested_amount
        donation_free_sum = donation.full_amount - donation.invested_amount
        if donation_free_sum > missing_project_sum:
            session.add(set_close_attributes_to_object(project))
            session.add(set_invested_amount_attribute_to_object(
                donation,
                missing_project_sum)
            )
            break
        if donation_free_sum < missing_project_sum:
            session.add(set_close_attributes_to_object(donation))
            session.add(set_invested_amount_attribute_to_object(
                project,
                donation_free_sum)
            )
            continue
        if donation_free_sum == missing_project_sum:
            session.add(set_close_attributes_to_object(project))
            session.add(set_close_attributes_to_object(donation))
            break
    await session.commit()
    await session.refresh(project)
    return project


async def distribute_new_donation_among_projects(
        donation: Donation,
        session: AsyncSession
) -> Donation:
    """Процесс распределения денег при создании нового доната."""
    open_projects = await charity_project_crud.get_all_open_projects(session)
    if not open_projects:
        return donation
    for project in open_projects:
        missing_project_sum = project.full_amount - project.invested_amount
        donation_free_sum = donation.full_amount - donation.invested_amount
        if donation_free_sum < missing_project_sum:
            session.add(set_close_attributes_to_object(donation))
            session.add(set_invested_amount_attribute_to_object(
                project,
                donation_free_sum)
            )
            break
        if donation_free_sum > missing_project_sum:
            session.add(set_close_attributes_to_object(project))
            session.add(set_invested_amount_attribute_to_object(
                donation,
                missing_project_sum)
            )
            continue
        if donation_free_sum == missing_project_sum:
            session.add(set_close_attributes_to_object(project))
            session.add(set_close_attributes_to_object(donation))
            break
    await session.commit()
    await session.refresh(donation)
    return donation
