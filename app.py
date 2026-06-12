import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from sklearn.ensemble import IsolationForest
import time
import random
from datetime import datetime

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="지능형 배터리 관제 플랫폼",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# ADVANCED CSS
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Orbitron:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', 'Orbitron', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #030712 0%, #0f172a 100%);
}

.main-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    text-align: center;
    color: white;
    margin-bottom: 5px;
    text-shadow: 0 0 10px cyan, 0 0 20px cyan;
}

.sub-title {
    text-align: center;
    color: #94a3b8;
    font-size: 1.1rem;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# TITLE
# ==========================================

st.markdown("<div class='main-title'>⚡ AI BATTERY CLOUD</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>실시간 배터리 상태 모니터링 및 AI 기반 수명 예측 플랫폼</div>", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.header("🎛️ 시뮬레이션 환경 설정")
    st.caption("배터리의 현재 상태값을 조정하여 AI의 예측 변화를 확인하세요.")

    cycle = st.slider("현재 충방전 사이클 (Cycles)", 0, 5000, 800)
    temp = st.slider("배터리 온도 (°C)", 10, 70, 28)
    ir = st.slider("내부 저항 (mΩ)", 0.01, 0.08, 0.025)
    qc = st.slider("충전 용량 비율", 0.5, 2.0, 1.25)
    qd = st.slider("방전 용량 비율", 0.5, 2.0, 1.18)

# ==========================================
# HEALTH ENGINE
# ==========================================

soh = max(40, 100 - (cycle * 0.015))
soc = np.clip(80 + np.random.normal(0, 3), 0, 100)
rul = int(max(0, 4000 - cycle))

health_score = (soh * 0.5) + (100 - ir * 1000) * 0.3 + (100 - abs(temp - 25)) * 0.2

# ==========================================
# KPI DASHBOARD
# ==========================================

st.markdown("### 📊 핵심 성능 지표 (KPI)")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("건강 상태 (SOH)", f"{soh:.1f}%", "-0.2% (전일 대비)", delta_color="normal")
with c2:
    st.metric("현재 충전량 (SOC)", f"{soc:.1f}%", "+1.3% (충전 중)", delta_color="normal")
with c3:
    st.metric("예상 잔존 수명 (RUL)", f"{rul} Cycles")
with c4:
    grade = "A 등급 (최상)" if health_score >= 80 else "B 등급 (양호)" if health_score >= 60 else "C 등급 (점검 요망)"
    st.metric("종합 시스템 등급", grade)

st.markdown("---")

# ==========================================
# TABS
# ==========================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📡 라이브 트윈", 
    "🔋 배터리 팩 분석", 
    "🔮 수명 예측", 
    "🚨 이상 탐지", 
    "🤖 AI 코파일럿"
])

# ==========================================
# TAB 1: 라이브 트윈 (스트리밍 + 3D)
# ==========================================
with tab1:
    st.subheader("📡 실시간 2D/3D 디지털 트윈")
    st.info("물리적 배터리의 상태를 가상 공간에 실시간으로 동기화하여 시각적으로 모니터링합니다.")

    start = st.button("▶ 실시간 스트림 시작")
    chart_area = st.empty()

    if start:
        cycles, preds, temps = [], [], []
        for i in range(50):
            current_cycle = cycle + i
            current_temp = temp + np.random.normal(0, 1)
            prediction = soh - i * 0.08 + np.random.normal(0, 0.4)

            cycles.append(current_cycle)
            preds.append(prediction)
            temps.append(current_temp)

            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=cycles, y=preds, mode="lines", name="SOH (%)", line=dict(color="#00ff99")), secondary_y=False)
            fig.add_trace(go.Scatter(x=cycles, y=temps, mode="lines", name="온도 (°C)", line=dict(color="#ff4b4b")), secondary_y=True)

            fig.update_layout(template="plotly_dark", height=450, margin=dict(t=30, b=0))
            chart_area.plotly_chart(fig, use_container_width=True)
            time.sleep(0.1)

    st.markdown("---")
    st.markdown("#### 🌐 3D 상태 매핑 모델")
    st.caption("사이클, 온도, 건강 상태(SOH)의 3차원 상관관계를 분석하여 배터리의 구조적 안정성을 파악합니다.")

    sample_size = 250
    twin_df = pd.DataFrame({
        "사이클": np.random.randint(cycle, cycle + 1000, sample_size),
        "온도": np.random.normal(temp, 4, sample_size),
        "SOH": np.random.normal(soh, 5, sample_size)
    })

    fig3d = px.scatter_3d(twin_df, x="사이클", y="온도", z="SOH", color="SOH", color_continuous_scale="Turbo", opacity=0.8)
    fig3d.update_layout(template="plotly_dark", height=600, margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig3d, use_container_width=True)

