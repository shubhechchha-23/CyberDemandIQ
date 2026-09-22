import os
import numpy as np
import pandas as pd


# ============================================================
# CYBERDEMANDEIQ
# PREDICTIVE CYBERSECURITY RESPONSE INTELLIGENCE
# ============================================================

INPUT_PATH = (
    "data/timeseries/"
    "security_demand_timeseries.csv"
)

OUTPUT_DIR = "data/intelligence"

OUTPUT_PATH = os.path.join(
    OUTPUT_DIR,
    "security_response_recommendations.csv"
)


# ============================================================
# Response Policy
# ============================================================

def determine_response_level(score):

    if score < 20:
        return "NORMAL"

    elif score < 50:
        return "ELEVATED"

    elif score < 80:
        return "HIGH_ALERT"

    else:
        return "CRITICAL"


def determine_recommended_action(score):

    if score < 20:

        return (
            "Continue routine monitoring"
        )

    elif score < 50:

        return (
            "Increase monitoring frequency "
            "and inspect emerging anomalies"
        )

    elif score < 80:

        return (
            "Prioritize security investigation "
            "and prepare additional response capacity"
        )

    else:

        return (
            "Activate high-priority incident "
            "response workflow"
        )


def main():

    print("=" * 70)
    print(
        "CYBERDEMANDEIQ - RESPONSE INTELLIGENCE"
    )
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Load security demand time series
    # --------------------------------------------------------

    print("\nLoading security demand data...")

    df = pd.read_csv(
        INPUT_PATH
    )

    print(
        f"Rows loaded: {len(df):,}"
    )

    # --------------------------------------------------------
    # 2. Calculate rolling security pressure
    # --------------------------------------------------------

    print(
        "\nCalculating rolling security pressure..."
    )

    df["rolling_attack_rate"] = (
        df.groupby("source_file")[
            "attack_rate"
        ]
        .transform(
            lambda x: x.rolling(
                window=5,
                min_periods=1
            ).mean()
        )
    )

    df["rolling_risk_score"] = (
        df.groupby("source_file")[
            "avg_risk_score"
        ]
        .transform(
            lambda x: x.rolling(
                window=5,
                min_periods=1
            ).mean()
        )
    )

    # --------------------------------------------------------
    # 3. Detect demand acceleration
    # --------------------------------------------------------

    df["demand_change"] = (
        df.groupby("source_file")[
            "security_demand_score"
        ]
        .diff()
        .fillna(0)
    )

    # --------------------------------------------------------
    # 4. Future response pressure
    # --------------------------------------------------------

    df["response_pressure"] = (

        0.50
        * df["security_demand_score"]

        +

        0.25
        * df["rolling_risk_score"]

        +

        0.15
        * (
            df["rolling_attack_rate"]
            * 100
        )

        +

        0.10
        * df["demand_change"].clip(
            lower=0
        )

    )

    # --------------------------------------------------------
    # 5. Normalize response pressure
    # --------------------------------------------------------

    df["response_pressure"] = (
        df["response_pressure"]
        .clip(
            lower=0,
            upper=100
        )
    )

    # --------------------------------------------------------
    # 6. Response level
    # --------------------------------------------------------

    df["response_level"] = (
        df["response_pressure"]
        .apply(
            determine_response_level
        )
    )

    # --------------------------------------------------------
    # 7. Recommended action
    # --------------------------------------------------------

    df["recommended_action"] = (
        df["response_pressure"]
        .apply(
            determine_recommended_action
        )
    )

    # --------------------------------------------------------
    # 8. Security capacity indicator
    # --------------------------------------------------------

    df["recommended_capacity_index"] = (
        1
        +
        df["response_pressure"] / 100
    )

    # --------------------------------------------------------
    # 9. Save
    # --------------------------------------------------------

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    # --------------------------------------------------------
    # 10. Summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print(
        "RESPONSE INTELLIGENCE SUMMARY"
    )
    print("=" * 70)

    print(
        "\nAverage response pressure:"
    )

    print(
        round(
            df[
                "response_pressure"
            ].mean(),
            2
        )
    )

    print(
        "\nResponse level distribution:"
    )

    print(
        df[
            "response_level"
        ]
        .value_counts()
    )

    print(
        "\nAverage recommended capacity index:"
    )

    print(
        round(
            df[
                "recommended_capacity_index"
            ].mean(),
            3
        )
    )

    print(
        "\nSaved to:"
    )

    print(
        OUTPUT_PATH
    )

    print("\n" + "=" * 70)
    print(
        "RESPONSE INTELLIGENCE COMPLETED"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()