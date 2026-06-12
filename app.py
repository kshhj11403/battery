import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.ensemble import IsolationForest
import time
import random

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="배터리 AI 클라우드 플랫폼",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed" # 사이드바 기본 숨김
)

# ==========================================
# 2. ADVANCED CSS (모던 & 깔끔한 UI 설정)
# ==========================================
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

html, body, [class*="css"] {
    font-family: 'Pretendard', sans-serif;
}

/* 세련된 다크 그라데이션 배경 */
.stApp {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}

.main-title {
    font-size: 2.5rem;
    font-weight: 800;
    text-align: center;
    color: #f8fafc;
    margin-top: 10px;
    margin-bottom: 30px;
    letter-spacing: -1px;
    text-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
}

.section-header {
    font-size: 1.2rem;
    font-weight: 700;
    color: #38bdf8;
    margin-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 5px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. TITLE & CONTROL CENTER (중앙 상단 배치)
# ==========================================
st.markdown("<div class='main-title'>⚡ 통합 배터리 AI 대시보드</div>", unsafe_allow_html=True)

st.markdown("<div class='section-header'>🎛️ 시뮬레이션 제어 패널</div>", unsafe_allow_html=True)

# 2줄로 나누어 슬라이더 배치 (가시성 극대화)
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns(3)
with ctrl_col1:
    cycle = st.slider("충방전 사이클 (Cycle)", 0, 5000, 800, help="현재까지 진행된 배터리 충방전 횟수")
with ctrl_col2:
    temp = st.slider("셀 평균 온도 (°C)", 10, 70, 28, help="배터리 팩의 현재 온도")
with ctrl_col3:
    ir = st.slider("내부 저항 (Ω)", 0.01, 0.08, 0.025, step=0.005, help="열화 수준을 나타내는 내부 저항값")

ctrl_col4, ctrl_col5 = st.columns(2)
with ctrl_col4:
    qc = st.slider("충전 용량 (Ah)", 0.5, 2.0, 1.25)
with ctrl_col5:
    qd = st.slider("방전 용량 (Ah)", 0.5, 2.0, 1.18)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 4. HEALTH ENGINE (전문 분석 엔진)
# ==========================================
soh = max(40, 100 - (cycle * 0.015))
soc = np.clip(80 + np.random.normal(0, 3), 0, 100)
rul = int(max(0, 4000 - cycle))
health_score = (soh * 0.5) + (100 - ir * 1000) * 0.3 + (100 - abs(temp - 25)) * 0.2

grade = "A (안전)"
grade_color = "normal"
if health_score < 80: 
    grade = "B (주의)"
if health_score < 60: 
    grade = "C (위험)"
    grade_color = "inverse"

# ==========================================
# 5. KPI DASHBOARD
# ==========================================
st.markdown("<div class='section-header'>📊 핵심 상태 지표 (KPI)</div>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("SOH (잔존 건강도)", f"{soh:.1f}%", "-0.2%")
kpi2.metric("SOC (현재 충전량)", f"{soc:.1f}%", "+1.3%")
kpi3.metric("RUL (예상 잔여 수명)", f"{rul:,} Cycles")
kpi4.metric("종합 시스템 등급", grade, delta_color=grade_color)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 6. TWO-TAB SYSTEM (직관적인 2-Tab 구조)
# ==========================================
tab1, tab2 = st.tabs(["🟢 실시간 모니터링", "🧠 AI 심층 분석 & 예측"])

# ------------------------------------------
# TAB 1: 실시간 모니터링 (디지털 트윈 & 팩 히트맵)
# ------------------------------------------
with tab1:
    mon_col1, mon_col2 = st.columns([1.2, 1])
    
    with mon_col1:
        st.subheader("🌐 실시간 디지털 트윈")
        st.write("SOH 열화 트렌드 및 온도 변화를 실시간으로 추적합니다.")
        
        start_stream = st.button("▶ 스트리밍 시작")
        chart_area = st.empty()

        if start_stream:
            cycles, preds, temps = [], [], []
            for i in range(40):
                cycles.append(cycle + i)
                preds.append(soh - i * 0.08 + np.random.normal(0, 0.4))
                temps.append(temp + np.random.normal(0, 1))

                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.add_trace(go.Scatter(x=cycles, y=preds, mode="lines+markers", name="SOH (%)", line=dict(color="#00ff99")), secondary_y=False)
                fig.add_trace(go.Scatter(x=cycles, y=temps, mode="lines", name="온도 (°C)", line=dict(color="#ff9900", dash="dot")), secondary_y=True)

                fig.update_layout(template="plotly_dark", height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10))
                chart_area.plotly_chart(fig, use_container_width=True)
                time.sleep(0.08)
        else:
            # Placeholder chart before streaming
            fig_placeholder = go.Figure().update_layout(template="plotly_dark", height=400, paper_bgcolor="rgba(0,0,0,0.05)", annotations=[dict(text="스트리밍 대기 중...", showarrow=False, font=dict(size=20, color="gray"))])
            chart_area.plotly_chart(fig_placeholder, use_container_width=True)

    with mon_col2:
        st.subheader("🔋 배터리 팩 열화상 히트맵")
        st.write("셀(Cell) 단위의 국부적 발열(Hot-spot)을 모니터링합니다.")
        
        heat = np.random.uniform(20, 40, (8, 12))
        heat[random.randint(0, 7)][random.randint(0, 11)] += 25 # 이상 발열 모사
        
        fig_heat = px.imshow(heat, color_continuous_scale="Turbo", text_auto=".1f", labels=dict(color="온도 (°C)"))
        fig_heat.update_layout(template="plotly_dark", height=400, margin=dict(t=10, b=10), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_heat, use_container_width=True)

# ------------------------------------------
# TAB 2: AI 심층 분석 (수명 예측, 이상 탐지, XAI)
# ------------------------------------------
with tab2:
    ai_col1, ai_col2 = st.columns(2)
    
    with ai_col1:
        st.subheader("📈 확률적 RUL 예측 (Monte Carlo)")
        future_x = np.linspace(cycle, cycle + 1500, 100)
        all_paths = []
        for _ in range(50):
            path = [soh - (fc - cycle) * np.random.normal(0.015, 0.005) + np.random.normal(0, 0.5) for fc in future_x]
            all_paths.append(path)
            
        all_paths = np.array(all_paths)
        mean_path = np.mean(all_paths, axis=0)
        
        fig_mc = go.Figure()
        for p in all_paths:
            fig_mc.add_trace(go.Scatter(x=future_x, y=p, mode="lines", line=dict(width=1, color="rgba(0,255,255,0.05)"), showlegend=False))
        fig_mc.add_trace(go.Scatter(x=future_x, y=mean_path, mode="lines", line=dict(color="#ff3366", width=3), name="예상 평균 SOH"))
        fig_mc.update_layout(template="plotly_dark", height=350, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10))
        st.plotly_chart(fig_mc, use_container_width=True)

    with ai_col2:
        st.subheader("🚨 AI 다차원 이상 탐지")
        # 합성 데이터 및 Isolation Forest
        data = pd.DataFrame({
            "temperature": np.concatenate([np.random.normal(temp, 2, 200), np.random.uniform(50, 80, 5)]),
            "ir": np.concatenate([np.random.normal(ir, 0.003, 200), np.random.uniform(0.05, 0.09, 5)])
        })
        detector = IsolationForest(contamination=0.03, random_state=42)
        data["status"] = np.where(detector.fit_predict(data) == -1, "이상", "정상")
        
        fig_anomaly = px.scatter(data, x="temperature", y="ir", color="status",
                                 color_discrete_map={"정상": "#38bdf8", "이상": "#ef4444"})
        fig_anomaly.update_layout(template="plotly_dark", height=350, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10))
        st.plotly_chart(fig_anomaly, use_container_width=True)

    st.markdown("---")
    
    # XAI & Risk Gauge
    xai_col1, xai_col2 = st.columns(2)
    
    with xai_col1:
        st.subheader("🧠 XAI: 주요 열화 요인 기여도")
        contrib = pd.DataFrame({"Feature": ["Cycle", "Temp", "IR", "QC", "QD"], "Contribution": [-12, -4, -8, +5, +3]})
        fig_water = go.Figure(go.Bar(
            x=contrib["Feature"], y=contrib["Contribution"], text=contrib["Contribution"], textposition="auto",
            marker_color=["#ef4444" if x < 0 else "#22c55e" for x in contrib["Contribution"]]
        ))
        fig_water.update_layout(template="plotly_dark", height=300, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10))
        st.plotly_chart(fig_water, use_container_width=True)

    with xai_col2:
        st.subheader("위험도 평가 지수 (Risk Index)")
        risk_value = np.clip(100 - health_score, 0, 100)
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=risk_value,
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar": {"color": "rgba(0,0,0,0)"},
                "steps": [{"range": [0, 40], "color": "#22c55e"}, {"range": [40, 70], "color": "#f59e0b"}, {"range": [70, 100], "color": "#ef4444"}],
                "threshold": {"line": {"color": "white", "width": 4}, "thickness": 0.75, "value": risk_value}
            }
        ))
        gauge.update_layout(template="plotly_dark", height=300, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10))
        st.plotly_chart(gauge, use_container_width=True)
