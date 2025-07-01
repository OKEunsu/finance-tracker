from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class IncomeByCategory(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String, nullable=False)       # 예: 근로소득, 사업소득, 투자소득
    income_date = Column(Date, nullable=False)      # 날짜 (월별 기록)
    amount = Column(Float, nullable=False)          # 수입 금액
    memo = Column(String)                           # 선택 메모

    def __repr__(self):
        return f"<IncomeByCategory(category={self.category}, date={self.income_date}, amount={self.amount})>"
