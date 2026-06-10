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
    page_title="Battery AI Cloud Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# ADVANCED CSS
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Orbitron', sans-serif;
}

.stApp{
background:
linear-gradient(
180deg,
#030712 0%,
#0f172a 100%
);
}

.main-title{
font-size:3rem;
font-weight:700;
text-align:center;
color:white;
margin-bottom:20px;
text-shadow:
0 0 10px cyan,
0 0 20px cyan;
}

.metric-card{
background:rgba(255,255,255,.04);
padding:20px;
border-radius:20px;
border:1px solid rgba(255,255,255,.08);
backdrop-filter:blur(12px);
}

.glass{
background:rgba(255,255,255,.03);
border-radius:24px;
padding:20px;
border:1px solid rgba(255,255,255,.08);
backdrop-filter:blur(14px);
}

.alert-good{
color:#00ff99;
font-weight:bold;
}

.alert-warning{
color:orange;
font-weight:bold;
}

.alert-danger{
color:red;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# TITLE
# ==========================================

st.markdown(
    "<div class='main-title'>⚡ BATTERY AI CLOUD PLATFORM</div>",
    unsafe_allow_html=True
)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("CONTROL CENTER")

    cycle = st.slider(
        "Cycle",
        0,
        5000,
        800
    )

    temp = st.slider(
        "Temperature",
        10,
        70,
        28
    )

    ir = st.slider(
        "Internal Resistance",
        0.01,
        0.08,
        0.025
    )

    qc = st.slider(
        "Charge Capacity",
        0.5,
        2.0,
        1.25
    )

    qd = st.slider(
        "Discharge Capacity",
        0.5,
        2.0,
        1.18
    )

# ==========================================
# HEALTH ENGINE
# ==========================================

soh = max(
    40,
    100 - (cycle * 0.015)
)

soc = np.clip(
    80 + np.random.normal(0,3),
    0,
    100
)

rul = int(
    max(
        0,
        4000 - cycle
    )
)

health_score = (
    soh * 0.5
    + (100-ir*1000)*0.3
    + (100-abs(temp-25))*0.2
)

# ==========================================
# KPI
# ==========================================

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "SOH",
        f"{soh:.1f}%",
        "-0.2%"
    )

with c2:
    st.metric(
        "SOC",
        f"{soc:.1f}%",
        "+1.3%"
    )

with c3:
    st.metric(
        "RUL",
        f"{rul} Cycles"
    )

with c4:

    grade = "A"

    if health_score < 80:
        grade="B"

    if health_score < 60:
        grade="C"

    st.metric(
        "Health Grade",
        grade
    )

# ==========================================
# TABS
# ==========================================

tab1,tab2,tab3,tab4,tab5 = st.tabs(
[
"Live Twin",
"Battery Pack",
"Forecast",
"Anomaly",
"Copilot"
]
)

# ==========================================
# TAB 1
# ==========================================

with tab1:

    st.subheader(
        "Real-Time Digital Twin"
    )

    start = st.button(
        "Start Stream"
    )

    chart_area = st.empty()

    if start:

        cycles=[]
        preds=[]
        temps=[]

        for i in range(50):

            current_cycle = cycle+i

            current_temp = (
                temp +
                np.random.normal(
                    0,
                    1
                )
            )

            prediction = (
                soh
                - i*0.08
                + np.random.normal(
                    0,
                    0.4
                )
            )

            cycles.append(
                current_cycle
            )

            preds.append(
                prediction
            )

            temps.append(
                current_temp
            )

            fig = make_subplots(
                specs=[
                    [
                        {
                            "secondary_y":True
                        }
                    ]
                ]
            )

            fig.add_trace(
                go.Scatter(
                    x=cycles,
                    y=preds,
                    mode="lines",
                    name="SOH"
                ),
                secondary_y=False
            )

            fig.add_trace(
                go.Scatter(
                    x=cycles,
                    y=temps,
                    mode="lines",
                    name="Temp"
                ),
                secondary_y=True
            )

            fig.update_layout(
                template="plotly_dark",
                height=500
            )

            chart_area.plotly_chart(
                fig,
                use_container_width=True
            )

            time.sleep(0.1)