# ==========================================
# TAB 2: 배터리 팩 분석 (열화상 + 셀 랭킹)
# ==========================================
with tab2:
    st.subheader("🌡️ 배터리 팩 내부 상태 심층 분석")
    
    st.markdown("#### 1️⃣ 셀 열화상 매핑 (Heatmap)")
    st.info("96개 개별 셀의 온도 분포입니다. 붉은색에 가까울수록 국소적 열 폭주 위험이 높습니다.")
    
    rows, cols = 8, 12
    heat = np.random.uniform(20, 40, (rows, cols))
    heat[random.randint(0, 7)][random.randint(0, 11)] += 20

    fig_heat = px.imshow(heat, color_continuous_scale="Turbo", text_auto=".1f", labels=dict(color="온도 (°C)"))
    fig_heat.update_layout(template="plotly_dark", height=500)
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 2️⃣ 개별 셀 건강 상태(SOH) 랭킹 및 분포")
    st.caption("전체 셀 중 가장 성능이 저하된 셀(Weakest Link)을 추적하여 선제적 교체 계획을 수립하세요.")

    cells = []
    for i in range(96):
        cells.append({
            "셀 번호": f"CELL-{i+1}",
            "SOH (%)": np.random.uniform(65, 100),
            "온도 (°C)": np.random.uniform(20, 45),
            "내부 저항 (mΩ)": np.random.uniform(0.01, 0.06)
        })

    fleet = pd.DataFrame(cells)
    fleet["종합 점수"] = (fleet["SOH (%)"] * 0.6) + (100 - fleet["내부 저항 (mΩ)"] * 1000) * 0.3 + (100 - fleet["온도 (°C)"]) * 0.1
    fleet = fleet.sort_values("종합 점수", ascending=False)

    colA, colB = st.columns([1, 1])
    with colA:
        st.dataframe(fleet.head(10), use_container_width=True)
    with colB:
        fig_hist = px.histogram(fleet, x="SOH (%)", nbins=25, color_discrete_sequence=["cyan"], title="배터리 팩 SOH 분포도")
        fig_hist.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_hist, use_container_width=True)

