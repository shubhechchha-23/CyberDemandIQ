from pathlib import Path
import pandas as pd

PROCESSED_DIR = Path("data/processed")

csv_files = sorted(PROCESSED_DIR.glob("cleaned_*.csv"))

print("=" * 70)
print("CYBERDEMANDIQ - CLEANED DATA INSPECTION")
print("=" * 70)

print(f"\nCleaned CSV files found: {len(csv_files)}")

for file in csv_files:
    print(f" - {file.name}")

if csv_files:

    file = csv_files[0]

    print("\n" + "=" * 70)
    print(f"INSPECTING: {file.name}")
    print("=" * 70)

    df = pd.read_csv(file, low_memory=False)

    print(f"\nRows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nCOLUMN NAMES:")
    print("-" * 70)

    for i, column in enumerate(df.columns, start=1):
        print(f"{i:02d}. {column}")

    print("\nDATA TYPES:")
    print("-" * 70)

    print(df.dtypes)

    print("\nMISSING VALUES:")
    print("-" * 70)

    missing = df.isnull().sum()
    print(missing[missing > 0])

    print("\nLABEL DISTRIBUTION:")
    print("-" * 70)

    if "label" in df.columns:
        print(df["label"].value_counts())

else:
    print("\nNo cleaned CSV files found!")