
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="Battery Guardian", page_icon="🔋", layout="wide")

st.markdown("""
<style>
.stApp {background-color:#f8fafc;}
h1,h2,h3 {color:#111827;}
[data-testid="stMetric"]{
    background:white;
    border-radius:12px;
    padding:12px;
    border:1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

def calculate_metrics(cycle,temp,months,ir):
    soh=max(40,100-cycle*0.015-months*0.08)
    soc=np.clip(85-np.random.normal(0,3),0,100)
    rul=max(0,int(4000-cycle))
    risk=min(100,max(0,100-soh+(temp-25)*1.5+ir*500))
    return soh,soc,rul,risk

def generate_report(soh,temp,rul,risk):
    level = "낮음" if risk < 35 else "중간" if risk < 65 else "높음"
    return f"""
### 종합 평가
현재 배터리는 **{'양호' if soh > 75 else '주의'}** 상태입니다.

### 핵심 결과
- SOH : {soh:.1f}%
- 예상 잔존 수명 : {rul} Cycles
- 위험도 : {level}

### 발견된 문제
- {'온도 관리 양호' if temp < 35 else '고온 노출 위험 존재'}
- {'급격한 열화 없음' if soh > 70 else '열화 진행 중'}

### 권장 조치
- 20~30°C 범위 유지
- 잦은 급속충전 최소화
- 월 1회 상태 점검
"""

def chatbot_response(question, soh, temp, rul, risk):
    q = question.lower()
    if "교체" in q:
        return f"현재 추정 잔존 수명은 {rul} cycles입니다. SOH가 70% 이하로 내려가면 교체 검토를 권장합니다."
    if "위험" in q:
        return f"현재 위험도는 {risk:.1f}/100 입니다."
    if "온도" in q:
        return f"현재 온도는 {temp}°C 입니다. 35°C 이상이면 열화가 빨라질 수 있습니다."
    return f"현재 SOH는 {soh:.1f}%이며 전반적으로 {'양호' if soh > 75 else '주의'} 상태입니다."

st.title("🔋 Battery Guardian")
st.caption("배터리 고장을 미리 예측하고 최적의 교체 시점을 알려주는 AI 플랫폼")

with st.container(border=True):
    st.subheader("배터리 진단 입력")
    c1,c2,c3,c4 = st.columns(4)

    with c1:
        battery = st.selectbox("배터리 종류",["Li-ion","LFP","NMC"])
    with c2:
        cycle = st.number_input("충방전 횟수",0,5000,800)
    with c3:
        temp = st.number_input("평균 온도(°C)",0.0,100.0,28.0)
    with c4:
        months = st.number_input("사용 개월 수",0,240,24)

    ir = st.slider("내부저항",0.01,0.08,0.025)

soh,soc,rul,risk = calculate_metrics(cycle,temp,months,ir)

m1,m2,m3,m4 = st.columns(4)
m1.metric("SOH",f"{soh:.1f}%")
m2.metric("SOC",f"{soc:.1f}%")
m3.metric("RUL",f"{rul}")
m4.metric("위험도",f"{risk:.0f}/100")

tab1,tab2,tab3 = st.tabs(["대시보드","예측 분석","AI 진단"])

with tab1:
    st.subheader("배터리 건강도 추세")
    x=np.arange(120)
    y=np.linspace(100,soh,120)+np.random.normal(0,1,120)
    st.plotly_chart(px.line(x=x,y=y,labels={"x":"시간","y":"SOH"}),
                    use_container_width=True)

    st.subheader("셀 온도 Heatmap")
    heat=np.random.uniform(20,40,(8,12))
    st.plotly_chart(px.imshow(heat,color_continuous_scale="Blues"),
                    use_container_width=True)

with tab2:
    st.subheader("수명 예측")
    future=np.arange(cycle,cycle+1500,20)

    fig=go.Figure()
    for _ in range(30):
        path=soh-(future-cycle)*(0.012+np.random.normal(0,0.003))
        fig.add_trace(go.Scatter(x=future,y=path,
                                 line=dict(width=1),
                                 opacity=0.15,
                                 showlegend=False))
    fig.update_layout(height=500)
    st.plotly_chart(fig,use_container_width=True)

    st.subheader("이상 탐지")
    data=pd.DataFrame({
        "온도":np.random.normal(temp,2,200),
        "저항":np.random.normal(ir,0.003,200)
    })

    model=IsolationForest(contamination=0.05, random_state=42)
    pred=model.fit_predict(data)
    data["상태"]=np.where(pred==-1,"이상","정상")

    fig2=px.scatter(data,x="온도",y="저항",color="상태")
    st.plotly_chart(fig2,use_container_width=True)

with tab3:
    st.subheader("AI 진단 리포트")
    st.markdown(generate_report(soh,temp,rul,risk))

    st.divider()
    st.subheader("Battery Copilot")

    if "chat" not in st.session_state:
        st.session_state.chat=[]

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt=st.chat_input("예: 내 배터리 위험한가요?")

    if prompt:
        st.session_state.chat.append({"role":"user","content":prompt})
        answer=chatbot_response(prompt,soh,temp,rul,risk)
        st.session_state.chat.append({"role":"assistant","content":answer})
        st.rerun()
