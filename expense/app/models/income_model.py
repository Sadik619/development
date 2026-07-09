from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from storage.database import Base


class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    amount = Column(Numeric(10, 2), nullable=False)

    source = Column(String(100), nullable=False)

    description = Column(String(255))

    income_date = Column(Date, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship("User", back_populates="incomes")