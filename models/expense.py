from sqlalchemy import Column, Integer, String, Enum
from models.base import Base
from models.categoryType import SubCategory

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sub_category = Column(Enum(SubCategory), nullable=False)  # 소비 태그
    date = Column(String, nullable=False)  # 소비 일자
    amount = Column(Integer, nullable=False)  # 소비 금액
