import os
import pandas as pd
import numpy as np


# ============================================================
# CYBERDEMANDEIQ
# Cybersecurity Traffic Time-Series Preparation
# ============================================================

INPUT_PATH = "data/risk/risk_scored_flows.csv"

OUTPUT_DIR = "data/timeseries"

OUTPUT_PATH = os.path.join(
    OUTPUT_DIR,
    "security_demand_timeseries.csv"
)


def main():

    print("=" * 70)
    print("CYBERDEMANDEIQ - SECURITY TIME-SERIES ENGINE")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Load risk-scored network flows
    # --------------------------------------------------------

    print("\nLoading risk-scored data...")

    df = pd.read_csv(INPUT_PATH)

    print(
        f"Rows loaded: {len(df):,}"
    )

    # --------------------------------------------------------
    # 2. Preserve original ordering
    # --------------------------------------------------------

    df["flow_sequence"] = np.arange(
        len(df)
    )

    # --------------------------------------------------------
    # 3. Create ordered windows
    #
    # 1000 flows = one traffic window
    # --------------------------------------------------------

    WINDOW_SIZE = 1000

    df["window_id"] = (
        df["flow_sequence"] // WINDOW_SIZE
    )

    # --------------------------------------------------------
    # 4. Aggregate cybersecurity demand
    # --------------------------------------------------------

    print("\nCreating traffic windows...")

    timeseries = (
        df.groupby(
            [
                "source_file",
                "window_id"
            ]
        )
        .agg(
            total_flows=(
                "flow_sequence",
                "count"
            ),

            attack_flows=(
                "attack_target",
                "sum"
            ),

            avg_risk_score=(
                "risk_score",
                "mean"
            ),

            max_risk_score=(
                "risk_score",
                "max"
            ),

            avg_attack_probability=(
                "attack_probability",
                "mean"
            ),

            avg_packet_rate=(
                "total_packet_rate",
                "mean"
            ),

            avg_byte_rate=(
                "total_byte_rate",
                "mean"
            ),

            avg_packet_size=(
                "average_packet_size",
                "mean"
            ),

            avg_flow_duration=(
                "flow_duration",
                "mean"
            ),

            avg_iat=(
                "flow_iat_mean",
                "mean"
            )
        )
        .reset_index()
    )

    # --------------------------------------------------------
    # 5. Attack rate
    # --------------------------------------------------------

    timeseries["attack_rate"] = (
        timeseries["attack_flows"]
        / timeseries["total_flows"]
    )

    # --------------------------------------------------------
    # 6. Security demand index
    # --------------------------------------------------------

    timeseries["security_demand_index"] = (
        0.40 * timeseries["attack_rate"]
        + 0.30 * (
            timeseries["avg_risk_score"] / 100
        )
        + 0.20 * timeseries[
            "avg_attack_probability"
        ]
        + 0.10 * (
            timeseries["max_risk_score"] / 100
        )
    )

    # --------------------------------------------------------
    # 7. Convert to 0-100 scale
    # --------------------------------------------------------

    timeseries["security_demand_score"] = (
        timeseries[
            "security_demand_index"
        ] * 100
    )

    # --------------------------------------------------------
    # 8. Demand category
    # --------------------------------------------------------

    timeseries["demand_level"] = pd.cut(
        timeseries[
            "security_demand_score"
        ],
        bins=[
            -np.inf,
            20,
            50,
            80,
            np.inf
        ],
        labels=[
            "LOW",
            "MEDIUM",
            "HIGH",
            "CRITICAL"
        ]
    )

    # --------------------------------------------------------
    # 9. Sort
    # --------------------------------------------------------

    timeseries = timeseries.sort_values(
        [
            "source_file",
            "window_id"
        ]
    )

    # --------------------------------------------------------
    # 10. Save
    # --------------------------------------------------------

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    timeseries.to_csv(
        OUTPUT_PATH,
        index=False
    )

    # --------------------------------------------------------
    # 11. Summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("TIME-SERIES SUMMARY")
    print("=" * 70)

    print(
        f"\nTotal windows: "
        f"{len(timeseries):,}"
    )

    print(
        f"\nAverage security demand: "
        f"{timeseries['security_demand_score'].mean():.2f}"
    )

    print("\nDemand levels:")

    print(
        timeseries[
            "demand_level"
        ].value_counts()
    )

    print("\nSaved to:")

    print(
        OUTPUT_PATH
    )

    print("\n" + "=" * 70)
    print("TIME-SERIES CREATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()