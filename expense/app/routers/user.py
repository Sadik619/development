from fastapi import APIRouter, Depends, HTTPException
from schemas.user import UserResponse,UserCreate
from models.user_model import User
from storage.database import get_db
from sqlalchemy.orm import Session
from auth.password import hash_password
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



@router.post("/", response_model=UserResponse)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(
        User.email == payload.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password) # Hash this in a real application
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user