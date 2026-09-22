import os
import pandas as pd
import numpy as np
import xgboost as xgb


# ============================================================
# CYBERDEMANDEIQ
# AI-Based Cyber Risk Scoring Engine
# ============================================================

DATA_PATH = "data/ml/security_features.csv"
MODEL_PATH = "models/cyberdemandiq_xgboost.json"

OUTPUT_DIR = "data/risk"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "risk_scored_flows.csv"
)


def calculate_risk_score(probability):
    """
    Convert attack probability into a 0-100 risk score.
    """

    return np.round(
        probability * 100,
        2
    )


def classify_risk(score):

    if score < 20:
        return "LOW"

    elif score < 50:
        return "MEDIUM"

    elif score < 80:
        return "HIGH"

    else:
        return "CRITICAL"


def main():

    print("=" * 70)
    print("CYBERDEMANDEIQ - AI CYBER RISK SCORING ENGINE")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Load dataset
    # --------------------------------------------------------

    print("\nLoading security dataset...")

    df = pd.read_csv(
        DATA_PATH
    )

    print(
        f"Rows loaded: {len(df):,}"
    )

    # --------------------------------------------------------
    # 2. Prepare ML features
    # --------------------------------------------------------

    metadata_columns = [
        "flow_id",
        "source_file",
        "label",
        "attack_target"
    ]

    X = df.drop(
        columns=metadata_columns,
        errors="ignore"
    )

    # --------------------------------------------------------
    # 3. Load trained XGBoost model
    # --------------------------------------------------------

    print("\nLoading trained XGBoost model...")

    model = xgb.XGBClassifier()

    model.load_model(
        MODEL_PATH
    )

    print("Model loaded successfully.")

    # --------------------------------------------------------
    # 4. Generate attack probabilities
    # --------------------------------------------------------

    print("\nGenerating attack probabilities...")

    attack_probability = model.predict_proba(
        X
    )[:, 1]

    # --------------------------------------------------------
    # 5. Convert probability → risk score
    # --------------------------------------------------------

    df["attack_probability"] = np.round(
        attack_probability,
        6
    )

    df["risk_score"] = calculate_risk_score(
        attack_probability
    )

    # --------------------------------------------------------
    # 6. Risk category
    # --------------------------------------------------------

    df["risk_level"] = [
        classify_risk(score)
        for score in df["risk_score"]
    ]

    # --------------------------------------------------------
    # 7. Recommended action
    # --------------------------------------------------------

    df["recommended_action"] = np.select(
        [
            df["risk_level"] == "LOW",
            df["risk_level"] == "MEDIUM",
            df["risk_level"] == "HIGH",
            df["risk_level"] == "CRITICAL"
        ],
        [
            "Monitor",
            "Investigate",
            "Prioritize Investigation",
            "Immediate Response"
        ],
        default="Monitor"
    )

    # --------------------------------------------------------
    # 8. Create output directory
    # --------------------------------------------------------

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    # --------------------------------------------------------
    # 9. Save results
    # --------------------------------------------------------

    print("\nSaving risk-scored dataset...")

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # --------------------------------------------------------
    # 10. Summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("RISK DISTRIBUTION")
    print("=" * 70)

    print(
        df["risk_level"]
        .value_counts()
    )

    print("\nAverage risk score:")

    print(
        round(
            df["risk_score"].mean(),
            2
        )
    )

    print("\nMaximum risk score:")

    print(
        df["risk_score"].max()
    )

    print("\nSaved to:")

    print(
        OUTPUT_FILE
    )

    print("\n" + "=" * 70)
    print("CYBER RISK SCORING COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()