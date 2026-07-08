from storage.database import get_db
@router.post("/expenses")
async def create_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db)
):
    expense = Expense(**payload.dict())

    db.add(expense)
    db.commit()

    return {
        "message": "Expense Added"
    }

@router.get("/expenses")
def get_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == current_user.id)
        .all()
    )

    return expenses
@router.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int,
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == current_user.id
        )
        .first()
    )

    if not expense:
        raise HTTPException(404, "Expense not found")

    expense.category_id = payload.category_id
    expense.amount = payload.amount
    expense.description = payload.description
    expense.expense_date = payload.expense_date

    db.commit()

    return {"message": "Expense updated successfully"}

@router.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == current_user.id
        )
        .first()
    )

    if not expense:
        raise HTTPException(404, "Expense not found")

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted successfully"}


from sqlalchemy import extract, func

@router.get("/analytics/monthly-summary")
def monthly_summary(
    month: int,
    year: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    income = (
        db.query(func.coalesce(func.sum(Income.amount), 0))
        .filter(
            Income.user_id == current_user.id,
            extract('month', Income.income_date) == month,
            extract('year', Income.income_date) == year
        )
        .scalar()
    )

    expense = (
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(
            Expense.user_id == current_user.id,
            extract('month', Expense.expense_date) == month,
            extract('year', Expense.expense_date) == year
        )
        .scalar()
    )

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

    data = (
        db.query(
            Category.name,
            func.sum(Expense.amount)
        )
        .join(Category)
        .filter(
            Expense.user_id == current_user.id,
            extract('month', Expense.expense_date) == month,
            extract('year', Expense.expense_date) == year
        )
        .group_by(Category.name)
        .all()
    )

    return [
        {
            "category": row[0],
            "amount": float(row[1])
        }
        for row in data
    ]