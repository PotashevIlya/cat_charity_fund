from datetime import datetime

from app.models import InvestmentBaseModel


def distribute_investments(
    target: InvestmentBaseModel,
    sources: list[InvestmentBaseModel]
) -> list[InvestmentBaseModel]:
    changed_objects = []
    for source in sources:
        ready_to_accept = target.full_amount - target.invested_amount
        if ready_to_accept == 0:
            break
        ready_to_give = source.full_amount - source.invested_amount
        trans_amount = min(ready_to_accept, ready_to_give)
        for obj in (target, source):
            obj.invested_amount += trans_amount
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.utcnow()
            changed_objects.append(obj)
    return changed_objects
