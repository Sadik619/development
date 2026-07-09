from fastapi import FastAPI
from routers import budget,dashboard,expense,income
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}
app.include_router(budget.router)
app.include_router(dashboard.router)
app.include_router(expense.router)
app.include_router(income.router)

