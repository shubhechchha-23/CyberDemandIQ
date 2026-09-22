import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib


# ============================================================
# CYBERDEMANDEIQ
# LSTM / GRU Sequence Preparation
# ============================================================

INPUT_PATH = "data/timeseries/security_demand_timeseries.csv"

OUTPUT_DIR = "data/sequences"

WINDOW_LENGTH = 12

FEATURE_COLUMNS = [
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


def main():

    print("=" * 70)
    print("CYBERDEMANDEIQ - SEQUENCE PREPARATION")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Load time-series data
    # --------------------------------------------------------

    print("\nLoading time-series dataset...")

    df = pd.read_csv(
        INPUT_PATH
    )

    print(
        f"Rows loaded: {len(df):,}"
    )

    # --------------------------------------------------------
    # 2. Sort correctly
    # --------------------------------------------------------

    df = df.sort_values(
        [
            "source_file",
            "window_id"
        ]
    ).reset_index(
        drop=True
    )

    # --------------------------------------------------------
    # 3. Create output directory
    # --------------------------------------------------------

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    all_X = []
    all_y = []

    # --------------------------------------------------------
    # 4. Create sequences separately for each source
    # --------------------------------------------------------

    print("\nCreating temporal sequences...")

    for source_name, group in df.groupby(
        "source_file"
    ):

        group = group.sort_values(
            "window_id"
        ).reset_index(
            drop=True
        )

        # Skip very small groups
        if len(group) <= WINDOW_LENGTH:
            continue

        values = group[
            FEATURE_COLUMNS
        ].astype(float).values

        # ----------------------------------------------------
        # Scale each source independently
        # ----------------------------------------------------

        scaler = MinMaxScaler()

        scaled_values = scaler.fit_transform(
            values
        )

        scaler_name = (
            source_name
            .replace(".csv", "")
            .replace(".pcap_ISCX", "")
            .replace("/", "_")
            .replace("\\", "_")
        )

        scaler_path = os.path.join(
            OUTPUT_DIR,
            f"{scaler_name}_scaler.pkl"
        )

        joblib.dump(
            scaler,
            scaler_path
        )

        # ----------------------------------------------------
        # Sliding-window sequences
        # ----------------------------------------------------

        for i in range(
            len(scaled_values) - WINDOW_LENGTH
        ):

            X_sequence = scaled_values[
                i:i + WINDOW_LENGTH
            ]

            y_target = scaled_values[
                i + WINDOW_LENGTH,
                FEATURE_COLUMNS.index(
                    "security_demand_score"
                )
            ]

            all_X.append(
                X_sequence
            )

            all_y.append(
                y_target
            )

    # --------------------------------------------------------
    # 5. Convert to NumPy arrays
    # --------------------------------------------------------

    X = np.array(
        all_X,
        dtype=np.float32
    )

    y = np.array(
        all_y,
        dtype=np.float32
    )

    # --------------------------------------------------------
    # 6. Save
    # --------------------------------------------------------

    X_path = os.path.join(
        OUTPUT_DIR,
        "X_sequences.npy"
    )

    y_path = os.path.join(
        OUTPUT_DIR,
        "y_targets.npy"
    )

    np.save(
        X_path,
        X
    )

    np.save(
        y_path,
        y
    )

    # --------------------------------------------------------
    # 7. Print information
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("SEQUENCE DATASET SUMMARY")
    print("=" * 70)

    print(
        f"\nSequence length : {WINDOW_LENGTH}"
    )

    print(
        f"Features        : {len(FEATURE_COLUMNS)}"
    )

    print(
        f"X shape         : {X.shape}"
    )

    print(
        f"y shape         : {y.shape}"
    )

    print("\nFeature order:")

    for index, feature in enumerate(
        FEATURE_COLUMNS,
        start=1
    ):

        print(
            f"{index:02d}. {feature}"
        )

    print("\nSaved files:")

    print(
        X_path
    )

    print(
        y_path
    )

    print("\n" + "=" * 70)
    print("SEQUENCE PREPARATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()