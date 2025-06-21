# home.py
import streamlit as st
from models.visualization import viz_spend_df
import plotly.express as px

st.set_page_config(layout='wide')
st.title("🏠 자산관리 홈")

st.markdown("#### 💸 월별 소비 내역")

df = viz_spend_df()
# 숫자형 컬럼만 포맷 지정
number_cols = df.select_dtypes(include=["number"]).columns

# Total 행만 추출
monthly_totals = df[df['category'] == 'Total'].drop(columns=['category']).T
monthly_totals.columns = ['Total Spending']
monthly_totals = monthly_totals.reset_index().rename(columns={'index': 'date'})

fig = px.bar(
    monthly_totals,
    x='date',
    y='Total Spending',
    title='📈 월별 총 소비액 추이',
    text='Total Spending' # Use 'Total Spending' for text directly on bars
)

fig.update_traces(
    texttemplate='%{text:,} 원',  # 숫자에 천 단위 콤마
    textposition='outside',    # 막대 그래프에서 숫자 위치 (막대 상단 바깥)
    textfont=dict(size=14, color='white'), # 텍스트 색상 변경 (막대 안에 있을 경우 대비)
    marker_color='cornflowerblue' # 막대 색상
)

# hover 시 막대 강조 (line chart와 동일하게 설정 가능)
fig.update_traces(
    hoverinfo='x+y',
    hoverlabel=dict(
        bgcolor='#1e1e1e',  # 다크 회색 배경 (Streamlit 다크 모드에 자연스럽게 어울림)
        font=dict(color='white'),  # 글씨는 밝게
        bordercolor='#888'  # 테두리 색은 은은하게
    ),
    hovertemplate="<b>%{x}</b><br>총 소비: %{y:,}원<extra></extra>"
)

# y축 스타일 설정
fig.update_yaxes(
    range=[0, 3_000_000],      # y축 시작값을 0으로 설정하여 막대 그래프의 비례감을 유지
    title='소비액 (원)',
    tickformat=',',            # 천 단위 콤마
    showgrid=False             # 가로줄 제거
)

st.plotly_chart(fig, use_container_width=True)

df_won = df.copy()
df_style = df_won.style.format({col: "{:,.0f}" for col in number_cols})

st.dataframe(df_style, hide_index=True, height = 668)

