from datetime import datetime

from app.models import CharityProjectAndDonationBaseModel


def distribute_investments(
    target: CharityProjectAndDonationBaseModel,
    sources: list[CharityProjectAndDonationBaseModel]
) -> tuple[CharityProjectAndDonationBaseModel]:
    for source in sources:
        current_sum = source.full_amount - source.invested_amount
        required_sum = target.full_amount - target.invested_amount
        if current_sum > required_sum:
            target.invested_amount = target.full_amount
            target.fully_invested = True
            target.close_date = datetime.utcnow()
            source.invested_amount += required_sum
        elif current_sum == required_sum:
            for obj in (target, source):
                obj.invested_amount = target.full_amount
                obj.fully_invested = True
                obj.close_date = datetime.utcnow()
        else:
            source.invested_amount = source.full_amount
            source.fully_invested = True
            source.close_date = datetime.utcnow()
            target.invested_amount += current_sum
    return target, sources
