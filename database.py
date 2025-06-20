# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base  # 꼭 필요
from models.account import Account
from models.asset_snapshot import AssetSnapshot

DATABASE_URL = "sqlite:///finance.db"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
