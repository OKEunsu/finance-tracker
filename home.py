# home.py
import streamlit as st
import pandas as pd
from models.visualization import viz_spend_df, viz_asset_df
from models.compute import compute_financial_metrics  # 추후 사용 예정
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="자산관리", page_icon="🏠", layout="wide")

st.title("🏠 자산관리 홈")

# -------------------------------
# 💰 월별 자산 내역
# -------------------------------
st.markdown("#### 💰 월별 자산 내역")
_, asset_df = viz_asset_df()
asset_df["date"] = pd.to_datetime(asset_df["date"], format="%Y-%m")

# 정렬 및 파생 컬럼
asset_df_sorted = asset_df.sort_values(by="date")
asset_df_sorted["total_asset"] = asset_df_sorted[["CHECKING", "ETC", "INVESTMENT", "SAVING"]].sum(axis=1)
asset_df_sorted["net_worth"] = asset_df_sorted["total_asset"] + asset_df_sorted["LOAN"]

def safe_ratio(numer, denom):
    return numer / denom * 100 if denom != 0 else 0

asset_df_sorted["debt_ratio"] = asset_df_sorted.apply(
    lambda row: safe_ratio(abs(row["LOAN"]), row["total_asset"]),
    axis=1
)
asset_df_sorted["liquidity_ratio"] = asset_df_sorted.apply(
    lambda row: safe_ratio(row["CHECKING"], abs(row["LOAN"])),
    axis=1
)

# 최신/전월 비교를 위한 계산
if len(asset_df_sorted) >= 2:
    latest = asset_df_sorted.iloc[-1]
    previous = asset_df_sorted.iloc[-2]

    # 최신값
    total_asset = latest["total_asset"]
    total_debt = latest["LOAN"]
    net_worth = latest["net_worth"]
    debt_ratio = safe_ratio(abs(total_debt), total_asset)
    liquidity = latest["CHECKING"] + latest["ETC"]
    liquidity_ratio = safe_ratio(liquidity, abs(total_debt))
    investment_ratio = safe_ratio(latest["INVESTMENT"], total_asset)

    # 전월값
    prev_total_asset = previous["total_asset"]
    prev_total_debt = previous["LOAN"]
    prev_net_worth = previous["net_worth"]
    prev_debt_ratio = safe_ratio(abs(prev_total_debt), prev_total_asset)
    prev_liquidity = previous["CHECKING"] 
    prev_liquidity_ratio = safe_ratio(prev_liquidity, abs(prev_total_debt))
    prev_investment_ratio = safe_ratio(previous["INVESTMENT"], prev_total_asset)

    metrics = {
        "총자산": (total_asset, total_asset - prev_total_asset),
        "총부채": (total_debt, total_debt - prev_total_debt),
        "순자산": (net_worth, net_worth - prev_net_worth),
        "부채비율": (debt_ratio, debt_ratio - prev_debt_ratio),
        "유동비율": (liquidity_ratio, liquidity_ratio - prev_liquidity_ratio),
        "투자비중": (investment_ratio, investment_ratio - prev_investment_ratio),
    }

else:
    latest = asset_df_sorted.iloc[-1]
    total_asset = int(latest["total_asset"])
    total_debt = int(latest["LOAN"])
    net_worth = int(latest["net_worth"])
    debt_ratio = abs(total_debt) / total_asset * 100 if total_asset else 0
    liquidity = latest["CHECKING"]
    liquidity_ratio = liquidity / abs(total_debt) * 100 if total_debt else 0
    investment_ratio = latest["INVESTMENT"] / total_asset * 100 if total_asset else 0

    metrics = {
        "총자산": (total_asset, "–"),
        "총부채": (total_debt, "–"),
        "순자산": (net_worth, "–"),
        "부채비율": (debt_ratio, "–"),
        "유동비율": (liquidity_ratio, "–"),
        "투자비중": (investment_ratio, "–"),
    }

# -------------------------------
# 📊 3x2 메트릭 출력
# -------------------------------

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
cols = [col1, col2, col3, col4, col5, col6]

metric_labels = [
    ("총자산", "₩ {:,.0f}", "{:+,.0f}"),      
    ("총부채", "₩ {:,.0f}", "{:+,.0f}"),      
    ("순자산", "₩ {:,.0f}", "{:+,.0f}"),      
    ("부채비율", "{:.2f}%", "{:+.2f}%"),
    ("유동비율", "{:.2f}%", "{:+.2f}%"),
    ("투자비중", "{:.2f}%", "{:+.2f}%"),
]

for i, (label, value_fmt, delta_fmt) in enumerate(metric_labels):
    value, delta = metrics[label]
    
    # 안전한 포맷팅
    try:
        value_str = value_fmt.format(value) if isinstance(value, (int, float)) else str(value)
    except (ValueError, TypeError):
        value_str = str(value)
    
    try:
        delta_str = delta_fmt.format(delta) if isinstance(delta, (int, float)) else str(delta)
    except (ValueError, TypeError):
        delta_str = "–"
    
    cols[i].metric(label, value_str, delta_str, border=True)

