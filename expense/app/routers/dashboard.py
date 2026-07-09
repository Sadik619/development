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
      tags=["dashboard"],
      )
@router.get("/dashboard")
def dashboard(
    month: int,
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    total_income = (
        db.query(func.coalesce(func.sum(Income.amount), 0))
        .filter(Income.user_id == current_user.id)
        .scalar()
    )

    total_expense = (
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.user_id == current_user.id)
        .scalar()
    )

    transaction_count = (
        db.query(Expense)
        .filter(Expense.user_id == current_user.id)
        .count()
    )

    return {
        "monthly_income": float(total_income),
        "monthly_expense": float(total_expense),
        "savings": float(total_income - total_expense),
        "total_transactions": transaction_count
    }