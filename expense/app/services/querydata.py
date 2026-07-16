from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy import extract
from models.expense_model import Expense
from models.income_model import Income
from models.category_model import Category
from models.budget_model import Budget
from sqlalchemy.orm import Session

class QueryData:
    @staticmethod
    def get_income_by_id(db,user_id):
        stmt = select(Income).where(
            Income.user_id == user_id
        )
        result = db.execute(stmt)
        rows = result.mappings().all()
        return rows
    @staticmethod
    def create_category(db: Session, payload):
        stmt = select(Category).where(Category.name == payload.name)

        result = db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Category already exists"
            )

        category = Category(name=payload.name)

        db.add(category)
        db.commit()
        db.refresh(category)

        return category
   

    @staticmethod
    def update_category_by_id(
        db: Session,
        category_id: int,
        payload,
    ):
        stmt = select(Category).where(Category.id == category_id)

        result = db.execute(stmt)
        category = result.scalar_one_or_none()

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found",
            )

        category.name = payload.name

        db.commit()
        db.refresh(category)

        return category
    
    @staticmethod
    def delete_category_id(
        db: Session,
        category_id: int,
    ):
        stmt = select(Category).where(
            Category.id == category_id,
        )

        result = db.execute(stmt)
        category = result.scalar_one_or_none()
        print(category)
        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Expense not found",
            )

        db.delete(category)
        db.commit()

        return {"message": "Category deleted successfully"}

    @staticmethod
    def get_category(db: Session):
        stmt = select(Category)
        result = db.execute(stmt)
        return result.scalars().all()
        
    
    @staticmethod
    def get_category_by_id(db: Session,category_id):
        stmt = select(Category).filter(Category.id == category_id)
        result = db.execute(stmt)
        return result.scalars().first()
    
    @staticmethod
    def total_income(db: Session, user_id: int):
        stmt = select(func.coalesce(func.sum(Income.amount), 0)).where(
            Income.user_id == user_id
        )

        result = db.execute(stmt)
        return result.scalar()

    @staticmethod
    def total_expense(db: Session, user_id: int):
        stmt = select(func.coalesce(func.sum(Expense.amount), 0)).where(
            Expense.user_id == user_id
        )

        result = db.execute(stmt)
        return result.scalar()

    @staticmethod
    def transaction_count(db: Session, user_id: int):
        stmt = select(func.count(Expense.id)).where(
            Expense.user_id == user_id
        )

        result =  db.execute(stmt)
        return result.scalar()

    @staticmethod
    def get_income_month_wise(db: Session, user_id: int,month,year):
        stmt=select(func.coalesce(func.sum(Income.amount), 0)).filter(
            Income.user_id == user_id,
            extract('month', Income.income_date) == month,
            extract('year', Income.income_date) == year
        )
        result =  db.execute(stmt)
        return result.scalar()
    
    @staticmethod
    def get_expense_month_wise(db: Session, user_id: int,month:int,year:int):
        print(month,year)
        stmt=select(func.coalesce(func.sum(Expense.amount), 0)).filter(
            Expense.user_id == user_id,
            extract('month', Expense.expense_date) == month,
            extract('year', Expense.expense_date) == year
        )
        result =  db.execute(stmt)
        return result.scalar()
    
    #         expense = (
    #             db.query(func.coalesce(func.sum(Expense.amount), 0))
    #             .filter(
    #                 Expense.user_id == current_user.id,
    #                 extract('month', Expense.expense_date) == month,
    #                 extract('year', Expense.expense_date) == year
    #             )
    #             .scalar()
    # )
  
    @staticmethod
    def get_category_by_id(db: Session,category_id):
        stmt=select(Category).filter(Category.id == category_id)
        # result =  db.execute(stmt)
        result = db.execute(stmt)
        rows = result.mappings().all()
        return rows
    
    @staticmethod
    def create_expense(db: Session, user_id: int, payload):
        # Check if category exists
        stmt = select(Category).where(Category.id == payload.category_id)

        result = db.execute(stmt)
        category = result.scalar_one_or_none()

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found."
            )

        expense = Expense(
            user_id=user_id,
            category_id=payload.category_id,
            amount=payload.amount,
            description=payload.description,
            expense_date=payload.expense_date,
        )

        db.add(expense)
        db.commit()
        db.refresh(expense)

        return expense
    

    @staticmethod
    def update_expense(
        db: Session,
        user_id: int,
        expense_id: int,
        payload,
    ):
        # Get expense
        stmt = select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == user_id,
        )

        result = db.execute(stmt)
        expense = result.scalar_one_or_none()

        if expense is None:
            raise HTTPException(
                status_code=404,
                detail="Expense not found",
            )

        # Check category exists
        stmt = select(Category).where(
            Category.id == payload.category_id
        )

        result = db.execute(stmt)
        category = result.scalar_one_or_none()

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found",
            )

        # Update fields
        expense.category_id = payload.category_id
        expense.amount = payload.amount
        expense.description = payload.description
        expense.expense_date = payload.expense_date

        db.commit()
        db.refresh(expense)

        return {"message": "Expense updated successfully"}

    @staticmethod
    def get_expense_by_user(db: Session,user_id):
        stmt=select(Expense).filter(Expense.user_id == user_id)
        # result =  db.execute(stmt)
        # return result.all()
        result = db.execute(stmt)
        rows = result.mappings().all()
        return rows
    @staticmethod
    def post_income(db: Session, user_id: int, payload):
        income = Income(
            user_id=user_id,
            amount=payload.amount,
            source=payload.source,
            income_date=payload.income_date,
        )

        db.add(income)
        db.commit()
        db.refresh(income)

        return income

    @staticmethod
    def get_expense_id_and_user(db: Session,user_id,expense_id):
        stmt=select(Expense).filter(Expense.user_id == user_id,Expense.id == expense_id)
        # result =  db.execute(stmt)
        # return result.all()
        result = db.execute(stmt)
        rows = result.mappings().first()
        return rows
    
    @staticmethod
    def delete_expense_id_and_user(
        db: Session,
        user_id: int,
        expense_id: int,
    ):
        stmt = select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == user_id,
        )

        result = db.execute(stmt)
        expense = result.scalar_one_or_none()
        print(expense)
        if expense is None:
            raise HTTPException(
                status_code=404,
                detail="Expense not found",
            )

        db.delete(expense)
        db.commit()

        return {"message": "Expense deleted successfully"}
    @staticmethod
    def get_category_wise_expense(db: Session,user_id: int,month,year):
        stmt = select(Category.name.label("category"),
            func.sum(Expense.amount).label("amount"),).join(Category).where(
            Expense.user_id == user_id,
            extract('month', Expense.expense_date) == month,
            extract('year', Expense.expense_date) == year
        ).group_by(Category.name)

        result = db.execute(stmt)
        rows = result.mappings().all()
        return rows
    @staticmethod
    def create_budget(db: Session, user_id: int, payload):
        # Check if budget already exists
        existing = db.execute(
            select(Budget).where(
                Budget.user_id == user_id,
                Budget.month == payload.month,
                Budget.year == payload.year,
            )
        ).scalar_one_or_none()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Budget already exists for this month."
            )

        budget = Budget(
            user_id=user_id,
            month=payload.month,
            year=payload.year,
            amount=payload.amount,
        )

        db.add(budget)
        db.commit()
        db.refresh(budget)

        return budget
    
    @staticmethod
    def get_budget_by_userid_monthwise(db: Session, user_id: int, month: int, year: int):
        budget = db.execute(
            select(Budget).where(
                Budget.user_id == user_id,
                Budget.month == month,
                Budget.year == year,
            )
        ).scalar_one_or_none()
        return budget
    
    @staticmethod
    def get_spend_summary(db: Session, user_id: int):
        spent = db.execute(
            select(func.coalesce(func.sum(Expense.amount), 0)).where(
                Expense.user_id == user_id
            )
        ).scalar_one()
        return spent
    
    #     data = (
    #     db.query(
    #         Category.name,
    #         func.sum(Expense.amount)
    #     )
    #     .join(Category)
    #     .filter(
    #         Expense.user_id == current_user.id,
    #         extract('month', Expense.expense_date) == month,
    #         extract('year', Expense.expense_date) == year
    #     )
    #     .group_by(Category.name)
    #     .all()
    # )
    #     income =  QueryData.total_income(db, user_id)
    #     expense = await QueryData.total_expense(db, user_id)
    #     transactions = await QueryData.transaction_count(db, user_id)

    #     return {
    #         "total_income": income,
    #         "total_expense": expense,
    #         "balance": income - expense,
    #         "transaction_count": transactions,
    #     }