# ==========================================
# TAB 2
# ==========================================

with tab2:

    st.subheader(
        "Battery Pack Heatmap"
    )

    rows = 8
    cols = 12

    heat = np.random.uniform(
        20,
        40,
        (
            rows,
            cols
        )
    )

    heat[
        random.randint(0,7)
    ][
        random.randint(0,11)
    ] += 20

    fig_heat = px.imshow(
        heat,
        color_continuous_scale="Turbo",
        text_auto=True
    )

    fig_heat.update_layout(
        template="plotly_dark",
        height=600
    )

    st.plotly_chart(
        fig_heat,
        use_container_width=True
    )

    st.info(
        "Each block represents an individual cell."
    )
# ==========================================
# TAB 3
# FORECAST ENGINE
# ==========================================

with tab3:

    st.subheader(
        "Predictive Battery Forecast"
    )

    colA,colB = st.columns([1,4])

    with colA:

        simulation_count = st.slider(
            "Simulation Paths",
            10,
            200,
            100
        )

        forecast_cycles = st.slider(
            "Future Cycles",
            100,
            3000,
            1000
        )

        degradation_noise = st.slider(
            "Noise Factor",
            0.01,
            0.30,
            0.08
        )

        run_forecast = st.button(
            "Run Monte Carlo"
        )

    with colB:

        if run_forecast:

            future_x = np.linspace(
                cycle,
                cycle + forecast_cycles,
                120
            )

            fig_mc = go.Figure()

            all_paths = []

            for p in range(simulation_count):

                path=[]

                base_degradation = np.random.normal(
                    0.015,
                    degradation_noise
                )

                random_walk = 0

                for fc in future_x:

                    random_walk += np.random.normal(
                        0,
                        degradation_noise
                    )

                    pred = (
                        soh
                        - (fc-cycle)*base_degradation
                        + random_walk
                    )

                    path.append(pred)

                all_paths.append(path)

                fig_mc.add_trace(
                    go.Scatter(
                        x=future_x,
                        y=path,
                        mode="lines",
                        line=dict(
                            width=1,
                            color="rgba(0,255,255,0.08)"
                        ),
                        showlegend=False
                    )
                )

            all_paths = np.array(all_paths)

            mean_path = np.mean(
                all_paths,
                axis=0
            )

            upper = np.percentile(
                all_paths,
                95,
                axis=0
            )

            lower = np.percentile(
                all_paths,
                5,
                axis=0
            )

            fig_mc.add_trace(
                go.Scatter(
                    x=future_x,
                    y=mean_path,
                    mode="lines",
                    line=dict(
                        color="magenta",
                        width=5
                    ),
                    name="Expected Life Path"
                )
            )

            fig_mc.add_trace(
                go.Scatter(
                    x=np.concatenate(
                        [future_x,future_x[::-1]]
                    ),
                    y=np.concatenate(
                        [upper,lower[::-1]]
                    ),
                    fill="toself",
                    fillcolor="rgba(255,0,255,0.15)",
                    line=dict(color="rgba(255,0,255,0)"),
                    name="95% Confidence"
                )
            )

            fig_mc.update_layout(
                template="plotly_dark",
                height=650,
                title="Monte Carlo Life Prediction"
            )

            st.plotly_chart(
                fig_mc,
                use_container_width=True
            )

# ==========================================
# RUL ANALYTICS
# ==========================================

            st.markdown("---")

            end_soh = mean_path[-1]

            risk = "LOW"

            if end_soh < 80:
                risk = "MEDIUM"

            if end_soh < 60:
                risk = "HIGH"

            r1,r2,r3 = st.columns(3)

            with r1:

                st.metric(
                    "Expected End SOH",
                    f"{end_soh:.1f}%"
                )

            with r2:

                st.metric(
                    "Forecast RUL",
                    f"{rul}"
                )

            with r3:

                st.metric(
                    "Risk Level",
                    risk
                )

