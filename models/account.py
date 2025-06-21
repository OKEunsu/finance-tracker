from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from models.base import Base
from models.categoryType import AccountType

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bank_name = Column(String, nullable=False)
    account_name = Column(String, nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    repayment_date = Column(String, nullable=True)
    
    # 자산 정산과의 관계
    snapshots = relationship("AssetSnapshot", back_populates="account", cascade="all, delete-orphan")



