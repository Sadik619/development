from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.expense_model import Expense
from models.income_model import Income


class QueryData:

    @staticmethod
    def total_income(db: AsyncSession, user_id: int):
        stmt = select(func.coalesce(func.sum(Income.amount), 0)).where(
            Income.user_id == user_id
        )

        result = db.execute(stmt)
        return result.scalar()

    @staticmethod
    def total_expense(db: AsyncSession, user_id: int):
        stmt = select(func.coalesce(func.sum(Expense.amount), 0)).where(
            Expense.user_id == user_id
        )

        result = db.execute(stmt)
        return result.scalar()

    @staticmethod
    def transaction_count(db: AsyncSession, user_id: int):
        stmt = select(func.count(Expense.id)).where(
            Expense.user_id == user_id
        )

        result =  db.execute(stmt)
        return result.scalar()

    # @staticmethod
    # def dashboard_summary(db: AsyncSession, user_id: int):
    #     income =  QueryData.total_income(db, user_id)
    #     expense = await QueryData.total_expense(db, user_id)
    #     transactions = await QueryData.transaction_count(db, user_id)

    #     return {
    #         "total_income": income,
    #         "total_expense": expense,
    #         "balance": income - expense,
    #         "transaction_count": transactions,
    #     }