import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API = "http://127.0.0.1:8000"


@st.cache_data(ttl=30)
def load_threats():
    return requests.get(
        f"{API}/api/attack-statistics",
        timeout=30
    ).json()


def show():

    st.subheader("🚨 Threat Intelligence")
    st.caption(
        "Real attack activity detected across the CyberDemandIQ network dataset"
    )

    data = load_threats()

    attacks = data.get("total_attack_records", 0)
    benign = data.get("total_benign_records", 2148386)
    types = data.get("attack_types", {})

    total = attacks + benign

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🚨 Total Attacks",
        f"{attacks:,}"
    )

    c2.metric(
        "🟢 Benign Traffic",
        f"{benign:,}"
    )

    c3.metric(
        "⚠️ Attack Rate",
        f"{attacks / total * 100:.2f}%"
    )

    st.divider()

    df = pd.DataFrame(
        list(types.items()),
        columns=["Attack Type", "Records"]
    )

    df = df.sort_values(
        "Records",
        ascending=False
    )

    st.markdown("### 🎯 Attack Distribution")

    fig = px.bar(
        df,
        x="Attack Type",
        y="Records",
        text="Records"
    )

    fig.update_layout(
        height=500,
        xaxis_tickangle=-35,
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=100
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("### 📋 Threat Inventory")

    df["Share"] = (
        df["Records"] / attacks * 100
    ).round(2)

    df["Share"] = (
        df["Share"].astype(str) + "%"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )