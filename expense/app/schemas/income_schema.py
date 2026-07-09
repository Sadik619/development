from pydantic import BaseModel
from datetime import date


class IncomeCreate(BaseModel):
    source: str
    amount: float
    date: date
    description: str | None = None