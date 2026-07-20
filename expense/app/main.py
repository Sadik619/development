from fastapi import FastAPI
from routers import budget, dashboard, expense, income,category,user,login

app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0",
    description="Expense Tracker using FastAPI",
)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"message": "Expense Tracker API"}

app.include_router(budget.router, tags=["Budget"])
app.include_router(dashboard.router,  tags=["Dashboard"])
app.include_router(expense.router, tags=["Expense"])
app.include_router(income.router, tags=["income"])
app.include_router(category.router,  tags=["category"])
app.include_router(user.router, tags=["user"])
app.include_router(login.router, tags=["login"])

