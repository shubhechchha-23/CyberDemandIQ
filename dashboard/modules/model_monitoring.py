import streamlit as st
import pandas as pd
import numpy as np
import os
from xgboost import XGBClassifier

MODEL_PATH = "models/cyberdemandiq_xgboost.json"
DATA_PATH = "data/ml/security_features.csv"


@st.cache_resource
def load_model():

    model = XGBClassifier()

    model.load_model(
        MODEL_PATH
    )

    return model


@st.cache_data
def load_data():

    return pd.read_csv(
        DATA_PATH,
        nrows=10000
    )


def show():

    st.subheader("🧪 ML Model Monitoring")

    st.caption(
        "Monitoring the health, predictions and feature behavior "
        "of the CyberDemandIQ detection model"
    )

    # =========================================================
    # MODEL STATUS
    # =========================================================

    model_active = os.path.exists(
        MODEL_PATH
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🤖 Model",
        "XGBoost"
    )

    c2.metric(
        "🟢 Status",
        "ACTIVE" if model_active else "OFFLINE"
    )

    c3.metric(
        "🧩 Features",
        "38"
    )

    c4.metric(
        "📦 Model Format",
        "JSON"
    )

    st.divider()

    if not model_active:

        st.error(
            "XGBoost model file was not found."
        )

        return

    # =========================================================
    # LOAD MODEL
    # =========================================================

    try:

        model = load_model()

        df = load_data()

    except Exception as e:

        st.error(
            "Unable to load model monitoring data."
        )

        st.code(
            str(e),
            language="text"
        )

        return

    # =========================================================
    # MODEL CONFIGURATION
    # =========================================================

    st.markdown(
        "### ⚙️ Model Configuration"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Estimators",
        "300"
    )

    c2.metric(
        "Max Depth",
        "8"
    )

    c3.metric(
        "Learning Rate",
        "0.08"
    )

    c4.metric(
        "Objective",
        "Binary"
    )

    st.divider()

    # =========================================================
    # FEATURE HEALTH
    # =========================================================

    st.markdown(
        "### 🔬 Feature Health"
    )

    feature_columns = [
        c for c in df.columns
        if c not in [
            "flow_id",
            "source_file",
            "label",
            "attack_target"
        ]
    ]

    missing_values = (
        df[feature_columns]
        .isnull()
        .sum()
        .sum()
    )

    numeric_features = (
        df[feature_columns]
        .select_dtypes(
            include=np.number
        )
        .shape[1]
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Security Features",
        len(feature_columns)
    )

    c2.metric(
        "Numeric Features",
        numeric_features
    )

    c3.metric(
        "Missing Values",
        f"{missing_values:,}"
    )

    if missing_values == 0:

        st.success(
            "🟢 Feature pipeline is healthy — no missing values detected."
        )

    else:

        st.warning(
            f"⚠️ {missing_values:,} missing feature values detected."
        )

    st.divider()

    # =========================================================
    # MODEL FEATURE IMPORTANCE
    # =========================================================

    st.markdown(
        "### 📊 Model Feature Importance"
    )

    importance = pd.DataFrame({
        "Feature": feature_columns,
        "Importance": model.feature_importances_
    })

    importance = importance.sort_values(
        "Importance",
        ascending=False
    )

    st.dataframe(
        importance,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =========================================================
    # PREDICTION MONITORING
    # =========================================================

    st.markdown(
        "### 🔎 Prediction Monitoring"
    )

    X = df[feature_columns]

    predictions = model.predict(
        X
    )

    probabilities = model.predict_proba(
        X
    )[:, 1]

    attack_predictions = int(
        predictions.sum()
    )

    benign_predictions = int(
        len(predictions) -
        attack_predictions
    )

    avg_probability = float(
        probabilities.mean()
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🟢 Predicted Benign",
        f"{benign_predictions:,}"
    )

    c2.metric(
        "🚨 Predicted Attacks",
        f"{attack_predictions:,}"
    )

    c3.metric(
        "📈 Avg Attack Probability",
        f"{avg_probability * 100:.2f}%"
    )

    st.divider()

    # =========================================================
    # PREDICTION DISTRIBUTION
    # =========================================================

    st.markdown(
        "### 📡 Prediction Distribution"
    )

    prediction_df = pd.DataFrame({
        "Prediction": [
            "BENIGN",
            "ATTACK"
        ],
        "Records": [
            benign_predictions,
            attack_predictions
        ]
    })

    st.bar_chart(
        prediction_df.set_index(
            "Prediction"
        )
    )

    st.divider()

    # =========================================================
    # MODEL HEALTH
    # =========================================================

    st.markdown(
        "### 💚 Model Health"

    )

    health_checks = [
        ("Model File", model_active),
        ("38 Features Available", len(feature_columns) == 38),
        ("Numeric Feature Pipeline", numeric_features == 38),
        ("No Missing Values", missing_values == 0)
    ]

    for name, status in health_checks:

        if status:

            st.success(
                f"🟢 {name}"
            )

        else:

            st.error(
                f"🔴 {name}"
            )

    st.divider()

    st.info(
        "Model monitoring currently evaluates model availability, "
        "feature integrity, missing values, feature importance and "
        "prediction distribution using the real CyberDemandIQ data."
    )