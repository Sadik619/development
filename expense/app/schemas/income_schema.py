from pydantic import BaseModel
from datetime import date


class IncomeCreate(BaseModel):
    # user_id: int
    amount: float
    income_date: date
    source: str | None = None