from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


async def distribute_open_donations_among_project(project: CharityProject, session: AsyncSession) -> CharityProject:
    open_donations = await donation_crud.get_all_open_donations(session)
    if not open_donations:
        return project
    for donation in open_donations:
        missing_project_sum = missing_project_sum = project.full_amount - project.invested_amount
        donation_awailiable_sum = donation.full_amount - donation.invested_amount
        if donation_awailiable_sum > missing_project_sum:
            setattr(project, 'invested_amount', project.full_amount)
            setattr(project, 'fully_invested', True)
            setattr(project, 'close_date', datetime.utcnow())
            setattr(donation, 'invested_amount',
                    donation.invested_amount + missing_project_sum)
            session.add(project)
            session.add(donation)
            break
        if donation_awailiable_sum < missing_project_sum:
            setattr(project, 'invested_amount',
                    project.invested_amount + donation_awailiable_sum)
            setattr(donation, 'invested_amount', donation.full_amount)
            setattr(donation, 'fully_invested', True)
            setattr(donation, 'close_date', datetime.utcnow())
            session.add(project)
            session.add(donation)
            continue
        if donation_awailiable_sum == missing_project_sum:
            setattr(donation, 'invested_amount', donation.full_amount)
            setattr(donation, 'fully_invested', True)
            setattr(donation, 'close_date', datetime.utcnow())
            setattr(project, 'invested_amount', project.full_amount)
            setattr(project, 'fully_invested', True)
            setattr(project, 'close_date', datetime.utcnow())
            session.add(project)
            session.add(donation)
            break
    await session.commit()
    await session.refresh(project)
    return project


async def distribute_new_donation_among_projects(donation: Donation, session: AsyncSession) -> Donation:
    open_projects = await charity_project_crud.get_sorted_by_create_date_open_projects(session)
    if not open_projects:
        return donation
    for project in open_projects:
        missing_project_sum = project.full_amount - project.invested_amount
        donation_awailiable_sum = donation.full_amount - donation.invested_amount
        if donation_awailiable_sum < missing_project_sum:
            setattr(project, 'invested_amount',
                    project.invested_amount + donation_awailiable_sum)
            setattr(donation, 'invested_amount', donation.full_amount)
            setattr(donation, 'fully_invested', True)
            setattr(donation, 'close_date', datetime.utcnow())
            session.add(project)
            session.add(donation)
            break
        if donation_awailiable_sum > missing_project_sum:
            setattr(project, 'invested_amount', project.full_amount)
            setattr(project, 'fully_invested', True)
            setattr(project, 'close_date', datetime.utcnow())
            setattr(donation, 'invested_amount',
                    donation.invested_amount + missing_project_sum)
            session.add(project)
            session.add(donation)
            continue
        if donation_awailiable_sum == missing_project_sum:
            setattr(donation, 'invested_amount', donation.full_amount)
            setattr(donation, 'fully_invested', True)
            setattr(donation, 'close_date', datetime.utcnow())
            setattr(project, 'invested_amount', project.full_amount)
            setattr(project, 'fully_invested', True)
            setattr(project, 'close_date', datetime.utcnow())
            session.add(project)
            session.add(donation)
            break
    await session.commit()
    await session.refresh(donation)
    return donation
