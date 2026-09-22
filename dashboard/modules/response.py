import streamlit as st
import requests

API = "http://127.0.0.1:8000"


@st.cache_data(ttl=30)
def load_attack_data():

    response = requests.get(
        f"{API}/api/attack-statistics",
        timeout=30
    )

    return response.json()


def get_response(attack_type):

    responses = {

        "DDoS": (
            "Activate traffic filtering and rate limiting. "
            "Inspect abnormal inbound traffic and isolate "
            "affected services."
        ),

        "DoS Hulk": (
            "Apply request-rate controls and investigate "
            "high-volume HTTP traffic."
        ),

        "PortScan": (
            "Review source IP activity and restrict "
            "unnecessary exposed ports."
        ),

        "FTP-Patator": (
            "Investigate repeated authentication attempts "
            "and enforce account protection."
        ),

        "SSH-Patator": (
            "Review SSH authentication logs and apply "
            "rate limiting or temporary source blocking."
        ),

        "Bot": (
            "Investigate automated traffic patterns and "
            "inspect suspicious source behavior."
        ),

        "Heartbleed": (
            "Check vulnerable TLS services and update "
            "affected systems immediately."
        )
    }

    return responses.get(
        attack_type,
        "Investigate the affected traffic, review logs, "
        "identify the source and apply appropriate "
        "network controls."
    )


def show():

    st.subheader("🧠 Response Intelligence")

    st.caption(
        "Security-response recommendations generated from "
        "observed attack activity"
    )

    try:

        data = load_attack_data()

        attack_types = data.get(
            "attack_types",
            {}
        )

        total_attacks = data.get(
            "total_attack_records",
            0
        )

        # =====================================================
        # OVERVIEW
        # =====================================================

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "🚨 Active Attack Records",
            f"{total_attacks:,}"
        )

        c2.metric(
            "🎯 Attack Categories",
            len(attack_types)
        )

        c3.metric(
            "🛡️ Response Mode",
            "ACTIVE"
        )

        st.divider()

        # =====================================================
        # THREAT SELECTION
        # =====================================================

        st.markdown(
            "### 🎯 Select Threat Category"
        )

        sorted_attacks = sorted(
            attack_types.items(),
            key=lambda x: x[1],
            reverse=True
        )

        attack_names = [
            x[0] for x in sorted_attacks
        ]

        selected = st.selectbox(
            "Attack Type",
            attack_names
        )

        selected_count = attack_types.get(
            selected,
            0
        )

        st.divider()

        # =====================================================
        # THREAT DETAILS
        # =====================================================

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Detected Records",
                f"{selected_count:,}"
            )

        with c2:

            share = (
                selected_count /
                total_attacks *
                100
                if total_attacks
                else 0
            )

            st.metric(
                "Attack Share",
                f"{share:.2f}%"
            )

        st.divider()

        # =====================================================
        # RESPONSE RECOMMENDATION
        # =====================================================

        st.markdown(
            "### 🚨 Recommended Response"
        )

        st.warning(
            get_response(selected)
        )

        st.divider()

        # =====================================================
        # RESPONSE CHECKLIST
        # =====================================================

        st.markdown(
            "### 🛡️ Response Checklist"
        )

        actions = [
            "🔍 Investigate source IP and traffic origin",
            "📊 Review affected network-flow records",
            "🧾 Inspect relevant security logs",
            "🚧 Apply appropriate traffic controls",
            "🔐 Check exposed services and credentials",
            "📈 Monitor subsequent traffic activity"
        ]

        for action in actions:

            st.checkbox(
                action,
                key=f"{selected}_{action}"
            )

        st.divider()

        # =====================================================
        # ATTACK DISTRIBUTION
        # =====================================================

        st.markdown(
            "### 📋 Attack Activity"
        )

        rows = []

        for name, count in sorted_attacks:

            rows.append({
                "Attack Type": name,
                "Records": count,
                "Share": round(
                    count /
                    total_attacks *
                    100,
                    2
                )
            })

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:

        st.error(
            "Unable to load response intelligence."
        )

        st.code(
            str(e),
            language="text"
        )