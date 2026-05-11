import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="소방청 화재현황 분석", layout="wide")

DB_PATH = "소방청화재현황/소방청화재현황.db"

@st.cache_data
def run_query(query):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql(query, conn)

st.title("🔥 소방청 화재현황 개선 대시보드")

# --- 1. 발화요인 대분류별 화재 건수 (수정 완료 상태) ---
st.header("1. 발화요인 대분류별 화재 발생 현황")
sql1 = "SELECT 발화요인대분류, COUNT(*) as 발생건수 FROM fire GROUP BY 발화요인대분류 ORDER BY 발생건수 DESC"
df1 = run_query(sql1)
fig1 = px.bar(df1, x="발화요인대분류", y="발생건수", color="발화요인대분류", text_auto=True)
st.plotly_chart(fig1, use_container_width=True)


# --- 2. 계절별 습도에 따른 화재 발생 (구간화 적용) ---
st.header("2. 계절별 습도 구간에 따른 화재 발생")

sql2_raw = """
SELECT 
    CASE 
        WHEN strftime('%m', f.접수일시) IN ('03','04','05') THEN '봄'
        WHEN strftime('%m', f.접수일시) IN ('06','07','08') THEN '여름'
        WHEN strftime('%m', f.접수일시) IN ('09','10','11') THEN '가을'
        ELSE '겨울'
    END AS 계절,
    t.습도
FROM fire f
JOIN 온습도 t ON f.접수일시 = t.접수일시
"""
df2_raw = run_query(sql2_raw)

# [단계 1] 이상치 제거 (IQR 방식)
Q1 = df2_raw['습도'].quantile(0.25)
Q3 = df2_raw['습도'].quantile(0.75)
df2_filtered = df2_raw[(df2_raw['습도'] >= Q1) & (df2_raw['습도'] <= Q3)].copy()

# [단계 2] 습도 구간화 (5% 단위로 묶기)
# 0부터 100까지 5단위로 범위를 만듭니다. (0, 5, 10, ..., 100)
bins = list(range(0, 105, 5))
labels = [f"{i}~{i+5}%" for i in bins[:-1]]

df2_filtered['습도구간'] = pd.cut(df2_filtered['습도'], bins=bins, labels=labels, right=False)

# [단계 3] 계절과 습도구간으로 그룹화하여 개수 세기
df2_counts = df2_filtered.groupby(['계절', '습도구간'], observed=False).size().reset_index(name='발생건수')

# 시각화
fig2 = px.bar(df2_counts, x="습도구간", y="발생건수", color="계절",
             facet_col="계절", 
             category_orders={"계절": ["봄", "여름", "가을", "겨울"]},
             title=f"습도 구간별(5% 단위) 화재 발생 분포 (이상치 제외: {Q1:.1f}% ~ {Q3:.1f}%)")

st.plotly_chart(fig2, use_container_width=True)

with st.expander("인사이트"):
    st.write(f"습도를 5% 단위로 묶어서 보니, 특정 습도 구간에서 화재가 집중되는 모습이 훨씬 명확해졌습니다.")


# --- 3. 풍속 구간별 평균 재산 피해 (수정 완료 상태) ---
st.header("3. 풍속 구간별 평균 재산 피해")
sql3 = "SELECT 풍속 AS 풍속구간, AVG(재산피해소계) as 평균재산피해 FROM fire f JOIN 풍속향 w ON f.접수일시 = w.접수일시 WHERE 풍속 != 'NONE' GROUP BY 풍속"
df3 = run_query(sql3)
wind_order = ["0~4 m/s", "5~8 m/s", "9~12 m/s", "13~17 m/s", "18 m/s 이상"]
df3['풍속구간'] = pd.Categorical(df3['풍속구간'], categories=wind_order, ordered=True)
df3 = df3.sort_values('풍속구간')
fig3 = px.bar(df3, x="풍속구간", y="평균재산피해", color="풍속구간", text_auto='.0f')
st.plotly_chart(fig3, use_container_width=True)