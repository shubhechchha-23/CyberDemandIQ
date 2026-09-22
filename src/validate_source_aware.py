import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)
from xgboost import XGBClassifier


# ============================================================
# CYBERDEMANDEIQ
# Source-Aware Cybersecurity Validation
# ============================================================

DATA_PATH = "data/ml/security_features.csv"

RANDOM_STATE = 42


def main():

    print("=" * 70)
    print("CYBERDEMANDEIQ - SOURCE-AWARE VALIDATION")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Load data
    # --------------------------------------------------------

    print("\nLoading dataset...")

    df = pd.read_csv(DATA_PATH)

    print(f"Rows: {len(df):,}")

    # --------------------------------------------------------
    # 2. Inspect sources
    # --------------------------------------------------------

    print("\nSource distribution:")

    print(
        df["source_file"]
        .value_counts()
        .to_string()
    )

    # --------------------------------------------------------
    # 3. Separate features and target
    # --------------------------------------------------------

    drop_columns = [
        "flow_id",
        "source_file",
        "label",
        "attack_target"
    ]

    X = df.drop(
        columns=drop_columns,
        errors="ignore"
    )

    y = df["attack_target"]

    # --------------------------------------------------------
    # 4. Source-aware split
    #
    # Hold out Wednesday as unseen source data.
    # --------------------------------------------------------

    test_source = "cleaned_Wednesday-workingHours.pcap_ISCX.csv"

    train_mask = df["source_file"] != test_source
    test_mask = df["source_file"] == test_source

    X_train = X.loc[train_mask]
    y_train = y.loc[train_mask]

    X_test = X.loc[test_mask]
    y_test = y.loc[test_mask]

    print("\nSource-aware split:")

    print(
        f"Training rows: {len(X_train):,}"
    )

    print(
        f"Testing rows : {len(X_test):,}"
    )

    print("\nTraining labels:")

    print(
        y_train.value_counts()
    )

    print("\nTesting labels:")

    print(
        y_test.value_counts()
    )

    # --------------------------------------------------------
    # 5. Train model
    # --------------------------------------------------------

    print("\nTraining XGBoost...")

    model = XGBClassifier(
        n_estimators=300,
        max_depth=8,
        learning_rate=0.08,
        subsample=0.85,
        colsample_bytree=0.85,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=RANDOM_STATE,
        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train
    )

    print("Training completed.")

    # --------------------------------------------------------
    # 6. Predictions
    # --------------------------------------------------------

    y_pred = model.predict(
        X_test
    )

    y_probability = model.predict_proba(
        X_test
    )[:, 1]

    # --------------------------------------------------------
    # 7. Metrics
    # --------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    print("\n" + "=" * 70)
    print("SOURCE-AWARE PERFORMANCE")
    print("=" * 70)

    print(f"\nAccuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    # ROC-AUC only if both classes exist
    if len(y_test.unique()) == 2:

        auc = roc_auc_score(
            y_test,
            y_probability
        )

        print(f"ROC-AUC  : {auc:.4f}")

    else:

        print(
            "ROC-AUC  : Not available "
            "(only one class in test source)"
        )

    # --------------------------------------------------------
    # 8. Confusion matrix
    # --------------------------------------------------------

    print("\nConfusion Matrix:")

    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )

    print("\n" + "=" * 70)
    print("SOURCE-AWARE VALIDATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()