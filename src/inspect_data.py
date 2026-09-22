from pathlib import Path
import pandas as pd

# Dataset folder
DATA_DIR = Path("data/raw/MachineLearningCVE")

# Find all CSV files
csv_files = list(DATA_DIR.glob("*.csv"))

print("=" * 60)
print("CYBERDEMANDIQ - DATASET INSPECTION")
print("=" * 60)

print(f"\nNumber of CSV files found: {len(csv_files)}")

for file in csv_files:
    print(f" - {file.name}")

# Inspect first CSV
if csv_files:
    first_file = csv_files[0]

    print("\n" + "=" * 60)
    print(f"INSPECTING: {first_file.name}")
    print("=" * 60)

    df = pd.read_csv(first_file, low_memory=False)

    print(f"\nRows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumn names:")
    for column in df.columns:
        print(f" - {column}")

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nLabel distribution:")
    if " Label" in df.columns:
        print(df[" Label"].value_counts())
    elif "Label" in df.columns:
        print(df["Label"].value_counts())
    else:
        print("Label column not found.")

else:
    print("\nNo CSV files found!")