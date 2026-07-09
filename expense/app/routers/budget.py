from sqlalchemy import func
from fastapi import APIRouter
from storage.database import get_db
from models.budget_model import Budget
from models.expense_model import Expense
from models.user_model import User

from fastapi import Depends
from auth.auth import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(
      prefix="",
      tags=["budget"],
      )
@router.get("/budget")
def get_budget(
    month: int,
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    budget = (
        db.query(Budget)
        .filter(
            Budget.user_id == current_user.id,
            Budget.month == month,
            Budget.year == year
        )
        .first()
    )

    spent = (
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(
            Expense.user_id == current_user.id
        )
        .scalar()
    )

    return {
        "budget_amount": budget.budget_amount,
        "spent_amount": spent,
        "remaining_amount": budget.budget_amount - spent
    }