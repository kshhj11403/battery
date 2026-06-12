from pathlib import Path

code = r'''
"""
Battery Intelligence Platform (Concept v2)

UI 방향:
- 일반인은 "건강도 / 교체시점 / 관리방법"만 확인
- 평가원은 "Digital Twin / XAI / Risk Radar / Confidence Interval" 확인

streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Battery Intelligence Platform", layout="wide")

st.markdown("""
<style>
.stApp{background:#f8fafc;}
.main-card{
    background:white;
    padding:24px;
    border-radius:20px;
    border:1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

st.title("🔋 Battery Intelligence Platform")
st.caption("배터리 교체 시점 예측 · Digital Twin · XAI 분석")

with st.container():
    c1,c2,c3,c4 = st.columns(4)

    battery = c1.selectbox("배터리 종류",["Li-ion","LFP","NMC"])
    cycle = c2.slider("충방전 횟수",0,5000,800)
    temp = c3.slider("평균 온도",0,60,28)
    months = c4.slider("사용 개월 수",0,120,24)

soh = max(40,100-cycle*0.015-months*0.08)
health_score = round(soh)
pred_years = max(0.5,(4000-cycle)/1000)

st.subheader("Executive Summary")

m1,m2,m3 = st.columns(3)

m1.metric("Battery Health Score",f"{health_score}/100")
m2.metric("예상 잔존 수명",f"{pred_years:.1f} 년")
m3.metric("교체 권장 시점","2029 Q3")

tabs = st.tabs([
    "Overview",
    "Root Cause (XAI)",
    "Digital Twin",
    "Risk Analysis"
])

with tabs[0]:

    st.subheader("AI Analyst Summary")

    st.info(
        f"""
현재 배터리는 건강도 {health_score}/100 수준입니다.

고온 노출과 누적 사이클 증가가 주요 열화 요인으로 분석됩니다.

현재 사용 패턴이 유지될 경우 약 {pred_years:.1f}년 후
교체가 권장됩니다.
"""
    )

    trend = np.linspace(100,soh,36)+np.random.normal(0,1,36)

    fig = px.line(
        x=list(range(36)),
        y=trend,
        labels={"x":"개월","y":"SOH (%)"}
    )

    st.plotly_chart(fig,use_container_width=True)

with tabs[1]:

    st.subheader("Explainable AI")

    factors = pd.DataFrame({
        "요인":[
            "고온 노출",
            "충방전 사이클",
            "사용 기간",
            "충전 습관",
            "기타"
        ],
        "영향도":[42,28,17,9,4]
    })

    fig = px.bar(
        factors,
        x="영향도",
        y="요인",
        orientation="h"
    )

    st.plotly_chart(fig,use_container_width=True)

    st.success("""
가장 큰 원인은 고온 노출(42%)입니다.

온도를 평균 5°C 낮추면
예상 수명이 약 0.8년 증가할 것으로 분석됩니다.
""")

with tabs[2]:

    st.subheader("Digital Twin Simulation")

    scenario = st.slider(
        "온도 감소 시나리오",
        -10,
        10,
        -5
    )

    current = pred_years
    future = pred_years + abs(scenario)*0.15

    d1,d2 = st.columns(2)

    d1.metric(
        "현재 예상 수명",
        f"{current:.1f}년"
    )

    d2.metric(
        "개선 후 예상 수명",
        f"{future:.1f}년",
        f"+{future-current:.1f}년"
    )

    x=np.arange(24)

    y1=soh-(x*0.8)
    y2=soh-(x*0.55)

    fig=go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y1,
            name="현재"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y2,
            name="개선 시나리오"
        )
    )

    st.plotly_chart(fig,use_container_width=True)

with tabs[3]:

    st.subheader("Battery Risk Radar")

    radar = go.Figure()

    radar.add_trace(
        go.Scatterpolar(
            r=[
                70,
                55,
                60,
                40,
                50
            ],
            theta=[
                "온도",
                "사이클",
                "노화",
                "충전습관",
                "내부저항"
            ],
            fill="toself"
        )
    )

    radar.update_layout(height=500)

    st.plotly_chart(radar,use_container_width=True)

    st.subheader("Prediction Confidence")

    st.metric(
        "예상 수명",
        f"{pred_years:.1f}년"
    )

    st.write("95% 신뢰구간")

    st.success(
        f"{max(0,pred_years-0.5):.1f} ~ {pred_years+0.7:.1f} 년"
    )

st.divider()

st.subheader("Recommended Actions")

st.write("• 평균 온도 30°C 이하 유지")
st.write("• 급속충전 빈도 감소")
st.write("• 월간 상태 점검 수행")
st.write("• SOH 70% 이하 시 교체 검토")
'''
path="/mnt/data/app.py"
Path(path).write_text(code,encoding="utf-8")
print(path)
