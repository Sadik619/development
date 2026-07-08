from services import querydata
from storage.database import get_db
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
    income=querydata.income(db,current_user.id)
    return income

    # return (
    #     db.query(Income)
    #     .filter(Income.user_id == current_user.id)
    #     .all()
    # )