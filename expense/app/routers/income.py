from sqlalchemy import func
from fastapi import APIRouter
from storage.database import get_db
from models.budget_model import Budget
from models.expense_model import Expense
from models.user_model import User
from models.income_model import Income

from services import querydata
from fastapi import Depends
from auth.auth import get_current_user
from sqlalchemy.orm import Session
from schemas.income_schema import IncomeCreate
router = APIRouter(
      prefix="",
      tags=["income"],
      )
@router.post("/income")
def create_income(
    payload: IncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    income = Income(
        user_id=current_user.id,
        amount=payload.amount,
        source=payload.source,
        description=payload.description,
        income_date=payload.income_date
    )

    db.add(income)
    db.commit()
    db.refresh(income)

    return {
        "message": "Income added successfully",
        "id": income.id
    }

@router.get("/income")
def get_income(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    income=querydata.Income(db,current_user.id)
    return income

    # return (
    #     db.query(Income)
    #     .filter(Income.user_id == current_user.id)
    #     .all()
    # )