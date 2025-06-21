from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import Base

class AssetSnapshot(Base):
    __tablename__ = "asset_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # accounts 테이블의 id를 참조
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    # 정산 일자 
    date = Column(String, nullable=False)  # 소비 일자
    # 자산 평가 금액
    balance = Column(BigInteger, nullable=False)
    # 계좌 연결
    account = relationship("Account", back_populates="snapshots")