# ==========================================
# DIGITAL TWIN 3D
# ==========================================

    st.markdown("---")

    st.subheader(
        "3D Battery Digital Twin"
    )

    sample_size = 250

    twin_df = pd.DataFrame({

        "cycle":
        np.random.randint(
            cycle,
            cycle+1000,
            sample_size
        ),

        "temperature":
        np.random.normal(
            temp,
            4,
            sample_size
        ),

        "soh":
        np.random.normal(
            soh,
            5,
            sample_size
        )

    })

    fig3d = px.scatter_3d(

        twin_df,

        x="cycle",

        y="temperature",

        z="soh",

        color="soh",

        color_continuous_scale="Turbo",

        opacity=0.8
    )

    fig3d.update_layout(

        template="plotly_dark",

        height=700
    )

    st.plotly_chart(
        fig3d,
        use_container_width=True
    )

# ==========================================
# FUTURE FAILURE MAP
# ==========================================

    st.subheader(
        "Failure Probability Map"
    )

    failure_cycle = np.arange(
        cycle,
        cycle+2000,
        25
    )

    failure_probability = []

    for fc in failure_cycle:

        prob = min(
            95,
            (
                (fc-cycle)
                /
                2000
            )*100
        )

        prob += np.random.normal(
            0,
            3
        )

        failure_probability.append(
            max(
                0,
                prob
            )
        )

    fig_fail = go.Figure()

    fig_fail.add_trace(

        go.Scatter(

            x=failure_cycle,

            y=failure_probability,

            fill="tozeroy",

            line=dict(
                width=4,
                color="red"
            ),

            name="Failure Risk"
        )
    )

    fig_fail.update_layout(

        template="plotly_dark",

        height=500,

        yaxis_title="Probability %",

        xaxis_title="Cycle"
    )

    st.plotly_chart(
        fig_fail,
        use_container_width=True
    )

# ==========================================
# FORECAST SUMMARY
# ==========================================

    st.markdown("---")

    if health_score > 85:

        st.success(
            "Battery condition is stable. Long remaining useful life expected."
        )

    elif health_score > 65:

        st.warning(
            "Battery degradation is increasing. Monitoring recommended."
        )

    else:

        st.error(
            "Battery approaching critical condition. Maintenance advised."
        )
# ==========================================
# TAB 4
# ANOMALY DETECTION CENTER
# ==========================================

with tab4:

    st.subheader(
        "AI Anomaly Detection Center"
    )

    st.write(
        "Isolation Forest 기반 이상징후 탐지"
    )

    # ----------------------------------
    # SYNTHETIC DATA
    # ----------------------------------

    normal_data = pd.DataFrame({

        "temperature":
        np.random.normal(
            temp,
            2,
            300
        ),

        "ir":
        np.random.normal(
            ir,
            0.003,
            300
        ),

        "cycle":
        np.random.normal(
            cycle,
            50,
            300
        )

    })

    anomaly_data = pd.DataFrame({

        "temperature":
        np.random.uniform(
            50,
            80,
            10
        ),

        "ir":
        np.random.uniform(
            0.05,
            0.09,
            10
        ),

        "cycle":
        np.random.uniform(
            cycle,
            cycle+500,
            10
        )

    })

    data = pd.concat(
        [
            normal_data,
            anomaly_data
        ],
        ignore_index=True
    )

    # ----------------------------------
    # ISOLATION FOREST
    # ----------------------------------

    detector = IsolationForest(
        contamination=0.03,
        random_state=42
    )

    detector.fit(data)

    data["anomaly"] = detector.predict(
        data
    )

    data["status"] = np.where(
        data["anomaly"]==-1,
        "Anomaly",
        "Normal"
    )

    # ----------------------------------
    # ANOMALY CHART
    # ----------------------------------

    fig_anomaly = px.scatter(

        data,

        x="temperature",

        y="ir",

        color="status",

        color_discrete_map={

            "Normal":"cyan",

            "Anomaly":"red"
        },

        size_max=12
    )

    fig_anomaly.update_layout(

        template="plotly_dark",

        height=600
    )

    st.plotly_chart(
        fig_anomaly,
        use_container_width=True
    )

# ==========================================
# ANOMALY TABLE
# ==========================================

    anomaly_rows = data[
        data["status"]=="Anomaly"
    ]

    st.markdown(
        "### Critical Events"
    )

    st.dataframe(
        anomaly_rows.head(20),
        use_container_width=True
    )

