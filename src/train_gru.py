import os
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ============================================================
# CYBERDEMANDEIQ
# GRU SECURITY DEMAND FORECASTING
# ============================================================

X_PATH = "data/sequences/X_sequences.npy"
Y_PATH = "data/sequences/y_targets.npy"

MODEL_DIR = "models"
REPORT_DIR = "reports"


def main():

    print("=" * 70)
    print("CYBERDEMANDEIQ - GRU FORECASTING")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Load sequence data
    # --------------------------------------------------------

    print("\nLoading sequence data...")

    X = np.load(X_PATH)
    y = np.load(Y_PATH)

    print(f"X shape: {X.shape}")
    print(f"y shape: {y.shape}")

    # --------------------------------------------------------
    # 2. Same temporal split as LSTM
    # --------------------------------------------------------

    print("\nCreating temporal train/test split...")

    split_index = int(
        len(X) * 0.80
    )

    X_train = X[:split_index]
    X_test = X[split_index:]

    y_train = y[:split_index]
    y_test = y[split_index:]

    print(
        f"Training sequences: {len(X_train)}"
    )

    print(
        f"Testing sequences : {len(X_test)}"
    )

    # --------------------------------------------------------
    # 3. Build GRU
    # --------------------------------------------------------

    print("\nBuilding GRU model...")

    model = Sequential([
        GRU(
            64,
            return_sequences=True,
            input_shape=(
                X_train.shape[1],
                X_train.shape[2]
            )
        ),

        Dropout(0.20),

        GRU(
            32
        ),

        Dropout(0.20),

        Dense(
            16,
            activation="relu"
        ),

        Dense(
            1
        )
    ])

    model.compile(
        optimizer="adam",
        loss="mse",
        metrics=["mae"]
    )

    model.summary()

    # --------------------------------------------------------
    # 4. Early stopping
    # --------------------------------------------------------

    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=8,
        restore_best_weights=True
    )

    # --------------------------------------------------------
    # 5. Train
    # --------------------------------------------------------

    print("\nTraining GRU...")

    history = model.fit(
        X_train,
        y_train,
        validation_split=0.15,
        epochs=50,
        batch_size=64,
        callbacks=[
            early_stopping
        ],
        verbose=1
    )

    print("\nGRU training completed.")

    # --------------------------------------------------------
    # 6. Predictions
    # --------------------------------------------------------

    print("\nGenerating forecasts...")

    predictions = model.predict(
        X_test,
        verbose=0
    ).flatten()

    # --------------------------------------------------------
    # 7. Evaluation
    # --------------------------------------------------------

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    print("\n" + "=" * 70)
    print("GRU FORECASTING PERFORMANCE")
    print("=" * 70)

    print(
        f"\nMAE  : {mae:.6f}"
    )

    print(
        f"RMSE : {rmse:.6f}"
    )

    print(
        f"R²   : {r2:.6f}"
    )

    # --------------------------------------------------------
    # 8. Save model
    # --------------------------------------------------------

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    model_path = os.path.join(
        MODEL_DIR,
        "cyberdemandiq_gru.keras"
    )

    model.save(
        model_path
    )

    print(
        f"\nModel saved to: {model_path}"
    )

    # --------------------------------------------------------
    # 9. Save predictions
    # --------------------------------------------------------

    os.makedirs(
        REPORT_DIR,
        exist_ok=True
    )

    prediction_file = os.path.join(
        REPORT_DIR,
        "gru_predictions.csv"
    )

    prediction_data = np.column_stack(
        (
            y_test,
            predictions
        )
    )

    np.savetxt(
        prediction_file,
        prediction_data,
        delimiter=",",
        header="actual,predicted",
        comments=""
    )

    # --------------------------------------------------------
    # 10. Plot
    # --------------------------------------------------------

    plt.figure(
        figsize=(12, 6)
    )

    plt.plot(
        y_test,
        label="Actual"
    )

    plt.plot(
        predictions,
        label="GRU Forecast"
    )

    plt.xlabel(
        "Test Time Window"
    )

    plt.ylabel(
        "Scaled Security Demand"
    )

    plt.title(
        "CyberDemandIQ - GRU Security Demand Forecast"
    )

    plt.legend()

    plt.tight_layout()

    plot_path = os.path.join(
        REPORT_DIR,
        "gru_forecast.png"
    )

    plt.savefig(
        plot_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Forecast plot saved to: {plot_path}"
    )

    print("\n" + "=" * 70)
    print("GRU FORECASTING COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()