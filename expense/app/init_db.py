from storage.database import Base, engine

# from models.user_model import User
# from models.budget_model import Budget
# from models.expense_model import Expense
# from models.income_model import Income
from models.category_model import Category

Base.metadata.create_all(bind=engine)