# ==========================================
# ALERT CENTER
# ==========================================

    st.markdown("---")

    st.subheader(
        "Alert Center"
    )

    alerts = []

    if temp > 45:

        alerts.append(
            "High Temperature Detected"
        )

    if ir > 0.04:

        alerts.append(
            "Internal Resistance Rising"
        )

    if soh < 70:

        alerts.append(
            "SOH Below Threshold"
        )

    if len(alerts)==0:

        st.success(
            "No active alerts"
        )

    else:

        for alert in alerts:

            st.error(alert)

# ==========================================
# CELL HEALTH MONITOR
# ==========================================

    st.markdown("---")

    st.subheader(
        "Cell Health Ranking"
    )

    cells = []

    for i in range(96):

        cells.append({

            "Cell":

            f"CELL-{i+1}",

            "SOH":

            np.random.uniform(
                65,
                100
            ),

            "Temp":

            np.random.uniform(
                20,
                45
            ),

            "IR":

            np.random.uniform(
                0.01,
                0.06
            )
        })

    fleet = pd.DataFrame(
        cells
    )

    fleet["Score"] = (

        fleet["SOH"]*0.6

        +(100-fleet["IR"]*1000)*0.3

        +(100-fleet["Temp"])*0.1

    )

    fleet = fleet.sort_values(
        "Score",
        ascending=False
    )

    st.dataframe(
        fleet,
        use_container_width=True
    )

# ==========================================
# HEALTH DISTRIBUTION
# ==========================================

    fig_hist = px.histogram(

        fleet,

        x="SOH",

        nbins=25,

        color_discrete_sequence=[
            "cyan"
        ]
    )

    fig_hist.update_layout(

        template="plotly_dark",

        height=500
    )

    st.plotly_chart(
        fig_hist,
        use_container_width=True
    )

# ==========================================
# XAI SECTION
# ==========================================

    st.markdown("---")

    st.subheader(
        "Explainable AI Dashboard"
    )

    feature_importance = pd.DataFrame({

        "Feature":[

            "Cycle",

            "Temperature",

            "IR",

            "QC",

            "QD"

        ],

        "Importance":[

            0.42,

            0.23,

            0.18,

            0.09,

            0.08

        ]
    })

    fig_imp = px.bar(

        feature_importance,

        x="Importance",

        y="Feature",

        orientation="h",

        color="Importance",

        color_continuous_scale="Turbo"
    )

    fig_imp.update_layout(

        template="plotly_dark",

        height=500
    )

    st.plotly_chart(
        fig_imp,
        use_container_width=True
    )

# ==========================================
# SHAP STYLE WATERFALL
# ==========================================

    st.subheader(
        "Contribution Analysis"
    )

    contrib = pd.DataFrame({

        "Feature":[

            "Cycle",

            "Temperature",

            "IR",

            "QC",

            "QD"

        ],

        "Contribution":[

            -12,

            -4,

            -8,

            +5,

            +3

        ]
    })

    fig_water = go.Figure()

    fig_water.add_trace(

        go.Bar(

            x=contrib["Feature"],

            y=contrib["Contribution"],

            marker_color=[

                "red" if x < 0
                else "green"

                for x in contrib[
                    "Contribution"
                ]
            ]
        )
    )

    fig_water.update_layout(

        template="plotly_dark",

        height=500
    )

    st.plotly_chart(
        fig_water,
        use_container_width=True
    )

# ==========================================
# RISK GAUGE
# ==========================================

    st.subheader(
        "Battery Risk Gauge"
    )

    risk_value = np.clip(

        100-health_score,

        0,

        100
    )

    gauge = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=risk_value,

            title={
                "text":"Risk Index"
            },

            gauge={

                "axis":{
                    "range":[0,100]
                },

                "bar":{
                    "color":"red"
                },

                "steps":[

                    {
                        "range":[0,40],
                        "color":"green"
                    },

                    {
                        "range":[40,70],
                        "color":"orange"
                    },

                    {
                        "range":[70,100],
                        "color":"red"
                    }
                ]
            }
        )
    )

    gauge.update_layout(

        template="plotly_dark",

        height=450
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )