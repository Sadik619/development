from pydantic import BaseModel
from datetime import date
from typing import Optional


class ExpenseCreate(BaseModel):
    user_id: Optional[int] = None
    category_id: Optional[int] = None
    amount: float
    description: Optional[str] = None
    expense_date: date