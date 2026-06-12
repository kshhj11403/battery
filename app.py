import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Battery Intelligence",
    page_icon="🔋",
    layout="centered", # 모던 웹서비스 느낌을 위해 centered 또는 좁은 여백 사용
    initial_sidebar_state="collapsed"
)

# ==========================================
# MODERN LIGHT CSS (Apple / Linear / Notion 스타일)
# ==========================================
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

html, body, [class*="css"] {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    color: #111827;
    background-color: #ffffff;
}

/* 상단 헤더 숨기기 */
header {visibility: hidden;}

/* 메인 타이틀 */
.service-title {
    font-size: 2rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 24px;
    letter-spacing: -0.02em;
}

/* 카드 UI */
.metric-container {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 32px;
}
.metric-card {
    flex: 1;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}
.metric-title {
    font-size: 0.875rem;
    font-weight: 600;
    color: #64748b;
    margin-bottom: 8px;
}
.metric-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.02em;
}
.metric-sub {
    font-size: 0.75rem;
    color: #3b82f6;
    margin-top: 4px;
    font-weight: 500;
}

/* AI Analyst Box */
.ai-insight-box {
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    border-radius: 0 8px 8px 0;
    padding: 20px 24px;
    margin-bottom: 40px;
}
.ai-insight-title {
    font-size: 1rem;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.ai-insight-text {
    font-size: 0.95rem;
    color: #1e40af;
    line-height: 1.6;
    margin: 0;
}
.highlight {
    font-weight: 700;
    color: #1d4ed8;
    background: #dbeafe;
    padding: 2px 6px;
    border-radius: 4px;
}

/* 섹션 타이틀 */
.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
    margin-top: 48px;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #f1f5f9;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# USER INPUTS (일반인/의사결정권자 맞춤형)
# ==========================================
st.markdown("<div class='service-title'>Battery Intelligence</div>", unsafe_allow_html=True)

with st.expander("⚙️ 배터리 사용 환경 설정 (시뮬레이션)", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        years_used = st.number_input("사용 기간 (년)", min_value=0.5, max_value=10.0, value=2.0, step=0.5)
    with col2:
        avg_temp = st.slider("주 평균 노출 온도 (°C)", 10, 50, 32)
    with col3:
        fast_charge_ratio = st.slider("급속 충전 빈도 (%)", 0, 100, 65)

# ==========================================
# ENGINE (백그라운드 계산 로직)
# ==========================================
# 기존의 Cycle, IR 등을 사용자 입력 기반으로 유추
estimated_cycles = years_used * 250
temp_stress = max(0, avg_temp - 25) * 0.8
fast_charge_stress = fast_charge_ratio * 0.15

# SOH 계산 (100% 시작)
soh_drop = (estimated_cycles * 0.012) + temp_stress + fast_charge_stress
current_soh = max(10, 100 - soh_drop)

# 수명 계산 (SOH 70%를 교체 주기로 가정)
degradation_rate_per_year = soh_drop / years_used if years_used > 0 else 5.0
years_to_replacement = max(0, (current_soh - 70) / degradation_rate_per_year)

# 교체 예상 분기 계산
now = datetime(2026, 6, 12)
replace_date = now + relativedelta(days=int(years_to_replacement * 365))
replace_quarter = f"{replace_date.year} Q{(replace_date.month-1)//3 + 1}"

# ==========================================
# 1. TOP 3 KPI CARDS
# ==========================================
st.markdown(f"""
<div class="metric-container">
    <div class="metric-card">
        <div class="metric-title">배터리 건강도</div>
        <div class="metric-value">{current_soh:.0f} / 100</div>
        <div class="metric-sub">{'안정적' if current_soh > 80 else '주의 필요'}</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">예상 교체 시점</div>
        <div class="metric-value">{replace_quarter if current_soh > 70 else '즉시 교체'}</div>
        <div class="metric-sub">수명 한계선(SOH 70%) 기준</div>
    </div>
    <div class="metric-card">
        <div class="metric-title">잔존 수명</div>
        <div class="metric-value">{years_to_replacement:.1f}년</div>
        <div class="metric-sub">현재 사용 패턴 유지 시</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 2. AI ANALYST INSIGHT
# ==========================================
# 가장 큰 원인 찾기
factors = {
    "고온 노출": temp_stress,
    "급속 충전": fast_charge_stress,
    "자연 노화(사용 기간)": (estimated_cycles * 0.012)
}
main_cause = max(factors, key=factors.get)

# 개선 시뮬레이션 계산
improved_temp = min(avg_temp, 25)
improved_temp_stress = max(0, improved_temp - 25) * 0.8
improved_soh_drop = (estimated_cycles * 0.012) + improved_temp_stress + fast_charge_stress
improved_deg_rate = improved_soh_drop / years_used
improved_years = max(0, (current_soh - 70) / improved_deg_rate) if improved_deg_rate > 0 else years_to_replacement
life_extension = improved_years - years_to_replacement

insight_msg = f"현재 배터리는 <b>{'양호한' if current_soh > 80 else '열화가 진행된'} 상태</b>입니다.<br>"
if current_soh > 70:
    insight_msg += f"수명 단축의 가장 큰 위험 요인은 <span class='highlight'>{main_cause}</span>입니다.<br>"
    if main_cause == "고온 노출":
        insight_msg += f"주차/운행 환경의 평균 온도를 <b>25°C 수준으로 낮추면</b> 교체 시기를 약 <span class='highlight'>{life_extension:.1f}년 연장</span>할 수 있습니다."
    elif main_cause == "급속 충전":
        insight_msg += f"완속 충전 비율을 늘리면 교체 시기를 유의미하게 연장할 수 있습니다."
else:
    insight_msg += "<span class='highlight'>배터리 교체 권장 주기(SOH 70%)에 도달했습니다.</span> 안전을 위해 점검 및 교체를 계획해 주세요."

st.markdown(f"""
<div class="ai-insight-box">
    <div class="ai-insight-title">✨ AI Analyst Insight</div>
    <p class="ai-insight-text">{insight_msg}</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. WHY? (XAI)
# ==========================================
st.markdown("<div class='section-title'>Why? 배터리 열화 원인 분석</div>", unsafe_allow_html=True)

total_stress = sum(factors.values())
xai_df = pd.DataFrame({
    "요인": list(factors.keys()),
    "기여도(%)": [(v / total_stress) * 100 for v in factors.values()]
}).sort_values(by="기여도(%)", ascending=True)

fig_xai = px.bar(
    xai_df, x="기여도(%)", y="요인", orientation='h',
    text=xai_df["기여도(%)"].apply(lambda x: f"{x:.1f}%")
)
fig_xai.update_traces(marker_color='#3b82f6', textposition='outside', textfont=dict(color='#475569'))
fig_xai.update_layout(
    template="plotly_white",
    height=250,
    margin=dict(l=0, r=40, t=20, b=0),
    xaxis=dict(showgrid=False, showticklabels=False, title=""),
    yaxis=dict(title="", tickfont=dict(size=14, color='#334155')),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_xai, use_container_width=True, config={'displayModeBar': False})

# ==========================================
# 4. DIGITAL TWIN (현재 vs 개선 후)
# ==========================================
st.markdown("<div class='section-title'>Digital Twin 시뮬레이션</div>", unsafe_allow_html=True)

future_years = np.linspace(0, max(5, years_to_replacement + 2), 50)
current_path = [max(0, current_soh - (degradation_rate_per_year * y)) for y in future_years]
improved_path = [max(0, current_soh - (improved_deg_rate * y)) for y in future_years]

fig_dt = go.Figure()

# 개선 후 경로 (녹색)
fig_dt.add_trace(go.Scatter(
    x=future_years, y=improved_path,
    mode='lines', name='온도 최적화 시',
    line=dict(color='#10b981', width=3, dash='dot')
))

# 현재 패턴 경로 (파란색)
fig_dt.add_trace(go.Scatter(
    x=future_years, y=current_path,
    mode='lines', name='현재 사용 패턴 유지',
    line=dict(color='#3b82f6', width=4)
))

# 교체 기준선 (SOH 70%)
fig_dt.add_hline(y=70, line_dash="dash", line_color="#ef4444", annotation_text="교체 권장선 (SOH 70%)", annotation_position="bottom left")

fig_dt.update_layout(
    template="plotly_white",
    height=350,
    margin=dict(l=0, r=0, t=20, b=0),
    xaxis_title="앞으로의 경과 시간 (년)",
    yaxis_title="배터리 건강도 (SOH %)",
    yaxis=dict(range=[50, 100]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_dt, use_container_width=True, config={'displayModeBar': False})

# ==========================================
# 5. MONTE CARLO (신뢰 구간)
# ==========================================
st.markdown("<div class='section-title'>수명 예측 신뢰구간 (Monte Carlo 95%)</div>", unsafe_allow_html=True)

# 몬테카를로 노이즈 생성
mc_paths = []
for _ in range(100):
    noise = np.random.normal(0, 1.5, len(future_years))
    # 누적 노이즈(Random Walk) 적용
    rw_noise = np.cumsum(noise) * 0.2
    path = np.clip(current_path + rw_noise, 0, 100)
    mc_paths.append(path)

mc_paths = np.array(mc_paths)
upper_bound = np.percentile(mc_paths, 95, axis=0)
lower_bound = np.percentile(mc_paths, 5, axis=0)

fig_mc = go.Figure()

# 95% 신뢰구간 채우기
fig_mc.add_trace(go.Scatter(
    x=np.concatenate([future_years, future_years[::-1]]),
    y=np.concatenate([upper_bound, lower_bound[::-1]]),
    fill='toself', fillcolor='rgba(148, 163, 184, 0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    name='95% 신뢰구간',
    hoverinfo="skip"
))

# 평균선
fig_mc.add_trace(go.Scatter(
    x=future_years, y=current_path,
    mode='lines', name='예상 평균치',
    line=dict(color='#64748b', width=2)
))

fig_mc.update_layout(
    template="plotly_white",
    height=300,
    margin=dict(l=0, r=0, t=20, b=0),
    xaxis_title="앞으로의 경과 시간 (년)",
    yaxis_title="SOH (%)",
    yaxis=dict(range=[50, 100]),
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_mc, use_container_width=True, config={'displayModeBar': False})