# ==========================================
# TAB 3: 수명 예측 (Monte Carlo + Failure Map)
# ==========================================
with tab3:
    st.subheader("🔮 고도화된 수명 예측 엔진")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("**시뮬레이션 파라미터**")
        simulation_count = st.slider("시뮬레이션 경로 수", 10, 200, 100)
        forecast_cycles = st.slider("예측 범위 (Cycles)", 100, 3000, 1000)
        degradation_noise = st.slider("열화 노이즈 (불확실성)", 0.01, 0.30, 0.08)
        run_forecast = st.button("▶ 몬테카를로 분석 실행")

    with col2:
        if run_forecast:
            future_x = np.linspace(cycle, cycle + forecast_cycles, 120)
            fig_mc = go.Figure()
            all_paths = []

            for p in range(simulation_count):
                path = []
                base_degradation = np.random.normal(0.015, degradation_noise)
                random_walk = 0
                for fc in future_x:
                    random_walk += np.random.normal(0, degradation_noise)
                    pred = soh - (fc - cycle) * base_degradation + random_walk
                    path.append(pred)
                all_paths.append(path)

                fig_mc.add_trace(go.Scatter(x=future_x, y=path, mode="lines", line=dict(width=1, color="rgba(0,255,255,0.08)"), showlegend=False))

            all_paths = np.array(all_paths)
            mean_path = np.mean(all_paths, axis=0)
            upper = np.percentile(all_paths, 95, axis=0)
            lower = np.percentile(all_paths, 5, axis=0)

            fig_mc.add_trace(go.Scatter(x=future_x, y=mean_path, mode="lines", line=dict(color="magenta", width=5), name="기대 수명 경로"))
            fig_mc.add_trace(go.Scatter(
                x=np.concatenate([future_x, future_x[::-1]]), 
                y=np.concatenate([upper, lower[::-1]]),
                fill="toself", fillcolor="rgba(255,0,255,0.15)", line=dict(color="rgba(255,0,255,0)"), name="95% 신뢰구간"
            ))

            fig_mc.update_layout(template="plotly_dark", height=500, title="Monte Carlo 수명 시뮬레이션")
            st.plotly_chart(fig_mc, use_container_width=True)

            st.markdown("---")
            r1, r2, r3 = st.columns(3)
            end_soh = mean_path[-1]
            risk = "높음 (HIGH)" if end_soh < 60 else "주의 (MEDIUM)" if end_soh < 80 else "안전 (LOW)"
            
            with r1: st.metric("목표 시점 예상 SOH", f"{end_soh:.1f}%")
            with r2: st.metric("총 예상 잔존 수명", f"{rul} Cycles")
            with r3: st.metric("시스템 운영 위험도", risk)

    st.markdown("---")
    st.markdown("#### 📉 사이클에 따른 고장 확률 맵")
    failure_cycle = np.arange(cycle, cycle + 2000, 25)
    failure_probability = [max(0, min(95, ((fc - cycle) / 2000) * 100) + np.random.normal(0, 3)) for fc in failure_cycle]

    fig_fail = go.Figure(go.Scatter(x=failure_cycle, y=failure_probability, fill="tozeroy", line=dict(width=4, color="red"), name="고장 위험 확률"))
    fig_fail.update_layout(template="plotly_dark", height=400, yaxis_title="확률 (%)", xaxis_title="예상 사이클")
    st.plotly_chart(fig_fail, use_container_width=True)

# ==========================================
# TAB 4: 이상 탐지 (Anomaly & Alerts)
# ==========================================
with tab4:
    st.subheader("🚨 머신러닝 기반 다차원 이상 징후 탐지")
    st.info("Isolation Forest 알고리즘을 활용하여 정상 범주를 벗어난 센서 데이터(온도, 저항, 사이클 등)를 실시간으로 식별합니다.")

    # Synthetic Data
    normal_data = pd.DataFrame({
        "온도": np.random.normal(temp, 2, 300),
        "내부저항": np.random.normal(ir, 0.003, 300),
        "사이클": np.random.normal(cycle, 50, 300)
    })
    anomaly_data = pd.DataFrame({
        "온도": np.random.uniform(50, 80, 10),
        "내부저항": np.random.uniform(0.05, 0.09, 10),
        "사이클": np.random.uniform(cycle, cycle + 500, 10)
    })
    data = pd.concat([normal_data, anomaly_data], ignore_index=True)

    # ML Anomaly Detection
    detector = IsolationForest(contamination=0.03, random_state=42)
    data["이상여부"] = detector.fit_predict(data)
    data["상태"] = np.where(data["이상여부"] == -1, "이상 징후 (Anomaly)", "정상 (Normal)")

    fig_anomaly = px.scatter(data, x="온도", y="내부저항", color="상태", color_discrete_map={"정상 (Normal)": "cyan", "이상 징후 (Anomaly)": "red"}, size_max=12)
    fig_anomaly.update_layout(template="plotly_dark", height=500)
    st.plotly_chart(fig_anomaly, use_container_width=True)

    colA, colB = st.columns([1, 1])
    with colA:
        st.markdown("#### 📋 비정상 데이터 로그")
        anomaly_rows = data[data["상태"] == "이상 징후 (Anomaly)"]
        st.dataframe(anomaly_rows.head(10)[["온도", "내부저항", "사이클"]], use_container_width=True)

    with colB:
        st.markdown("#### 🔔 활성 알람 센터 (Alerts)")
        alerts = []
        if temp > 45: alerts.append("🔥 배터리 과열 감지 (온도 45°C 초과)")
        if ir > 0.04: alerts.append("⚡ 내부 저항 수치 비정상적 상승")
        if soh < 70: alerts.append("📉 SOH 70% 미만 진입 (교체 권고)")

        if not alerts:
            st.success("✅ 현재 활성화된 시스템 경고가 없습니다.")
        else:
            for alert in alerts:
                st.error(alert)

