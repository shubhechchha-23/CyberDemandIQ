import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API = "http://127.0.0.1:8000"


@st.cache_data(ttl=30)
def load_data():

    database = requests.get(
        f"{API}/api/database-stats",
        timeout=30
    ).json()

    attacks = requests.get(
        f"{API}/api/attack-statistics",
        timeout=30
    ).json()

    return database, attacks


def show():

    st.subheader("📊 Security Operations Overview")

    st.caption(
        "Real-time cybersecurity intelligence from CyberDemandIQ"
    )

    try:

        database, attacks = load_data()

        total = database.get(
            "total_records",
            0
        )

        attack_count = attacks.get(
            "total_attack_records",
            0
        )

        benign = total - attack_count

        attack_rate = (
            attack_count / total * 100
            if total
            else 0
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "🌐 Network Flows",
            f"{total:,}"
        )

        c2.metric(
            "🚨 Attack Records",
            f"{attack_count:,}"
        )

        c3.metric(
            "🟢 Benign Traffic",
            f"{benign:,}"
        )

        c4.metric(
            "⚠️ Attack Rate",
            f"{attack_rate:.2f}%"
        )

        st.divider()

        attack_types = attacks.get(
            "attack_types",
            {}
        )

        if attack_types:

            df = pd.DataFrame({
                "Attack Type": attack_types.keys(),
                "Records": attack_types.values()
            })

            df = df.sort_values(
                "Records",
                ascending=True
            )

            st.markdown(
                "### 🚨 Threat Landscape"
            )

            fig = px.bar(
                df,
                x="Records",
                y="Attack Type",
                orientation="h",
                text="Records"
            )

            fig.update_layout(
                height=500,
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.divider()

        st.markdown(
            "### 🤖 AI & Infrastructure Status"
        )

        a, b, c = st.columns(3)

        a.success(
            "🟢 XGBoost Detection Engine\n\n"
            "Accuracy: 99.90%\n\n"
            "ROC-AUC: 1.00"
        )

        b.success(
            "🟢 PostgreSQL Database\n\n"
            f"{total:,} network records\n\n"
            "cybersecurity.network_flows"
        )

        c.success(
            "🟢 Temporal Intelligence\n\n"
            "R²: 0.9253\n\n"
            "Sequence model active"
        )

    except Exception as e:

        st.error(
            "Unable to load security overview."
        )

        st.code(
            str(e),
            language="text"
        )