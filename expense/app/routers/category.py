from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.querydata import QueryData
from storage.database import get_db
from models.category_model import Category
from schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/", response_model=CategoryResponse)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db)
):
    category= QueryData.create_category(db,payload)
    return category


@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    category = QueryData.get_category(db)
    return category

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = QueryData.get_category_by_id(db,category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    payload: CategoryCreate,
    db: Session = Depends(get_db)
):
    return QueryData.update_category_by_id(
        db,
        category_id,
        payload,
    )


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category=QueryData.delete_category_id(db,category_id)
    return {"message": f"Category deleted successfully {category}"}