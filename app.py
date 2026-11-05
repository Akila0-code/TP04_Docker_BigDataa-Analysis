
import os
import pandas as pd

DATA_PATH = "/app/data/tp03_fire_monitoring_sample.csv"


def main():
    print("=" * 50)
    print("TP04 - Docker Big Data Environment")
    print("Fire Monitoring Data Analysis")
    print("=" * 50)

    if not os.path.exists(DATA_PATH):
        print(f"ERROR: Dataset not found: {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)

    print(f"\nDataset shape: {df.shape}")
    print("\nColumns:")
    print(list(df.columns))

    print("\nMissing values:")
    print(df.isnull().sum())

    if "fire_alarm" in df.columns:
        print("\nFire alarm distribution:")
        print(df["fire_alarm"].value_counts().sort_index())

    for column in ["temperature", "humidity", "smoke_level"]:
        if column in df.columns:
            print(f"\nMean {column}: {df[column].mean():.2f}")

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()
