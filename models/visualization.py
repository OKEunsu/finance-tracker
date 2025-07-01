from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models.account import Account
from models.asset_snapshot import AssetSnapshot
from models.expense import Expense
import pandas as pd
import plotly.express as px

def viz_spend_df() -> pd.DataFrame:
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
    pivot_df = pivot_df.loc[:, (pivot_df != 0).any(axis=0)]
    return pivot_df 

def viz_asset_df() -> pd.DataFrame:
    # DB 연결
    engine = create_engine("sqlite:///finance.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    # 월별 소비액 집계
    asset_data = session.query(AssetSnapshot).all()
    asset_data = (
        session.query(AssetSnapshot)
        .join(Account)
        .options(joinedload(AssetSnapshot.account))
        .all()
    )
    asset_df = pd.DataFrame([{
        "account_name": e.account.account_name,  # 조인한 계좌명
        "account_type": e.account.account_type,
        "date": e.date,
        "amount": e.balance
    } for e in asset_data])
    
    asset_df["account_type"] = asset_df["account_type"].apply(lambda x: x.name)

    pivot_df = pd.pivot_table(
    asset_df,
    index="date",       # 행: 계좌별
    columns="account_type",             # 열: 월별
    values="amount",            # 값: 잔액
    aggfunc="sum",              # 집계 함수
    fill_value=0,               # NaN 대신 0
    margins=False,               # 총합 행/열 추가
    ).reset_index().rename_axis(None, axis=1)

    return asset_df, pivot_df

def make_monthly_spend_chart(monthly_totals):
    fig = px.bar(
        monthly_totals,
        x='date',
        y='Total Spending',
        title='📊 월별 총 소비액 추이',
        text='Total Spending'
    )
    fig.update_traces(
        texttemplate='%{text:,} 원',
        textposition='outside',
        marker_color='cornflowerblue'
    )
    fig.update_xaxes(dtick="M1", tickformat="%Y-%m")
    fig.update_yaxes(
        range=[0, 3_000_000],
        title='소비액 (원)',
        tickformat=',',
        showgrid=False
    )
    return fig

def make_net_worth_chart(df):
    fig = px.line(
        df,
        x="date",
        y="net_worth",
        title="📈 순자산 추이",
        markers=True,
        labels={"date": "월", "net_worth": "금액 (₩)"}
    )
    fig.update_xaxes(dtick="M1", tickformat="%Y-%m")
    fig.update_yaxes(
        tickformat=",", dtick=1_000_000,
        showgrid=False, rangemode="tozero"
    )
    return fig
