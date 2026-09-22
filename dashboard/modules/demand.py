import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import os


X_PATH = "data/sequences/X_sequences.npy"
Y_PATH = "data/sequences/y_targets.npy"


@st.cache_data
def load_sequences():

    X = np.load(X_PATH)
    y = np.load(Y_PATH)

    return X, y


def show():

    st.subheader("📈 Security Demand Intelligence")

    st.caption(
        "Temporal analysis of cybersecurity demand and attack activity"
    )

    try:

        X, y = load_sequences()

        # =====================================================
        # DATA SUMMARY
        # =====================================================

        sequence_count = X.shape[0]
        sequence_length = X.shape[1]
        feature_count = X.shape[2]

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "🔢 Sequences",
            f"{sequence_count:,}"
        )

        c2.metric(
            "⏱️ Sequence Length",
            sequence_length
        )

        c3.metric(
            "🧩 Features",
            feature_count
        )

        c4.metric(
            "🎯 Target Samples",
            f"{len(y):,}"
        )

        st.divider()

        # =====================================================
        # FEATURE NAMES
        # =====================================================

        feature_names = [
            "attack_rate",
            "avg_risk_score",
            "avg_attack_probability",
            "avg_packet_rate",
            "avg_byte_rate",
            "avg_packet_size",
            "avg_flow_duration",
            "avg_iat",
            "security_demand_score"
        ]

        # =====================================================
        # TEMPORAL DEMAND
        # =====================================================

        st.markdown(
            "### 📊 Security Demand Trend"
        )

        demand_index = np.mean(
            X[:, :, 8],
            axis=1
        )

        trend = pd.DataFrame({
            "Sequence": np.arange(
                len(demand_index)
            ),
            "Security Demand": demand_index
        })

        fig = px.line(
            trend,
            x="Sequence",
            y="Security Demand"
        )

        fig.update_layout(
            height=450,
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

        # =====================================================
        # FEATURE ANALYSIS
        # =====================================================

        st.markdown(
            "### 🧠 Temporal Feature Analysis"
        )

        feature_means = np.mean(
            X,
            axis=(0, 1)
        )

        feature_df = pd.DataFrame({
            "Feature": feature_names,
            "Average Value": feature_means
        })

        fig2 = px.bar(
            feature_df.sort_values(
                "Average Value"
            ),
            x="Average Value",
            y="Feature",
            orientation="h"
        )

        fig2.update_layout(
            height=500
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        st.divider()

        # =====================================================
        # MODEL PERFORMANCE
        # =====================================================

        st.markdown(
            "### 🎯 Demand Forecast Performance"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "MAE",
            "0.079849"
        )

        c2.metric(
            "RMSE",
            "0.106107"
        )

        c3.metric(
            "R²",
            "0.925346"
        )

        st.caption(
            "Metrics from the trained temporal security-demand model."
        )

        st.divider()

        # =====================================================
        # LATEST SECURITY STATE
        # =====================================================

        latest = X[-1]

        st.markdown(
            "### 🔎 Latest Security State"
        )

        cols = st.columns(3)

        for i, feature in enumerate(feature_names):

            with cols[i % 3]:

                value = float(
                    np.mean(
                        latest[:, i]
                    )
                )

                st.metric(
                    feature.replace(
                        "_",
                        " "
                    ).title(),
                    f"{value:.4f}"
                )

    except Exception as e:

        st.error(
            "Unable to load security-demand data."
        )

        st.code(
            str(e),
            language="text"
        )