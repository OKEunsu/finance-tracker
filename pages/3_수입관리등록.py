# 수입관리등록.py
import streamlit as st
from datetime import date
from sqlalchemy.orm import Session
from models.income import IncomeByCategory
from database import get_session

st.set_page_config(page_title="수입 등록", page_icon="💵", layout="centered")
st.title("💵 수입 관리 등록")

# 세션 가져오기
session: Session = next(get_session())

# 입력 폼
category = st.selectbox("카테고리", ["근로소득", "사업소득", "투자소득", "기타소득"])
income_date = st.date_input("수입 날짜", value=date.today())
amount = st.number_input("금액 (₩)", min_value=0.0, step=1000.0)
memo = st.text_input("메모 (선택)", "")

if st.button("저장하기"):
    new_income = IncomeByCategory(
        category=category,
        income_date=income_date,
        amount=amount,
        memo=memo
    )
    session.add(new_income)
    session.commit()
    st.success("✅ 수입이 성공적으로 등록되었습니다!")
