from pydantic import BaseModel


class BudgetCreate(BaseModel):
    month: int
    year: int
    budget_amount: float


class BudgetResponse(BaseModel):
    id: int
    user_id: int
    month: int
    year: int
    budget_amount: float

    class Config:
        from_attributes = True