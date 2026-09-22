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

    st.subheader("⚠️ Risk Analytics")

    st.caption(
        "AI-assisted security risk assessment from observed "
        "network activity"
    )

    try:

        # =====================================================
        # LOAD REAL DATABASE DATA
        # =====================================================

        database, data = load_data()

        total = database.get(
            "total_records",
            0
        )

        attacks = data.get(
            "total_attack_records",
            0
        )

        benign = total - attacks

        attack_types = data.get(
            "attack_types",
            {}
        )

        # =====================================================
        # ATTACK RATE
        # =====================================================

        attack_rate = (
            attacks / total * 100
            if total > 0
            else 0
        )

        # =====================================================
        # DERIVED RISK INDICATOR
        # =====================================================

        risk_score = min(
            100,
            attack_rate * 5
        )

        if risk_score >= 70:

            risk_level = "CRITICAL"

        elif risk_score >= 45:

            risk_level = "HIGH"

        elif risk_score >= 20:

            risk_level = "MEDIUM"

        else:

            risk_level = "LOW"

        # =====================================================
        # KPI CARDS
        # =====================================================

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "🚨 Attack Records",
            f"{attacks:,}"
        )

        c2.metric(
            "⚠️ Attack Rate",
            f"{attack_rate:.2f}%"
        )

        c3.metric(
            "🎯 Risk Score",
            f"{risk_score:.1f}/100"
        )

        c4.metric(
            "🛡️ Risk Level",
            risk_level
        )

        st.divider()

        # =====================================================
        # SECURITY EXPOSURE
        # =====================================================

        st.markdown(
            "### 🎯 Security Exposure"
        )

        st.progress(
            int(risk_score)
        )

        if risk_level == "CRITICAL":

            st.error(
                "CRITICAL SECURITY EXPOSURE"
            )

        elif risk_level == "HIGH":

            st.warning(
                "HIGH SECURITY EXPOSURE"
            )

        elif risk_level == "MEDIUM":

            st.warning(
                "MEDIUM SECURITY EXPOSURE"
            )

        else:

            st.success(
                "LOW SECURITY EXPOSURE"
            )

        st.caption(
            "Risk Score is a derived dashboard indicator based "
            "on the observed attack rate."
        )

        st.divider()

        # =====================================================
        # THREAT RISK DISTRIBUTION
        # =====================================================

        st.markdown(
            "### 🚨 Threat Risk Distribution"
        )

        df = pd.DataFrame(
            list(attack_types.items()),
            columns=[
                "Attack Type",
                "Records"
            ]
        )

        if not df.empty:

            df["Share"] = (
                df["Records"] /
                attacks *
                100
            )

            df["Risk Contribution"] = (
                df["Share"] * 5
            ).clip(
                upper=100
            )

            chart_df = df.sort_values(
                "Risk Contribution",
                ascending=True
            )

            fig = px.bar(
                chart_df,
                x="Risk Contribution",
                y="Attack Type",
                orientation="h",
                text="Risk Contribution"
            )

            fig.update_layout(
                height=550,
                xaxis_title="Risk Contribution",
                yaxis_title="Attack Type",
                margin=dict(
                    l=10,
                    r=10,
                    t=30,
                    b=10
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No attack-type data available."
            )

        # =====================================================
        # RISK ASSESSMENT TABLE
        # =====================================================

        st.markdown(
            "### 📋 Risk Assessment"
        )

        if not df.empty:

            table = df.copy()

            table["Share"] = (
                table["Share"]
                .round(2)
                .astype(str)
                + "%"
            )

            table["Risk Contribution"] = (
                table["Risk Contribution"]
                .round(2)
            )

            table = table.sort_values(
                "Records",
                ascending=False
            )

            st.dataframe(
                table,
                use_container_width=True,
                hide_index=True
            )

        st.divider()

        # =====================================================
        # SECURITY SUMMARY
        # =====================================================

        st.markdown(
            "### 🧠 Security Interpretation"
        )

        st.info(
            f"CyberDemandIQ analyzed {total:,} network flows, "
            f"including {attacks:,} attack records and "
            f"{benign:,} benign records. "
            f"The observed attack rate is "
            f"{attack_rate:.2f}%."
        )

    except Exception as e:

        st.error(
            "Unable to calculate risk analytics."
        )

        st.code(
            str(e),
            language="text"
        )