import streamlit as st
from database import SessionLocal
from models.account import Account
from models.categoryType import AccountType
from models.mappings import account_map
from database import init_db, get_session
import pandas as pd

init_db()  # 테이블 생성

st.title("💳 계좌 등록")

with st.form("account_form", clear_on_submit=True):
    bank_name = st.text_input("은행명", placeholder="예: 카카오뱅크")
    account_name = st.text_input("계좌명", placeholder="예: 생활비")
    account_type_label = st.selectbox("계좌 유형", list(account_map.keys()))
    account_type_enum = account_map[account_type_label]
    repayment_date = st.text_input("상환일", placeholder="예: 15일")

    submitted = st.form_submit_button("계좌 등록")

if submitted:
    if not bank_name or not account_name:
        st.warning("⚠️ 은행명과 계좌명은 필수 입력 항목입니다.")
    else:
        db = SessionLocal()
        try:
            acc = Account(
                bank_name=bank_name,
                account_name=account_name,
                account_type=account_type_enum,
                repayment_date=repayment_date if repayment_date else None
            )
            db.add(acc)
            db.commit()
            db.refresh(acc)
            st.success(f"✅ 계좌 '{account_name}'이(가) 등록되었습니다!")
        finally:
            db.close()

session = next(get_session())

# 1. 계좌 목록 불러오기
accounts = session.query(Account).all()

# Account 객체들을 딕셔너리로 변환
df_accounts = pd.DataFrame([
    {
        "은행": acc.bank_name,
        "계좌명": acc.account_name,
        "계좌유형": acc.account_type.value  # Enum일 경우 .value 필요
    }
    for acc in accounts
])

st.markdown("#### 📂 등록된 계좌 목록")
st.dataframe(df_accounts, hide_index=True)