from sqlalchemy import func

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