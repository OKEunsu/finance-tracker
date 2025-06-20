from sqlalchemy import Column, Integer, String, Enum
from models.base import Base
from models.account_type import AccountType

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bank_name = Column(String, nullable=False)
    account_name = Column(String, nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
        