# ==========================================
# TAB 5: AI 코파일럿 (XAI)
# ==========================================
with tab5:
    st.subheader("🤖 설명 가능한 AI (XAI) 대시보드")
    st.info("인공지능이 도출한 현재 배터리 상태 점수의 근거와 변수별 기여도를 투명하게 제공합니다.")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### 📌 노화 예측 중요도 (Feature Importance)")
        feature_importance = pd.DataFrame({
            "특성(Feature)": ["누적 사이클", "온도 노출", "내부 저항 (IR)", "충전 속도 (QC)", "방전 심도 (QD)"],
            "중요도": [0.42, 0.23, 0.18, 0.09, 0.08]
        })
        fig_imp = px.bar(feature_importance, x="중요도", y="특성(Feature)", orientation="h", color="중요도", color_continuous_scale="Turbo")
        fig_imp.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_imp, use_container_width=True)

    with c2:
        st.markdown("#### 📉 수명 증감 기여도 (Contribution Waterfall)")
        contrib = pd.DataFrame({
            "변수": ["초기 상태", "누적 사이클", "고온 스트레스", "저항 증가", "최적화 충전"],
            "영향력": [100, -12, -4, -8, +5]
        })
        fig_water = go.Figure(go.Bar(
            x=contrib["변수"], y=contrib["영향력"],
            marker_color=["gray", "red", "red", "red", "green"], text=contrib["영향력"], textposition="auto"
        ))
        fig_water.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_water, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🎛️ 종합 리스크 인디케이터")
    risk_value = np.clip(100 - health_score, 0, 100)
    
    gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=risk_value, title={"text": "현재 종합 리스크 지수"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "red" if risk_value > 70 else "orange" if risk_value > 40 else "green"},
            "steps": [
                {"range": [0, 40], "color": "rgba(0,255,0,0.2)"},
                {"range": [40, 70], "color": "rgba(255,165,0,0.2)"},
                {"range": [70, 100], "color": "rgba(255,0,0,0.2)"}
            ]
        }
    ))
    gauge.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(gauge, use_container_width=True)

    if health_score > 85:
        st.success("💡 **AI 진단 의견:** 배터리 상태가 매우 안정적입니다. 예상되는 잔존 수명이 길며 즉각적인 조치가 필요하지 않습니다.")
    elif health_score > 65:
        st.warning("💡 **AI 진단 의견:** 열화가 진행 중입니다. 주요 사용 패턴을 분석하고 온도를 적정 수준으로 유지할 것을 권장합니다.")
    else:
        st.error("💡 **AI 진단 의견:** 배터리가 임계치에 도달했습니다. 시스템 안정성을 위해 즉각적인 정밀 점검 또는 부품 교체가 필요합니다.")
