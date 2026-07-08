from sqlalchemy import func
from storage.database import get_db
from sqlalchemy.future import select
from models import income_model

summary = (
    db.query(
        func.sum(Expense.amount)
    )
    .filter(
        Expense.user_id == user_id
    )
    .scalar()
)
async def income(db,current_user):
    stmt = (
        db.query(func.coalesce(func.sum(income_model.Income.amount), 0))
        .filter(income_model.Income.user_id == current_user.id)
        .scalar()
    )
    result = await db.execute(stmt)
    total_income = result.all()
    return total_income

async def total_expense(db):
    stmt = (
        db.query(func.coalesce(func.sum(Income.amount), 0))
        .filter(Income.user_id == current_user.id)
        .scalar()
    )
    result = await db.execute(stmt)
    total_income = result.all()
    return total_income

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