import os
import streamlit as st
import pandas as pd
import plotly.express as px
from xgboost import XGBClassifier


MODEL_PATH = "models/cyberdemandiq_xgboost.json"
DATA_PATH = "data/ml/security_features.csv"
IMPORTANCE_PATH = "models/feature_importance.csv"


# ============================================================
# CACHED MODEL
# ============================================================

@st.cache_resource
def load_model():

    model = XGBClassifier()
    model.load_model(MODEL_PATH)

    return model


# ============================================================
# CACHED FEATURES
# ============================================================

@st.cache_data
def get_features():

    df = pd.read_csv(
        DATA_PATH,
        nrows=1
    )

    return [
        c for c in df.columns
        if c not in [
            "flow_id",
            "source_file",
            "label",
            "attack_target"
        ]
    ]


# ============================================================
# CACHED SAMPLE
# ============================================================

@st.cache_data
def load_sample():

    return pd.read_csv(
        DATA_PATH,
        nrows=1
    )


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

@st.cache_data
def load_importance():

    if not os.path.exists(
        IMPORTANCE_PATH
    ):
        return None

    return pd.read_csv(
        IMPORTANCE_PATH
    )


# ============================================================
# DASHBOARD
# ============================================================

def show():

    st.subheader(
        "🤖 AI Detection Engine"
    )

    st.caption(
        "Real XGBoost-powered network attack detection"
    )

    # ========================================================
    # MODEL STATUS
    # ========================================================

    if not os.path.exists(
        MODEL_PATH
    ):

        st.error(
            "🔴 XGBoost model not found."
        )

        return

    st.success(
        "🟢 XGBoost Detection Model: ACTIVE"
    )

    st.divider()

    # ========================================================
    # MODEL PERFORMANCE
    # ========================================================

    st.markdown(
        "### 📊 Model Performance"
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Accuracy",
        "99.90%"
    )

    c2.metric(
        "Precision",
        "99.60%"
    )

    c3.metric(
        "Recall",
        "99.80%"
    )

    c4.metric(
        "F1 Score",
        "99.70%"
    )

    c5.metric(
        "ROC-AUC",
        "1.000"
    )

    st.divider()

    # ========================================================
    # TRAINING SUMMARY
    # ========================================================

    st.markdown(
        "### 🎯 Detection Summary"
    )

    a, b, c = st.columns(3)

    a.metric(
        "Training Samples",
        "2,059,411"
    )

    b.metric(
        "Testing Samples",
        "514,853"
    )

    c.metric(
        "Security Features",
        "38"
    )

    st.divider()

    # ========================================================
    # CONFUSION MATRIX
    # ========================================================

    st.markdown(
        "### 🧩 Confusion Matrix"
    )

    cm = pd.DataFrame(
        [
            ["BENIGN", "BENIGN", 429332],
            ["BENIGN", "ATTACK", 345],
            ["ATTACK", "BENIGN", 169],
            ["ATTACK", "ATTACK", 85007]
        ],
        columns=[
            "Actual",
            "Predicted",
            "Records"
        ]
    )

    matrix = cm.pivot(
        index="Actual",
        columns="Predicted",
        values="Records"
    )

    fig = px.imshow(
        matrix,
        text_auto=True,
        labels={
            "x": "Predicted",
            "y": "Actual",
            "color": "Records"
        }
    )

    fig.update_layout(
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ========================================================
    # FEATURE IMPORTANCE
    # ========================================================

    importance = load_importance()

    if importance is not None:

        st.markdown(
            "### 🔬 Top Security Features"
        )

        top_features = importance.head(
            15
        )

        fig = px.bar(
            top_features.sort_values(
                "importance",
                ascending=True
            ),
            x="importance",
            y="feature",
            orientation="h"
        )

        fig.update_layout(
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ========================================================
    # LIVE NETWORK FLOW ANALYSIS
    # ========================================================

    st.markdown(
        "### 🔮 Live Network Flow Analysis"
    )

    st.caption(
        "Enter network-flow values and run the trained "
        "XGBoost detector."
    )

    try:

        feature_names = get_features()

        model = load_model()

        sample = load_sample()

        # ----------------------------------------------------
        # SAMPLE FLOW
        # ----------------------------------------------------

        if st.button(
            "📥 Load Sample Network Flow"
        ):

            st.session_state[
                "sample_loaded"
            ] = True

        use_sample = st.session_state.get(
            "sample_loaded",
            False
        )

        inputs = {}

        cols = st.columns(3)

        for i, feature in enumerate(
            feature_names
        ):

            default = 0.0

            if (
                use_sample
                and feature in sample.columns
            ):

                value = sample.iloc[0][feature]

                if pd.notna(value):

                    default = float(
                        value
                    )

            with cols[i % 3]:

                inputs[feature] = st.number_input(
                    feature,
                    value=default,
                    format="%.6f",
                    key=f"input_{feature}"
                )

        st.divider()

        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        if st.button(
            "🚀 Analyze Network Flow",
            use_container_width=True
        ):

            X_input = pd.DataFrame(
                [inputs],
                columns=feature_names
            )

            probability = float(
                model.predict_proba(
                    X_input
                )[0][1]
            )

            prediction = int(
                model.predict(
                    X_input
                )[0]
            )

            st.divider()

            if prediction == 1:

                st.error(
                    "🚨 ATTACK DETECTED"
                )

                st.metric(
                    "Attack Probability",
                    f"{probability * 100:.2f}%"
                )

                if probability >= 0.90:

                    risk = "CRITICAL"

                elif probability >= 0.70:

                    risk = "HIGH"

                elif probability >= 0.40:

                    risk = "MEDIUM"

                else:

                    risk = "LOW"

                st.warning(
                    f"Risk Level: {risk}"
                )

            else:

                st.success(
                    "🟢 BENIGN TRAFFIC"
                )

                st.metric(
                    "Attack Probability",
                    f"{probability * 100:.2f}%"
                )

                st.info(
                    "The trained XGBoost model classified "
                    "this network flow as benign."
                )

    except Exception as e:

        st.error(
            "Prediction could not be completed."
        )

        st.code(
            str(e),
            language="text"
        )

    st.divider()

    # ========================================================
    # MODEL INFORMATION
    # ========================================================

    st.markdown(
        "### 🧠 Model Information"
    )

    st.info(
        "CyberDemandIQ uses a binary XGBoost classifier "
        "trained on 2,574,264 network-flow records and "
        "38 engineered cybersecurity features."
    )