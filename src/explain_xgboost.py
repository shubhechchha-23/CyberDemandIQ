import os
import pandas as pd
import matplotlib.pyplot as plt

MODEL_DIR = "models"
OUTPUT_DIR = "reports"

INPUT_FILE = os.path.join(
    MODEL_DIR,
    "feature_importance.csv"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


def main():

    print("=" * 70)
    print("CYBERDEMANDEIQ - XGBOOST EXPLAINABILITY")
    print("=" * 70)

    df = pd.read_csv(INPUT_FILE)

    df = df.sort_values(
        by="importance",
        ascending=False
    )

    print("\nTop 20 security features:\n")

    print(
        df.head(20).to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Top 15 feature importance visualization
    # --------------------------------------------------------

    top_features = df.head(15).sort_values(
        by="importance"
    )

    plt.figure(
        figsize=(10, 7)
    )

    plt.barh(
        top_features["feature"],
        top_features["importance"]
    )

    plt.xlabel("XGBoost Importance")
    plt.ylabel("Security Feature")
    plt.title(
        "CyberDemandIQ - Top Security Features"
    )

    plt.tight_layout()

    output_path = os.path.join(
        OUTPUT_DIR,
        "xgboost_feature_importance.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"\nVisualization saved to:\n{output_path}"
    )

    print("\n" + "=" * 70)
    print("EXPLAINABILITY ANALYSIS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()