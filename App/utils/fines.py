from datetime import date
from decimal import Decimal


def calculate_overdue_fine(due_date: date, return_date: date, daily_rate: Decimal = Decimal("2.00")) -> Decimal:
    if return_date <= due_date:
        return Decimal("0.00")
    days_overdue = (return_date - due_date).days
    return (daily_rate * days_overdue).quantize(Decimal("0.01"))
