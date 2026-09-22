import streamlit as st
import requests
import pandas as pd


API = "http://127.0.0.1:8000"


@st.cache_data(ttl=60)
def load_database():

    response = requests.get(
        f"{API}/api/database-stats",
        timeout=5
    )

    response.raise_for_status()

    return response.json()


def show():

    st.subheader(
        "🗄️ Database Explorer"
    )

    st.caption(
        "CyberDemandIQ PostgreSQL Security Dataset"
    )

    try:

        data = load_database()

    except Exception as e:

        st.error(
            "Unable to connect to CyberDemandIQ API."
        )

        st.code(
            str(e),
            language="text"
        )

        return

    if "total_records" not in data:

        st.error(
            "Database statistics unavailable."
        )

        return

    labels = data.get(
        "label_distribution",
        {}
    )

    total = data.get(
        "total_records",
        0
    )

    st.divider()

    # ========================================================
    # DATABASE OVERVIEW
    # ========================================================

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Database",
        data.get(
            "database",
            "PostgreSQL"
        )
    )

    c2.metric(
        "Schema",
        data.get(
            "schema",
            "cybersecurity"
        )
    )

    c3.metric(
        "Total Records",
        f"{total:,}"
    )

    st.divider()

    # ========================================================
    # DATASET DISTRIBUTION
    # ========================================================

    st.markdown(
        "### 📊 Dataset Distribution"
    )

    df = pd.DataFrame(
        list(labels.items()),
        columns=[
            "Label",
            "Records"
        ]
    )

    df = df.sort_values(
        "Records",
        ascending=False
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # DISTRIBUTION CHART
    # ========================================================

    st.markdown(
        "### 📈 Security Dataset Composition"
    )

    chart_df = df.set_index(
        "Label"
    )

    st.bar_chart(
        chart_df[
            "Records"
        ]
    )

    st.divider()

    # ========================================================
    # DATABASE STATUS
    # ========================================================

    st.markdown(
        "### 🟢 Database Status"
    )

    st.success(
        "PostgreSQL Connected • "
        "cybersecurity.network_flows"
    )

    st.caption(
        f"{total:,} network-flow records available "
        "through the CyberDemandIQ API."
    )