import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px

# 1. 페이지 설정 및 DB 연결 확인
st.set_page_config(page_title="소방청 화재현황 분석", layout="wide")

DB_PATH = "소방청화재현황.db"

def check_db():
    if not os.path.exists(DB_PATH):
        st.error(f"⚠️ '{DB_PATH}' 파일이 같은 폴더에 없습니다. 데이터베이스 파일을 확인해주세요!")
        st.stop()

check_db()

# 데이터 불러오기 함수 (캐싱을 통해 속도 향상)
@st.cache_data
def run_query(query):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql(query, conn)

st.title("🔥 소방청 화재현황 데이터 분석 대시보드")
st.markdown("공공데이터를 활용하여 화재의 원인과 환경적 요인을 분석합니다.")

# --- 차트 1: 발화요인별 화재 발생률 ---
st.header("1. 발화요인 대분류/소분류별 화재 발생")

sql1 = """
SELECT 발화요인대분류, 발화요인소분류, COUNT(*) as 발생건수
FROM fire
GROUP BY 발화요인대분류, 발화요인소분류
ORDER BY 발화요인대분류
"""
df1 = run_query(sql1)

# 대분류별로 그룹화하여 시각화 (facet_col을 사용하여 대분류 간 간격 확보)
fig1 = px.bar(df1, x="발화요인소분류", y="발생건수", color="발화요인대분류",
             facet_col="발화요인대분류", facet_col_wrap=3,
             title="발화요인 대분류별 소분류 화재 건수")
fig1.update_xaxes(matches=None) # 각 서브차트의 x축 독립 설정

st.plotly_chart(fig1, use_container_width=True)

with st.expander("사용한 SQL 및 인사이트"):
    st.code(sql1, language='sql')
    st.write("- **인사이트**: 특정 대분류(예: 전기적 요인) 내에서 특정 소분류의 비중이 압도적으로 높은지 확인할 수 있습니다. 대분류 간 거리를 두어 각 카테고리별 집중 요인을 한눈에 비교하기 좋습니다.")


# --- 차트 2: 계절별 습도에 따른 화재발생률 ---
st.header("2. 계절별 습도에 따른 화재 발생")

sql2 = """
SELECT 
    CASE 
        WHEN strftime('%m', f.접수일시) IN ('03','04','05') THEN '봄'
        WHEN strftime('%m', f.접수일시) IN ('06','07','08') THEN '여름'
        WHEN strftime('%m', f.접수일시) IN ('09','10','11') THEN '가을'
        ELSE '겨울'
    END AS 계절,
    (t.습도 / 10 * 10) || '%' as 습도범위, 
    COUNT(*) as 발생건수
FROM fire f
JOIN 온습도 t ON f.접수일시 = t.접수일시
GROUP BY 계절, 습도범위
ORDER BY 계절, 습도범위
"""
df2 = run_query(sql2)

fig2 = px.bar(df2, x="습도범위", y="발생건수", color="계절",
             facet_col="계절", category_orders={"계절": ["봄", "여름", "가을", "겨울"]},
             title="계절 및 습도 구간별 화재 발생 빈도")

st.plotly_chart(fig2, use_container_width=True)

with st.expander("사용한 SQL 및 인사이트"):
    st.code(sql2, language='sql')
    st.write("- **인사이트**: 습도가 낮은 겨울과 봄철에 화재 발생 건수가 집중되는 경향을 보입니다. 특히 특정 습도 구간(예: 30-40%)에서 사고가 급증하는지 파악하여 예방 조치를 강화할 수 있습니다.")


# --- 차트 3: 풍속에 따른 재산 피해 소계 ---
st.header("3. 풍속에 따른 평균 재산 피해")

sql3 = """
SELECT 
    CASE 
        WHEN 풍속 < 2 THEN '0-2(약풍)'
        WHEN 풍속 < 4 THEN '2-4(남실바람)'
        WHEN 풍속 < 6 THEN '4-6(건들바람)'
        WHEN 풍속 < 8 THEN '6-8(흔들바람)'
        ELSE '8+(강풍)'
    END AS 풍속구간,
    AVG(재산피해소계) as 평균재산피해
FROM fire f
JOIN 풍속향 w ON f.접수일시 = w.접수일시
WHERE 풍속 IS NOT NULL
GROUP BY 풍속구간
ORDER BY 풍속
"""
df3 = run_query(sql3)

fig3 = px.bar(df3, x="풍속구간", y="평균재산피해", 
             color="풍속구간",
             title="풍속 구간별 화재당 평균 재산 피해액")

st.plotly_chart(fig3, use_container_width=True)

with st.expander("사용한 SQL 및 인사이트"):
    st.code(sql3, language='sql')
    st.write("- **인사이트**: 풍속이 강해질수록 불길이 번지는 속도가 빨라져 평균 재산 피해액이 증가하는 상관관계를 확인할 수 있습니다. 데이터 개수가 적더라도 평균값(AVG)을 통해 풍속의 위험성을 객관적으로 보여줍니다.")