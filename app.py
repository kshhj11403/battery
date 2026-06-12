import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.ensemble import IsolationForest
import time
import random
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="배터리 AI 클라우드 플랫폼",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ADVANCED CSS (모던 & 깔끔한 UI 설정)
# ==========================================
st.markdown("""
<style>
/* 트렌디하고 가독성 높은 Pretendard 폰트 적용 */
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

html, body, [class*="css"] {
    font-family: 'Pretendard', sans-serif;
}

/* 세련된 다크 그라데이션 배경 */
.stApp {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}

.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    text-align: center;
    color: #f8fafc;
    margin-bottom: 30px;
    letter-spacing: -1px;
    text-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
}

.glass-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. TITLE
# ==========================================
st.markdown("<div class='main-title'>⚡ 배터리 AI 클라우드 플랫폼</div>", unsafe_allow_html=True)

# ==========================================
# 4. SIDEBAR (제어 센터)
# ==========================================
with st.sidebar:
    st.header("🎛️ 시뮬레이션 제어 센터")
    st.markdown("배터리의 상태 변수를 조작하여<br>AI 모델의 반응을 확인하세요.", unsafe_allow_html=True)
    st.markdown("---")
    
    cycle = st.slider("충방전 사이클 (Cycle)", 0, 5000, 800, help="현재까지 진행된 배터리 충/방전 횟수입니다.")
    temp = st.slider("셀 온도 (Temperature, °C)", 10, 70, 28, help="배터리 팩의 현재 평균 온도입니다.")
    ir = st.slider("내부 저항 (Internal Resistance, Ω)", 0.01, 0.08, 0.025, step=0.005, help="노화가 진행될수록 내부 저항이 증가합니다.")
    qc = st.slider("충전 용량 (Charge Capacity, Ah)", 0.5, 2.0, 1.25)
    qd = st.slider("방전 용량 (Discharge Capacity, Ah)", 0.5, 2.0, 1.18)

# ==========================================
# 5. HEALTH ENGINE (전문 분석 엔진)
# ==========================================
# SOH (State of Health): 배터리 잔존 수명 비율
soh = max(40, 100 - (cycle * 0.015))

# SOC (State of Charge): 현재 충전 상태
soc = np.clip(80 + np.random.normal(0, 3), 0, 100)

# RUL (Remaining Useful Life): 잔존 유효 사이클 수
rul = int(max(0, 4000 - cycle))

# 종합 건강도 점수 (Health Score)
health_score = (soh * 0.5) + (100 - ir * 1000) * 0.3 + (100 - abs(temp - 25)) * 0.2

grade = "A (최상)"
if health_score < 80: grade = "B (주의)"
if health_score < 60: grade = "C (위험)"

# ==========================================
# 6. KPI DASHBOARD
# ==========================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("SOH (건강 상태)", f"{soh:.1f}%", "-0.2%", help="초기 용량 대비 현재 배터리의 잔존 용량 비율입니다.")
with c2:
    st.metric("SOC (충전 상태)", f"{soc:.1f}%", "+1.3%", help="현재 배터리에 충전되어 있는 에너지의 비율입니다.")
with c3:
    st.metric("RUL (예측 잔존 수명)", f"{rul:,} Cycles", help="배터리 수명이 다할 때까지 남은 예상 사이클 횟수입니다.")
with c4:
    st.metric("종합 건강 등급", grade)

st.markdown("---")

# ==========================================
# 7. TABS NAVIGATION
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌐 실시간 라이브 트윈", 
    "🔋 배터리 팩 모니터링", 
    "📈 RUL 수명 예측", 
    "🚨 AI 이상 탐지", 
    "🧠 XAI 분석 및 코파일럿"
])

# ==========================================
# TAB 1: 실시간 트윈 (Live Twin)
# ==========================================
with tab1:
    st.subheader("🌐 실시간 디지털 트윈 (Real-Time Digital Twin)")
    st.write("배터리 셀의 SOH 열화 트렌드와 온도 변화를 실시간 스트리밍으로 추적합니다.")
    
    start = st.button("▶ 실시간 스트리밍 시작")
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
            fig.add_trace(
                go.Scatter(x=cycles, y=preds, mode="lines+markers", name="SOH (%)", line=dict(color="#00ff99")),
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=cycles, y=temps, mode="lines", name="온도 (°C)", line=dict(color="#ff9900", dash="dot")),
                secondary_y=True
            )

            fig.update_layout(
                template="plotly_dark", 
                height=450, 
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor="rgba(0,0,0,0)", 
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            chart_area.plotly_chart(fig, use_container_width=True)
            time.sleep(0.08)

# ==========================================
# TAB 2: 배터리 팩 모니터링 (Battery Pack Heatmap)
# ==========================================
with tab2:
    st.subheader("🔋 배터리 팩 열화상 히트맵")
    st.write("팩 내부의 개별 셀(Cell) 온도를 시각화하여 국부적인 발열(Hot-spot)을 모니터링합니다.")
    
    rows, cols = 8, 12
    heat = np.random.uniform(20, 40, (rows, cols))
    
    # 핫스팟 생성 (이상 발열 현상 모사)
    heat[random.randint(0, 7)][random.randint(0, 11)] += 25

    fig_heat = px.imshow(
        heat, 
        color_continuous_scale="Turbo", 
        text_auto=".1f",
        labels=dict(color="온도 (°C)")
    )
    fig_heat.update_layout(template="plotly_dark", height=500, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_heat, use_container_width=True)

# ==========================================
# TAB 3: RUL 수명 예측 (Forecast Engine)
# ==========================================
with tab3:
    st.subheader("📈 확률적 몬테카를로 수명 예측 (Monte Carlo SOH Forecasting)")
    
    colA, colB = st.columns([1, 4])
    with colA:
        simulation_count = st.slider("시뮬레이션 경로 수", 10, 200, 100)
        forecast_cycles = st.slider("미래 예측 사이클", 100, 3000, 1000)
        degradation_noise = st.slider("불확실성(노이즈) 계수", 0.01, 0.30, 0.08)
        run_forecast = st.button("시뮬레이션 실행")

    with colB:
        if run_forecast:
            future_x = np.linspace(cycle, cycle + forecast_cycles, 120)
            fig_mc = go.Figure()
            all_paths = []

            for p in range(simulation_count):
                path = []
                base_deg = np.random.normal(0.015, degradation_noise)
                random_walk = 0
                for fc in future_x:
                    random_walk += np.random.normal(0, degradation_noise)
                    pred = soh - (fc - cycle) * base_deg + random_walk
                    path.append(pred)
                all_paths.append(path)
                
                fig_mc.add_trace(go.Scatter(x=future_x, y=path, mode="lines", line=dict(width=1, color="rgba(0,255,255,0.05)"), showlegend=False))

            all_paths = np.array(all_paths)
            mean_path = np.mean(all_paths, axis=0)
            upper = np.percentile(all_paths, 95, axis=0)
            lower = np.percentile(all_paths, 5, axis=0)

            fig_mc.add_trace(go.Scatter(x=future_x, y=mean_path, mode="lines", line=dict(color="#ff3366", width=4), name="예상 수명 경로(Mean)"))
            fig_mc.add_trace(go.Scatter(
                x=np.concatenate([future_x, future_x[::-1]]),
                y=np.concatenate([upper, lower[::-1]]),
                fill="toself", fillcolor="rgba(255,51,102,0.15)", line=dict(color="rgba(255,255,255,0)"), name="95% 신뢰구간"
            ))

            fig_mc.update_layout(template="plotly_dark", height=450, paper_bgcolor="rgba(0,0,0,0)", xaxis_title="사이클", yaxis_title="SOH (%)")
            st.plotly_chart(fig_mc, use_container_width=True)

            # RUL 분석 결과
            end_soh = mean_path[-1]
            risk = "낮음 (안정)" if end_soh >= 80 else "보통 (주의)" if end_soh >= 60 else "높음 (위험)"

            st.markdown("#### 📊 예측 시나리오 요약")
            r1, r2, r3 = st.columns(3)
            r1.metric("목표 도달 시 예상 SOH", f"{end_soh:.1f}%")
            r2.metric("예측 기반 RUL", f"{rul} Cycles")
            r3.metric("최종 위험도 수준", risk)

            if health_score > 85: st.success("🟢 배터리 상태가 안정적입니다. 여유 있는 잔존 수명이 확보되어 있습니다.")
            elif health_score > 65: st.warning("🟡 배터리 열화가 진행되고 있습니다. 사용 패턴 최적화가 필요할 수 있습니다.")
            else: st.error("🔴 배터리가 한계 수명에 근접했습니다. 조기 교체 및 정밀 점검을 권장합니다.")

# ==========================================
# TAB 4: AI 이상 탐지 (Anomaly Detection)
# ==========================================
with tab4:
    st.subheader("🚨 Isolation Forest 다차원 이상 탐지 시스템")
    st.write("머신러닝 기반 무감독 학습 알고리즘(Isolation Forest)을 통해 정상 군집에서 벗어난 잠재적 고장 인자를 탐지합니다.")

    # 합성 데이터 생성
    normal_data = pd.DataFrame({
        "temperature": np.random.normal(temp, 2, 300),
        "ir": np.random.normal(ir, 0.003, 300),
        "cycle": np.random.normal(cycle, 50, 300)
    })
    anomaly_data = pd.DataFrame({
        "temperature": np.random.uniform(50, 80, 10),
        "ir": np.random.uniform(0.05, 0.09, 10),
        "cycle": np.random.uniform(cycle, cycle + 500, 10)
    })
    data = pd.concat([normal_data, anomaly_data], ignore_index=True)

    # 이상 탐지 모델 적용
    detector = IsolationForest(contamination=0.03, random_state=42)
    data["anomaly"] = detector.fit_predict(data)
    data["status"] = np.where(data["anomaly"] == -1, "이상 (Anomaly)", "정상 (Normal)")

    col1, col2 = st.columns([3, 2])
    
    with col1:
        fig_anomaly = px.scatter(
            data, x="temperature", y="ir", color="status",
            color_discrete_map={"정상 (Normal)": "#38bdf8", "이상 (Anomaly)": "#ef4444"},
            labels={"temperature": "온도 (°C)", "ir": "내부 저항 (Ω)"},
            size_max=12
        )
        fig_anomaly.update_layout(template="plotly_dark", height=450, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_anomaly, use_container_width=True)

    with col2:
        st.markdown("#### ⚠️ 실시간 경고 센터")
        alerts = []
        if temp > 45: alerts.append("고온 상태 감지됨 (냉방 시스템 점검 요망)")
        if ir > 0.04: alerts.append("내부 저항 급증 (열화 가속화 가능성)")
        if soh < 70: alerts.append("SOH 위험 임계치 도달 (배터리 성능 저하)")

        if not alerts:
            st.success("✅ 현재 발생한 활성 경고가 없습니다.")
        else:
            for alert in alerts:
                st.error(f"🚨 {alert}")
                
        st.markdown("#### 📋 주요 이상 데이터 로그")
        st.dataframe(data[data["status"] == "이상 (Anomaly)"].drop(columns=['anomaly']).head(), use_container_width=True)

# ==========================================
# TAB 5: XAI 분석 및 코파일럿 (Explainable AI & Risk)
# ==========================================
with tab5:
    st.subheader("🧠 설명 가능한 AI (XAI) 대시보드")
    st.write("AI 모델이 해당 배터리의 건강 상태(SOH)를 평가할 때, 어떤 변수들이 가장 큰 영향을 미쳤는지 직관적으로 설명합니다.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 변수 중요도 (Feature Importance)")
        feature_importance = pd.DataFrame({
            "Feature": ["Cycle (충방전 횟수)", "Temperature (온도)", "IR (내부 저항)", "QC (충전 용량)", "QD (방전 용량)"],
            "Importance": [0.42, 0.23, 0.18, 0.09, 0.08]
        })
        fig_imp = px.bar(
            feature_importance, x="Importance", y="Feature", orientation="h",
            color="Importance", color_continuous_scale="Teal"
        )
        fig_imp.update_layout(template="plotly_dark", height=350, paper_bgcolor="rgba(0,0,0,0)", yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_imp, use_container_width=True)

    with col2:
        st.markdown("#### 현재 SOH 기여도 요인 (SHAP Contribution)")
        contrib = pd.DataFrame({
            "Feature": ["Cycle", "Temp", "IR", "QC", "QD"],
            "Contribution": [-12, -4, -8, +5, +3]
        })
        fig_water = go.Figure(go.Bar(
            x=contrib["Feature"], y=contrib["Contribution"],
            text=contrib["Contribution"], textposition="auto",
            marker_color=["#ef4444" if x < 0 else "#22c55e" for x in contrib["Contribution"]]
        ))
        fig_water.update_layout(template="plotly_dark", height=350, paper_bgcolor="rgba(0,0,0,0)", yaxis_title="영향도 (점수)")
        st.plotly_chart(fig_water, use_container_width=True)

    st.markdown("---")
    
    st.markdown("#### 🚨 종합 배터리 고장 위험도 (Risk Index)")
    risk_value = np.clip(100 - health_score, 0, 100)

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_value,
        title={"text": "배터리 고장 위험도 지수 (%)", "font": {"size": 24}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "white"},
            "bar": {"color": "rgba(0,0,0,0)"}, # 바 숨기고 포인터 사용 가능, 여기선 심플 유지
            "steps": [
                {"range": [0, 40], "color": "#22c55e"},
                {"range": [40, 70], "color": "#f59e0b"},
                {"range": [70, 100], "color": "#ef4444"}
            ],
            "threshold": {
                "line": {"color": "white", "width": 4},
                "thickness": 0.75,
                "value": risk_value
            }
        }
    ))
    gauge.update_layout(template="plotly_dark", height=350, paper_bgcolor="rgba(0,0,0,0)")
    
    # 레이아웃을 중앙 정렬하기 위해 컬럼 활용
    _, g_col, _ = st.columns([1, 2, 1])
    with g_col:
        st.plotly_chart(gauge, use_container_width=True)
