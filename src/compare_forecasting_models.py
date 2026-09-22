import os
import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ============================================================
# CYBERDEMANDEIQ
# FORECASTING MODEL COMPARISON
# ============================================================

X_PATH = "data/sequences/X_sequences.npy"
Y_PATH = "data/sequences/y_targets.npy"

REPORT_DIR = "reports"


def evaluate_model(
    name,
    actual,
    predicted
):

    mae = mean_absolute_error(
        actual,
        predicted
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            predicted
        )
    )

    r2 = r2_score(
        actual,
        predicted
    )

    return {
        "model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }


def main():

    print("=" * 70)
    print("CYBERDEMANDEIQ - FORECASTING MODEL COMPARISON")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Load sequence data
    # --------------------------------------------------------

    X = np.load(
        X_PATH
    )

    y = np.load(
        Y_PATH
    )

    # --------------------------------------------------------
    # 2. Same temporal test split
    # --------------------------------------------------------

    split_index = int(
        len(X) * 0.80
    )

    X_test = X[split_index:]
    y_test = y[split_index:]

    # --------------------------------------------------------
    # 3. Persistence baseline
    #
    # Last value of previous sequence =
    # prediction for next demand
    # --------------------------------------------------------

    target_feature_index = 8

    persistence_predictions = (
        X_test[
            :,
            -1,
            target_feature_index
        ]
    )

    # --------------------------------------------------------
    # 4. Load saved LSTM predictions
    # --------------------------------------------------------

    lstm_predictions = pd.read_csv(
        "reports/lstm_predictions.csv"
    )

    lstm_actual = (
        lstm_predictions["actual"]
        .values
    )

    lstm_pred = (
        lstm_predictions["predicted"]
        .values
    )

    # --------------------------------------------------------
    # 5. Load saved GRU predictions
    # --------------------------------------------------------

    gru_predictions = pd.read_csv(
        "reports/gru_predictions.csv"
    )

    gru_actual = (
        gru_predictions["actual"]
        .values
    )

    gru_pred = (
        gru_predictions["predicted"]
        .values
    )

    # --------------------------------------------------------
    # 6. Evaluate all models
    # --------------------------------------------------------

    results = []

    results.append(
        evaluate_model(
            "Persistence Baseline",
            y_test,
            persistence_predictions
        )
    )

    results.append(
        evaluate_model(
            "LSTM",
            lstm_actual,
            lstm_pred
        )
    )

    results.append(
        evaluate_model(
            "GRU",
            gru_actual,
            gru_pred
        )
    )

    results_df = pd.DataFrame(
        results
    )

    # --------------------------------------------------------
    # 7. Print comparison
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("FORECASTING MODEL COMPARISON")
    print("=" * 70)

    print(
        results_df.to_string(
            index=False,
            float_format=lambda x: f"{x:.6f}"
        )
    )

    # --------------------------------------------------------
    # 8. Save results
    # --------------------------------------------------------

    os.makedirs(
        REPORT_DIR,
        exist_ok=True
    )

    output_path = os.path.join(
        REPORT_DIR,
        "forecasting_model_comparison.csv"
    )

    results_df.to_csv(
        output_path,
        index=False
    )

    print(
        f"\nComparison saved to:\n{output_path}"
    )

    print("\n" + "=" * 70)
    print("MODEL COMPARISON COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()