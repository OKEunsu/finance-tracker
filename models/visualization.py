from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.account import Account
from models.asset_snapshot import AssetSnapshot
from models.expense import Expense
import pandas as pd

def viz_spend_df():
    # DB 연결
    engine = create_engine("sqlite:///finance.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    # 월별 소비액 집계
    expense_data = session.query(Expense).all()
    
    # SQLAlchemy 객체 리스트를 딕셔너리 리스트로 변환 → DataFrame 생성
    expense_df = pd.DataFrame([{
        "id": e.id,
        "category": e.sub_category,
        "date": e.date,
        "amount": e.amount
    } for e in expense_data])
    
    # 월별, 카테고리별 금액 합계로 피벗
    pivot_df = expense_df.pivot_table(
        index="category",        
        columns="date",   
        values="amount",      
        aggfunc="sum",        
        fill_value=0 ,         
        margins=True, 
        margins_name='Total'
    ).reset_index()

    pivot_df = pivot_df.sort_values(by = 'Total', ascending=False)
    pivot_df["category"] = pivot_df["category"].astype(str).str.replace("SubCategory.", "", regex=False)
    
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.drop(columns='index')
    return pivot_df 

