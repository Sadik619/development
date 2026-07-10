from fastapi import FastAPI
from routers import budget, dashboard, expense, income,category,user,login

app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0",
    description="Expense Tracker using FastAPI",
)

@app.get("/")
def home():
    return {"message": "Expense Tracker API"}

app.include_router(budget.router, prefix="/budget", tags=["Budget"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(expense.router, prefix="/expense", tags=["Expense"])
app.include_router(income.router, prefix="/income", tags=["income"])
app.include_router(category.router, prefix="/category", tags=["category"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(login.router, prefix="/login", tags=["login"])

