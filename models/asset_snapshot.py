from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class AssetSnapshot(Base):
    __tablename__ = "asset_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year_month = Column(String, nullable=False)
    balance = Column(Integer, nullable=False)

    account_id = Column(Integer, ForeignKey("accounts.id"))
    account = relationship("Account", backref="snapshots")
