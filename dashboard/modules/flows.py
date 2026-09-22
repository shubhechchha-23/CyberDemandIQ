import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:8000"


@st.cache_data(ttl=30)
def load_flows(limit, attack_only):

    response = requests.get(
        f"{API}/api/network-flows",
        params={
            "limit": limit,
            "attack_only": attack_only
        },
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def show():

    st.subheader("🔎 Network Investigation")

    st.caption(
        "Investigate real network-flow records from PostgreSQL"
    )

    c1, c2 = st.columns(2)

    with c1:

        limit = st.selectbox(
            "Records to inspect",
            [25, 50, 100, 200],
            index=2
        )

    with c2:

        attack_only = st.toggle(
            "🚨 Attack traffic only"
        )

    st.divider()

    try:

        data = load_flows(
            limit,
            attack_only
        )

        records = data.get(
            "records",
            []
        )

        if not records:

            st.warning(
                "No network-flow records found."
            )

            return

        df = pd.DataFrame(records)

        total = len(df)

        attacks = (
            df["label"].ne("BENIGN").sum()
            if "label" in df.columns
            else 0
        )

        benign = total - attacks

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Flows Loaded",
            f"{total:,}"
        )

        c2.metric(
            "Attack Flows",
            f"{attacks:,}"
        )

        c3.metric(
            "Benign Flows",
            f"{benign:,}"
        )

        st.divider()

        st.markdown(
            "### 🌐 Network Flow Records"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        if "label" in df.columns:

            st.markdown(
                "### 🚨 Observed Traffic Classes"
            )

            distribution = (
                df["label"]
                .value_counts()
                .rename_axis("Label")
                .reset_index(
                    name="Records"
                )
            )

            st.dataframe(
                distribution,
                use_container_width=True,
                hide_index=True
            )

        st.download_button(
            "⬇️ Download Investigation Data",
            df.to_csv(index=False),
            "cyberdemandiq_network_investigation.csv",
            "text/csv",
            use_container_width=True
        )

    except Exception as e:

        st.error(
            "Unable to load network-flow data."
        )

        st.code(
            str(e),
            language="text"
        )