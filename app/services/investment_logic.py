from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject



async def invest_donation(donation, session: AsyncSession):
    donation = await donation_crud.get(donation.id, session)
    all_projects = await charity_project_crud.get_sorted_by_create_date_open_projects(session)
    
    for project in all_projects:
        project_missing_sum = project.full_amount - project.invested_amount
        donation_available_sum = donation.full_amount - donation.invested_amount
        if project_missing_sum > donation_available_sum:
            setattr(project, 'invested_amount', project.invested_amount + donation.full_amount)
            setattr(donation, 'invested_amount', donation.full_amount)
            setattr(donation, 'fully_invested', True)
            setattr(donation, 'close_date', datetime.utcnow())
            session.add(project)
            session.add(donation)
            await session.commit()
            break
        elif project_missing_sum < donation_available_sum:
            setattr(donation, 'invested_amount', project_missing_sum)
            setattr(project, 'invested_amount', project.full_amount)
            setattr(project, 'fully_invested', True)
            setattr(project, 'close_date', datetime.utcnow())
            session.add(project)
            session.add(donation)
            await session.commit()
            continue
        else:
            setattr(donation, 'invested_amount', donation.full_amount)
            setattr(donation, 'fully_invested', True)
            setattr(donation, 'close_date', datetime.utcnow())
            setattr(project, 'invested_amount', project.full_amount)
            setattr(project, 'fully_invested', True)
            setattr(project, 'close_date', datetime.utcnow())
            session.add(project)
            session.add(donation)
            await session.commit()
            break
    
    

async def invest_to_project(project, session: AsyncSession):
    all_open_donations = await donation_crud.get_all_open_donations(session)
    if all_open_donations:
        for donation in all_open_donations:
            missing_sum = project.full_amount
            available_sum_in_donation = donation.full_amount - donation.invested_amount
            if available_sum_in_donation > missing_sum:
                setattr(project, 'invested_amount', project.full_amount)
                setattr(project, 'fully_invested', True)
                setattr(project, 'close_date', datetime.utcnow())
                setattr(donation, 'invested_amount', donation.invested.amount + project.full_amount)
                session.add(project)
                session.add(donation)
                await session.commit()
                break
            elif available_sum_in_donation == missing_sum:
                setattr(project, 'invested_amount', project.full_amount)
                setattr(project, 'fully_invested', True)
                setattr(project, 'close_date', datetime.utcnow())
                setattr(donation, 'invested_amount', donation.full_amount)
                setattr(donation, 'fully_invested', True)
                setattr(donation, 'close_date', datetime.utcnow())
                session.add(project)
                session.add(donation)
                await session.commit()
                break
            else:
                setattr(donation, 'invested_amount', donation.full_amount)
                setattr(donation, 'fully_invested', True)
                setattr(donation, 'close_date', datetime.utcnow())
                setattr(project, 'invested_amount', available_sum_in_donation)
                session.add(project)
                session.add(donation)
                await session.commit()
                continue

        