import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from xgboost import XGBClassifier


# ============================================================
# CYBERDEMANDEIQ
# XGBoost Cybersecurity Attack Detector
# ============================================================

DATA_PATH = "data/ml/security_features.csv"
MODEL_DIR = "models"

RANDOM_STATE = 42


def main():

    print("=" * 70)
    print("CYBERDEMANDEIQ - XGBOOST ATTACK DETECTOR")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Load engineered dataset
    # --------------------------------------------------------

    print("\nLoading ML dataset...")

    df = pd.read_csv(DATA_PATH)

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    # --------------------------------------------------------
    # 2. Separate target and metadata
    # --------------------------------------------------------

    X = df.drop(
        columns=[
            "flow_id",
            "source_file",
            "label",
            "attack_target"
        ],
        errors="ignore"
    )

    y = df["attack_target"]

    print("\nFeature matrix:")
    print(f"X shape: {X.shape}")
    print(f"y shape: {y.shape}")

    # --------------------------------------------------------
    # 3. Train / Test split
    # --------------------------------------------------------

    print("\nCreating stratified train/test split...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y
    )

    print(f"Training samples : {len(X_train):,}")
    print(f"Testing samples  : {len(X_test):,}")

    # --------------------------------------------------------
    # 4. XGBoost model
    # --------------------------------------------------------

    print("\nInitializing XGBoost...")

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

    # --------------------------------------------------------
    # 5. Train
    # --------------------------------------------------------

    print("\nTraining XGBoost model...")
    print("This may take some time.")

    model.fit(
        X_train,
        y_train
    )

    print("Training completed.")

    # --------------------------------------------------------
    # 6. Predictions
    # --------------------------------------------------------

    print("\nGenerating predictions...")

    y_pred = model.predict(X_test)

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
        y_pred
    )

    recall = recall_score(
        y_test,
        y_pred
    )

    f1 = f1_score(
        y_test,
        y_pred
    )

    auc = roc_auc_score(
        y_test,
        y_probability
    )

    print("\n" + "=" * 70)
    print("MODEL PERFORMANCE")
    print("=" * 70)

    print(f"\nAccuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {auc:.4f}")

    # --------------------------------------------------------
    # 8. Classification report
    # --------------------------------------------------------

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=[
                "BENIGN",
                "ATTACK"
            ]
        )
    )

    # --------------------------------------------------------
    # 9. Confusion matrix
    # --------------------------------------------------------

    print("Confusion Matrix:")

    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )

    # --------------------------------------------------------
    # 10. Feature importance
    # --------------------------------------------------------

    feature_importance = pd.DataFrame({
        "feature": X.columns,
        "importance": model.feature_importances_
    })

    feature_importance = feature_importance.sort_values(
        by="importance",
        ascending=False
    )

    print("\nTop 20 Security Features:")

    print(
        feature_importance.head(20).to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # 11. Save model
    # --------------------------------------------------------

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    model_path = os.path.join(
        MODEL_DIR,
        "cyberdemandiq_xgboost.json"
    )

    model.save_model(
        model_path
    )

    print(
        f"\nModel saved to: {model_path}"
    )

    # --------------------------------------------------------
    # 12. Save feature importance
    # --------------------------------------------------------

    importance_path = os.path.join(
        MODEL_DIR,
        "feature_importance.csv"
    )

    feature_importance.to_csv(
        importance_path,
        index=False
    )

    print(
        f"Feature importance saved to: "
        f"{importance_path}"
    )

    print("\n" + "=" * 70)
    print("XGBOOST TRAINING COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()