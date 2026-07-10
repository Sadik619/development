from sqlalchemy import func
from fastapi import APIRouter
from storage.database import get_db
from models.budget_model import Budget
from models.expense_model import Expense
from models.user_model import User

from fastapi import Depends
from auth.auth import get_current_user
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from storage.database import get_db
from models.budget_model import Budget
from schemas.budget import BudgetCreate, BudgetResponse

router = APIRouter(
    prefix="/budget",
    tags=["Budget"]
)


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
    "budget_amount": budget.amount,
    "spent_amount": spent,
    "remaining_amount": budget.amount - spent
} if budget else {}



@router.post("/", response_model=BudgetResponse)
def create_budget(
    payload: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Example: assigning budget to user with id=1
    # Replace this with current_user.id when authentication is added
    user_id = current_user.id

    existing = db.query(Budget).filter(
        Budget.user_id == user_id,
        Budget.month == payload.month,
        Budget.year == payload.year
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Budget already exists for this month."
        )

    budget = Budget(
        user_id=user_id,
        month=payload.month,
        year=payload.year,
        amount=payload.amount
    )

    db.add(budget)
    db.commit()
    db.refresh(budget)

    return budget