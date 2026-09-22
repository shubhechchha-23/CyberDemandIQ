from pathlib import Path
import pandas as pd
import re


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

RAW_DIR = Path("data/raw/MachineLearningCVE")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# CLEAN COLUMN NAMES
# ---------------------------------------------------------

def clean_column_name(column):
    """
    Standardize column names:
    - Remove leading/trailing spaces
    - Replace spaces with underscores
    - Remove special characters
    """
    column = column.strip()
    column = column.replace(" ", "_")
    column = re.sub(r"[^A-Za-z0-9_]", "", column)

    return column.lower()


# ---------------------------------------------------------
# CLEAN ONE CSV FILE
# ---------------------------------------------------------

def clean_file(file_path):

    print("\n" + "=" * 60)
    print(f"Processing: {file_path.name}")
    print("=" * 60)

    # Read CSV
    df = pd.read_csv(file_path, low_memory=False)

    print(f"Original shape: {df.shape}")

    # Clean column names
    df.columns = [clean_column_name(col) for col in df.columns]

    # Replace infinity values
    df = df.replace([float("inf"), float("-inf")], pd.NA)

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate rows
    duplicates = df.duplicated().sum()

    print(f"Duplicate rows found: {duplicates}")

    df = df.drop_duplicates()

    # Find label column
    label_columns = [col for col in df.columns if col == "label"]

    if label_columns:
        label_column = label_columns[0]

        # Clean labels
        df[label_column] = (
            df[label_column]
            .astype(str)
            .str.strip()
        )

        print("\nAttack/traffic labels:")
        print(df[label_column].value_counts())

    # Save cleaned file
    output_file = PROCESSED_DIR / f"cleaned_{file_path.name}"

    df.to_csv(output_file, index=False)

    print(f"\nCleaned shape: {df.shape}")
    print(f"Saved to: {output_file}")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    csv_files = sorted(RAW_DIR.glob("*.csv"))

    print("=" * 60)
    print("CYBERDEMANDIQ DATA CLEANING PIPELINE")
    print("=" * 60)

    print(f"\nCSV files found: {len(csv_files)}")

    if not csv_files:
        print("\nNo CSV files found!")
        return

    for file_path in csv_files:
        clean_file(file_path)

    print("\n" + "=" * 60)
    print("DATA CLEANING COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()