import streamlit as st
from database import SessionLocal
from models.expense import Expense
from models.categoryType import SubCategory
from models.mappings import spend_map  
from database import init_db
from datetime import datetime

init_db()  # 테이블 생성

# 현재 연도 기준 범위 설정
current_year = datetime.now().year
years = [str(y) for y in range(current_year - 2, current_year+1)]
months = [f"{m:02d}" for m in range(1, 13)]  # 01 ~ 

st.set_page_config(layout="centered")
st.title("💸 소비 관리")

with st.form("expense_form", clear_on_submit=True):
    sub_category = st.selectbox("소비 카테고리", list(spend_map.keys()))
    sub_category_enum = spend_map[sub_category]
    
    # 연/월 선택
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("연도 선택", years, index=years.index(str(current_year)))
    with col2:
        selected_month = st.selectbox("월 선택", months, index=datetime.now().month - 1)
        
    month_date = f"{selected_year}-{selected_month}"
    amount = st.number_input("금액", step=1000)
    submitted = st.form_submit_button("지출 등록")
    
if submitted:
    db = SessionLocal()
    try:
        expense = Expense(
            sub_category=sub_category_enum,
            date=month_date,  # 여기 수정됨
            amount=int(amount)
        )
        db.add(expense)
        db.commit()
        st.success(f"✅ {month_date}의 '{sub_category}' 카테고리에 {amount:,}원 지출이 등록되었습니다!")
    except Exception as e:
        st.error("❌ 지출 등록 중 오류가 발생했습니다.")
        st.exception(e)
    finally:
        db.close()
