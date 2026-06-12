import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# ==========================================
# PAGE CONFIG & CSS
# ==========================================
st.set_page_config(page_title="배터리 미래 시뮬레이터", page_icon="🔮", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .hospital-card {
        background-color: #1e293b; padding: 20px; border-radius: 10px; 
        border-left: 5px solid #3b82f6; margin-bottom: 20px;
    }
    .sns-card {
        background-color: #1e293b; padding: 20px; border-radius: 15px; 
        border: 1px solid #475569; font-family: 'Courier New', Courier, monospace;
        color: #fbbf24; text-align: center; margin-top: 20px;
    }
    .highlight { color: #38bdf8; font-weight: bold; }
    h1, h2, h3 { color: #f1f5f9; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA & LOGIC MOCKUP
# ==========================================
def calculate_future(base_soh, stop_fast_charge, lower_temp, optimize_charge):
    added_months = 0
    saved_money = 0
    carbon_reduction = 0
    
    if stop_fast_charge:
        added_months += 11
        saved_money += 55000
        carbon_reduction += 12
    if lower_temp:
        added_months += 7
        saved_money += 35000
        carbon_reduction += 8
    if optimize_charge:
        added_months += 5
        saved_money += 25000
        carbon_reduction += 5
        
    return added_months, saved_money, carbon_reduction

# ==========================================
# HEADER
# ==========================================
st.title("🔮 배터리 미래 시뮬레이터")
st.caption("당신의 습관이 배터리의 수명을 결정합니다. 미래를 예측하고 운명을 바꿔보세요.")
st.markdown("---")

# ==========================================
# SECTION 1: AI 배터리 의사 (Hospital Concept)
# ==========================================
st.header("🏥 AI 배터리 진단 차트")

col1, col2 = st.columns([1, 2])

with col1:
    device_name = st.text_input("환자명 (기기명)", "Galaxy S25 Ultra")
    usage_months = st.slider("사용 기간 (개월)", 1, 48, 14)
    current_soh = st.number_input("현재 SOH (%)", 0.0, 100.0, 84.5)
    
with col2:
    diagnosis_status = "경고 (Warning)" if current_soh < 85 else "정상 (Normal)"
    color = "red" if diagnosis_status == "경고 (Warning)" else "green"
    
    st.markdown(f"""
    <div class="hospital-card">
        <h3>📋 진단 결과</h3>
        <p><b>환자명:</b> {device_name}</p>
        <p><b>진단명:</b> <span style="color:{color}; font-weight:bold;">열화 초기 증상 및 고온 스트레스 누적</span></p>
        <p><b>현재 위험도:</b> {'🔴 높음' if current_soh < 80 else '🟡 경증' if current_soh < 90 else '🟢 낮음'}</p>
        <p><b>AI 주치의 소견:</b> 잦은 고속 충전으로 인해 동급 기기 대비 노화가 12% 빠르게 진행되고 있습니다. 즉각적인 습관 교정이 필요합니다.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# SECTION 2: 연도별 생존 확률 타임머신
# ==========================================
st.header("⏳ 수명 타임머신: 이대로 계속 쓴다면?")
st.write("현재 사용 습관을 유지할 경우 예상되는 미래의 배터리 상태입니다.")

years = ["2026 (현재)", "2027 (+1년)", "2028 (+2년)", "2029 (+3년)"]
soh_drop = [current_soh, current_soh - 9, current_soh - 21, current_soh - 35]
survival_prob = [94, 73, 42, 11]

fig = go.Figure()
fig.add_trace(go.Scatter(x=years, y=survival_prob, mode='lines+markers+text', 
                         name='생존 확률 (%)', text=[f"{p}%" for p in survival_prob], 
                         textposition="top center", marker=dict(size=12, color='#ef4444'), line=dict(width=4)))

fig.add_trace(go.Bar(x=years, y=soh_drop, name='예상 SOH (%)', marker_color='#3b82f6', opacity=0.6))

fig.update_layout(template="plotly_dark", height=400, yaxis_title="퍼센트 (%)", 
                  title="연도별 SOH 및 기기 생존 확률 추이", margin=dict(b=0))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==========================================
# SECTION 3: 배터리 미래 시뮬레이터 (Core Idea)
# ==========================================
st.header("🎮 운명 바꾸기 시뮬레이터")
st.write("아래의 습관을 바꾸면 미래가 어떻게 변하는지 즉시 확인하세요.")

c1, c2 = st.columns([1, 1.5])

with c1:
    st.markdown("#### 🛠️ 처방전 (행동 선택)")
    act1 = st.toggle("⚡ 매일 하던 고속충전 중단하기", value=False)
    act2 = st.toggle("🌡️ 게임 시간 줄여서 온도 5도 낮추기", value=False)
    act3 = st.toggle("🔋 배터리 20% 밑으로 떨어지기 전에 충전하기", value=False)

with c2:
    st.markdown("#### 🎁 예측되는 보상 결과")
    added_months, saved_money, carbon = calculate_future(current_soh, act1, act2, act3)
    
    if added_months == 0:
        st.info("행동을 선택하여 배터리의 수명을 연장해 보세요!")
    else:
        st.success("✅ 새로운 습관이 적용되었습니다!")
        m1, m2, m3 = st.columns(3)
        m1.metric("수명 연장", f"+{added_months}개월")
        m2.metric("절약 금액 (교체비용)", f"{saved_money:,}원")
        m3.metric("탄소 배출 절감", f"{carbon}kg 🌲")

st.markdown("---")

# ==========================================
# SECTION 4: 배터리 SNS (Fun Factor)
# ==========================================
st.header("💌 배터리의 속마음")

messages = [
    "안녕...? 나 네 배터리야. 솔직히 말할게. 어제 밤새 100% 꽂아두고 잔 거, 나 진짜 숨 막혀 죽는 줄 알았어... 🥵",
    "주인님, 롤 모바일 하면서 충전기 꽂아두는 건 진짜 선 넘었죠. 저 어제 체온 42도 찍었어요. 살려주세요. 😭",
    "이대로 가면 저 내년 겨울엔 밖에서 폰 꺼질지도 몰라요. 저체온증 + 과로사 오기 직전입니다. 🥶"
]
selected_msg = messages[int(current_soh) % 3] # 단순 랜덤화 모방

st.markdown(f"""
<div class="sns-card">
    "{selected_msg}"
</div>
""", unsafe_allow_html=True)
