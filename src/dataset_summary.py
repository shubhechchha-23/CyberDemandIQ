from pathlib import Path
import pandas as pd

PROCESSED_DIR = Path("data/processed")

files = sorted(PROCESSED_DIR.glob("cleaned_*.csv"))

print("=" * 80)
print("CYBERDEMANDEIQ - COMPLETE DATASET SUMMARY")
print("=" * 80)

total_rows = 0

for file in files:

    df = pd.read_csv(file, low_memory=False)

    total_rows += len(df)

    print("\n" + "-" * 80)
    print(f"FILE: {file.name}")
    print("-" * 80)

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    if "label" in df.columns:
        print("\nLabels:")
        print(df["label"].value_counts().to_string())

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if len(missing) > 0:
        print("\nMissing values:")
        print(missing.to_string())
    else:
        print("\nMissing values: None")

print("\n" + "=" * 80)
print("TOTAL ROWS ACROSS ALL FILES")
print("=" * 80)

print(f"{total_rows:,}")

print("\nSummary completed successfully.")