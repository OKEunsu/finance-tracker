import streamlit as st
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_session
import pandas as pd

st.set_page_config(layout="wide")
st.title("📂 데이터 테이블 설정 SQL 콘솔")

# SQL로 사용해서 DB 수정하게 만들기

# DB 세션
session: Session = next(get_session())

from sqlalchemy import inspect

# 인스펙터 생성
inspector = inspect(session.bind)

# 모든 테이블 목록
tables = inspector.get_table_names()

with st.expander("🔍 데이터베이스 테이블 및 컬럼 정보 보기"):
    if tables:
        for table in tables:
            st.markdown(f"### 📄 `{table}`")
            columns = inspector.get_columns(table)
            col_info = [
                {
                    "컬럼명": col["name"],
                    "타입": str(col["type"]),
                    "Nullable": col["nullable"],
                    "기본값": col.get("default")
                }
                for col in columns
            ]
            st.dataframe(pd.DataFrame(col_info))
    else:
        st.info("데이터베이스에 테이블이 없습니다.")

# SQL 입력창
sql_query = st.text_area(
    "실행할 SQL 쿼리를 입력하세요",
    height=200,
    placeholder="예: SELECT * FROM expenses WHERE amount > 50000"
)

# 실행 버튼
if st.button("🟢 실행하기"):
    try:
        # 실행
        result = session.execute(text(sql_query.strip()))

        # SELECT 쿼리라면 결과 보여주기
        if sql_query.strip().lower().startswith("select"):
            rows = result.fetchall()
            if rows:
                df = pd.DataFrame(rows, columns=result.keys())
                st.dataframe(df)
            else:
                st.info("조회 결과가 없습니다.")
        else:
            # DML 쿼리 (INSERT/UPDATE/DELETE 등)
            session.commit()
            st.success("✅ SQL 실행이 완료되었습니다.")
    except Exception as e:
        session.rollback()
        st.error("❌ 오류 발생:")
        st.exception(e)