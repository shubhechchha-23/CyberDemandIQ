import os
import pandas as pd
import psycopg2


# ============================================================
# CYBERDEMANDEIQ
# PostgreSQL → ML Dataset Preparation
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "cyberdemandiq",
    "user": "postgres",
    "password": "your_postgresql_password"
}


OUTPUT_DIR = "data/ml"


# ============================================================
# Connect to PostgreSQL
# ============================================================

def get_connection():

    return psycopg2.connect(**DB_CONFIG)


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 70)
    print("CYBERDEMANDEIQ - ML DATA PREPARATION")
    print("=" * 70)

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    try:

        connection = get_connection()

        print("\nPostgreSQL connection successful!")

    except Exception as error:

        print("\nDatabase connection failed.")
        print(error)

        return


    # ========================================================
    # Load engineered cybersecurity features
    # ========================================================

    query = """
        SELECT *
        FROM analytics.security_features;
    """

    print("\nExtracting security features from PostgreSQL...")

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()


    # ========================================================
    # Basic inspection
    # ========================================================

    print("\nDataset loaded successfully.")

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    print("\nTarget distribution:")

    print(
        df["attack_target"]
        .value_counts()
        .sort_index()
    )


    # ========================================================
    # Handle infinite values
    # ========================================================

    print("\nCleaning infinite values...")

    df.replace(
        [float("inf"), float("-inf")],
        pd.NA,
        inplace=True
    )


    # ========================================================
    # Handle missing values
    # ========================================================

    missing_before = df.isna().sum().sum()

    print(
        f"Missing values before cleaning: "
        f"{missing_before:,}"
    )

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    df[numeric_columns] = df[numeric_columns].fillna(
        df[numeric_columns].median()
    )


    missing_after = df.isna().sum().sum()

    print(
        f"Missing values after cleaning: "
        f"{missing_after:,}"
    )


    # ========================================================
    # Save complete ML dataset
    # ========================================================

    output_path = os.path.join(
        OUTPUT_DIR,
        "security_features.csv"
    )

    print("\nSaving ML dataset...")

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved to: {output_path}"
    )


    # ========================================================
    # Create X and y
    # ========================================================

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


    print("\nML matrix:")

    print(
        f"X shape: {X.shape}"
    )

    print(
        f"y shape: {y.shape}"
    )


    # ========================================================
    # Save X and y
    # ========================================================

    X.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "X_features.csv"
        ),
        index=False
    )

    y.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "y_target.csv"
        ),
        index=False
    )


    print("\n" + "=" * 70)
    print("ML DATA PREPARATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()