from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from storage.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)

    name = Column(String(50), unique=True)

    expenses = relationship(
        "Expense",
        back_populates="category"
    )