import streamlit as st
from sqlalchemy.orm import Session
from models.account import Account
from models.asset_snapshot import AssetSnapshot
from database import init_db, get_session
from datetime import datetime

init_db()  # 테이블 생성
session = next(get_session())

# 현재 연도 기준 범위 설정
current_year = datetime.now().year
years = [str(y) for y in range(current_year - 1, current_year+1)]
months = [f"{m:02d}" for m in range(1, 13)]  # 01 ~ 12

st.set_page_config(layout="centered")

# 1. 계좌 목록 불러오기
accounts = session.query(Account).all()
account_names = [acc.account_name for acc in accounts]
account_map = {acc.account_name: acc.id for acc in accounts}

st.title("📅 월말 자산 정산 등록")

# 2. 선택 박스
selected_account = st.selectbox("정산할 계좌를 선택하세요", account_names)
selected_account_id = account_map[selected_account]

# 3. 입력 폼
with st.form("asset_snapshot_form"):
    # 연/월 선택
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("연도 선택", years, index=years.index(str(current_year)))
    with col2:
        selected_month = st.selectbox("월 선택", months, index=datetime.now().month - 1)
        
    month_date = f"{selected_year}-{selected_month}"
    balance = st.number_input("잔액 (₩)", step=1000, format="%d")

    submitted = st.form_submit_button("정산 기록 저장")

    if submitted:
        new_snapshot = AssetSnapshot(
            account_id=selected_account_id,
            date=month_date,
            balance=balance,
        )
        session.add(new_snapshot)
        session.commit()
        st.success(f"'{selected_account}' 계좌의 {month_date} 정산 정보가 저장되었습니다.")

