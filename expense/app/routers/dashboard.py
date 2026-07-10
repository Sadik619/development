from sqlalchemy import func
from fastapi import APIRouter
from storage.database import get_db
from models.budget_model import Budget
from models.expense_model import Expense
from models.user_model import User
from models.income_model import Income
from services.querydata import QueryData

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
    user_id=current_user.id
    total_income=QueryData.total_income(db,user_id)
    total_expense=QueryData.total_expense(db,user_id)
    transaction_count=QueryData.transaction_count(db,user_id)


    return {
        "monthly_income": float(total_income),
        "monthly_expense": float(total_expense),
        "savings": float(total_income - total_expense),
        "total_transactions": transaction_count
    } if user_id else {}