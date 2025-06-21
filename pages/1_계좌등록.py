import streamlit as st
from database import SessionLocal
from models.account import Account
from models.asset_snapshot import AssetSnapshot

st.title("💳 계좌 등록")

with st.form("account_form"):
    bank_name = st.text_input("은행명", placeholder="예: 카카오뱅크")
    account_name = st.text_input("계좌명", placeholder="예: 생활비")
    account_type = st.selectbox("계좌 유형", ["CHECKING", "SAVING", "INVESTMENT", "LOAN", "ETC"])
    year_month = st.text_input("기준 월", placeholder="예: 2024-06")

    submitted = st.form_submit_button("계좌 등록")

if submitted:
    db = SessionLocal()
    acc = Account(bank_name=bank_name, account_name=account_name, account_type=account_type)
    db.add(acc)
    db.commit()
    db.refresh(acc)  

    st.success(f"✅ 계좌 '{account_name}'이(가) 등록되었습니다!")