# -------------------------------
# 📈 순자산 추이 라인 차트
# -------------------------------
fig_1 = px.line(
    asset_df_sorted,
    x="date",
    y="net_worth",
    title="📈 순자산 추이",
    markers=True,
    labels={"date": "월", "net_worth": "금액 (₩)"}
)
fig_1.update_xaxes(dtick="M1", tickformat="%Y-%m")
fig_1.update_yaxes(
    tickformat=",", dtick=1000000,
    showgrid=False, rangemode="tozero"
)
fig_1.update_traces(
    line_color="green",
    marker=dict(size=20, color="green")  # 👈 마커 크기와 색상 지정
)
st.plotly_chart(fig_1, use_container_width=True)

# -------------------------------
# 부채비율 추이 라인 차트
# -------------------------------
fig_2 = px.line(
    asset_df_sorted,
    x="date",
    y="debt_ratio",
    title="📉 부채비율 추이",
    markers=True,
    labels={"date": "월", "debt_ratio": "부채비율 (%)"},
    line_shape="linear"
)

# 빨간색 지정
fig_2.update_traces(
    line_color="red",
    marker=dict(size=20, color="red")  # 👈 마커 크기와 색상 지정
)

# 축 설정
fig_2.update_xaxes(dtick="M1", tickformat="%Y-%m")
fig_2.update_yaxes(
    tickformat=".1f",  # 소수점 한 자리 (%)
    dtick=10,
    showgrid=False,
    rangemode="tozero"
)

st.plotly_chart(fig_2, use_container_width=True)

# 
fig_3 = px.line(
    asset_df_sorted,
    x="date",
    y="liquidity_ratio",
    title="🧮 유동비율 추이",
    markers=True,
    labels={"date": "월", "liquidity_ratio": "유동비율 (%)"}
)

fig_3.update_traces(
    line_color="yellow",
    marker=dict(size=20, color="yellow")
)

fig_3.update_xaxes(dtick="M1", tickformat="%Y-%m")
fig_3.update_yaxes(
    tickformat=".1f", dtick=50,
    showgrid=False, rangemode="tozero"
)

st.plotly_chart(fig_3, use_container_width=True, key="current_ratio_chart")

# -------------------------------
# 💸 월별 소비 내역
# -------------------------------
st.markdown("#### 💸 월별 소비 내역")
spend_df = viz_spend_df()
number_cols = spend_df.select_dtypes(include=["number"]).columns

# ✅ 월별 총 소비액 추이 데이터 구성
monthly_totals = spend_df[spend_df['category'] == 'Total'].drop(columns=['category']).T
monthly_totals.columns = ['Total Spending']
monthly_totals = monthly_totals.reset_index().rename(columns={'index': 'date'})

# ✅ 바 차트
fig = px.bar(
    monthly_totals,
    x='date',
    y='Total Spending',
    title='📉 월별 총 소비액 추이',
    text='Total Spending'
)
fig.update_traces(
    texttemplate='%{text:,}원',
    textposition='outside',
    marker_color='cornflowerblue'
)
fig.update_xaxes(dtick="M1", tickformat="%Y-%m")
fig.update_yaxes(
    range=[0, 4_000_000],
    title='소비액 (원)',
    tickformat=',',
    showgrid=False
)
st.plotly_chart(fig, use_container_width=True)

df_pie = spend_df[spend_df["category"] != "Total"].copy()

# ✅ 1. 드롭다운에서 Total 제거
number_cols = [col for col in df_pie.columns if col not in ["category", "Total"]]
selected_month = st.selectbox("📅 조회할 월을 선택하세요", options=number_cols)

# ✅ 2. 해당 월 기준 데이터 추출
pie_data = df_pie[["category", selected_month]].copy()
pie_data = pie_data[pie_data[selected_month] > 0]
pie_data.columns = ["category", "amount"]

# 소비 데이터 준비 (pie_data: category, amount 포함)
total_amount = int(pie_data["amount"].sum())
total_text = f"{total_amount:,.0f}원"

# ✅ 3. 카테고리 상위 N개 + 기타 처리
N = 7
pie_data = pie_data.sort_values(by="amount", ascending=False)
top = pie_data[:N]
others = pie_data[N:]

if not others.empty:
    others_sum = pd.DataFrame([{
        "category": "기타",
        "amount": others["amount"].sum()
    }])
    pie_data = pd.concat([top, others_sum], ignore_index=True)

# ✅ 4. 커스텀 색상 설정 (원하면 이 리스트 바꿔도 됨)
color_sequence = [
    "#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF", "#845EC2", "#FF9671", "#00C9A7", "#B0A8B9"
]

# ✅ 5. 파이차트 크기 키우고 시각화
fig = px.pie(
    pie_data,
    names="category",
    values="amount",
    title=f"{selected_month} 소비 비중",
    color_discrete_sequence=color_sequence,
    hole=0.4  # 도넛 스타일
)

# 중앙 텍스트 추가 (annotation)
fig.update_layout(
    title_text=f"{selected_month} 소비 비중",
    annotations=[dict(
        text=total_text,
        x=0.5, y=0.5,
        font_size=18,
        showarrow=False
    )],
    height=500
)
fig.update_traces(textinfo="percent+label")  # 퍼센트와 라벨 같이

st.plotly_chart(fig, use_container_width=True)

# ✅ 소비 내역 테이블
df_style = spend_df.copy().style.format({col: "{:,.0f}" for col in number_cols})
st.dataframe(df_style, hide_index=True, height=668)
