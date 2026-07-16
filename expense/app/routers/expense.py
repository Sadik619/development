from sqlalchemy import extract, func
from sqlalchemy import func
from fastapi import APIRouter
from storage.database import get_db
from models.budget_model import Budget
from models.expense_model import Expense
from models.user_model import User
from fastapi import HTTPException
from models.category_model import Category
from fastapi import Depends
from auth.auth import get_current_user
from sqlalchemy.orm import Session
from schemas.expense import ExpenseCreate
from services.querydata import QueryData
router = APIRouter(
      prefix="",
      tags=["expenses"],
      )
@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.post("/expenses")
def create_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return QueryData.create_expense(
        db,
        current_user.id,
        payload,
    )
@router.get("/expenses")
def get_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(current_user)

    expenses = QueryData.get_expense_by_user(db,current_user.id)

    return expenses
@router.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int,
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return QueryData.update_expense(
        db,
        current_user.id,
        expense_id,
        payload,
    )

@router.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = QueryData.delete_expense_id_and_user(db,current_user.id,expense_id)

    return {"message": f"Expense deleted successfully,{expense}"}
  

@router.get("/analytics/monthly-summary")
def monthly_summary(
    month: int,
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    income = QueryData.get_income_month_wise(db, current_user.id,month,year)
    expense = QueryData.get_expense_month_wise(db, current_user.id,month,year)

    print("income",income)

    print("expense",expense)

    return {
        "total_income": float(income),
        "total_expense": float(expense),
        "savings": float(income - expense)
    }


@router.get("/analytics/category-summary")
def category_summary(
    month: int,
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    expense =  QueryData.get_category_wise_expense(db,current_user.id,month,year)
    for i in expense:
        print("11111",i)
    return [
        {
            "category": row["category"],
            "amount": float(row["amount"]),
        }
        for row in expense
    ]