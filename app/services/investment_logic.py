from datetime import datetime

from app.models import CharityProjectAndDonationBaseModel


def calc_trans_amount(target, source):
    ready_to_accept = target.full_amount - target.invested_amount
    ready_to_give = source.full_amount - source.invested_amount
    if ready_to_accept > ready_to_give:
        return ready_to_give
    return ready_to_accept


def distribute_investments(
    target: CharityProjectAndDonationBaseModel,
    sources: list[CharityProjectAndDonationBaseModel]
) -> list[CharityProjectAndDonationBaseModel]:
    for source in sources:
        trans_amount = calc_trans_amount(target, source)
        for obj in (target, source):
            obj.invested_amount += trans_amount
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.utcnow()
    return sources
