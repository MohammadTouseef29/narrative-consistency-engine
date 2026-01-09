# STEP 5: Entry point for Track A system

import os
import pandas as pd

# Pathway import (stub on Windows is acceptable)
import pathway as pw


def main():
    print("=== KDSH Track A: System Start ===")

    # Project paths
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")

    print("Base directory:", base_dir)
    print("Data directory:", data_dir)

    # List data files
    print("\nFiles in data directory:")
    for f in os.listdir(data_dir):
        print(" -", f)

    # Load train and test CSVs
    train_path = os.path.join(data_dir, "train.csv")
    test_path = os.path.join(data_dir, "test.csv")

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    print("\nTrain CSV shape:", train_df.shape)
    print("Test CSV shape:", test_df.shape)

    print("\nTrain CSV columns:")
    print(train_df.columns.tolist())

    print("\nTest CSV columns:")
    print(test_df.columns.tolist())

    print("\n=== System Initialized Successfully ===")


if __name__ == "__main__":
    main()
