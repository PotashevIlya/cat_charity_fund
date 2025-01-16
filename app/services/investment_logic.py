from datetime import datetime

from app.models import CharityProjectAndDonationBaseModel


def distribute_investments(
    target: CharityProjectAndDonationBaseModel,
    sources: list[CharityProjectAndDonationBaseModel]
) -> tuple[
    CharityProjectAndDonationBaseModel,
    list[CharityProjectAndDonationBaseModel]
]:
    for source in sources:
        source_amount = source.full_amount - source.invested_amount
        if target.invested_amount + source_amount <= target.full_amount:
            for obj in (target, source):
                obj.invested_amount += source_amount
                if obj.invested_amount == obj.full_amount:
                    obj.fully_invested = True
                    obj.close_date = datetime.utcnow()
        else:
            source.invested_amount += (
                target.full_amount - target.invested_amount
            )
            target.invested_amount = target.full_amount
            target.fully_invested = True
            target.close_date = datetime.utcnow()
            break
    return target, sources
