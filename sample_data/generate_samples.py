"""
Generate sample Excel files for testing and demonstration.

Run this script to populate sample_data/ with realistic test files:
    python sample_data/generate_samples.py

Creates 5 Excel files simulating monthly sales reports from different regions,
with intentional duplicates and empty rows to demonstrate cleaning capabilities.
"""

import os
import sys

import pandas as pd
import numpy as np

# Ensure we can import from the project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Realistic sample data
PRODUCTS = ["Widget A", "Widget B", "Gadget Pro", "Gadget Lite", "Service Pack"]
REGIONS = ["North", "South", "East", "West", "Central"]
SALES_REPS = ["Alice Johnson", "Bob Smith", "Carol Davis", "Dan Wilson", "Eva Martinez"]


def generate_sales_file(filename: str, num_rows: int, region: str, seed: int):
    """Generate a single sales report Excel file."""
    rng = np.random.default_rng(seed)

    data = {
        "Date": pd.date_range("2024-01-01", periods=num_rows, freq="D").strftime("%Y-%m-%d").tolist(),
        "Region": [region] * num_rows,
        "Sales_Rep": rng.choice(SALES_REPS, size=num_rows).tolist(),
        "Product": rng.choice(PRODUCTS, size=num_rows).tolist(),
        "Quantity": rng.integers(1, 50, size=num_rows).tolist(),
        "Unit_Price": (rng.random(size=num_rows) * 100 + 10).round(2).tolist(),
        "Total": [0.0] * num_rows,  # Will calculate below
    }

    df = pd.DataFrame(data)
    df["Total"] = (df["Quantity"] * df["Unit_Price"]).round(2)

    # Add some intentional duplicates (rows 2 and 3 repeated)
    if num_rows > 5:
        duplicate_rows = df.iloc[1:3].copy()
        df = pd.concat([df, duplicate_rows], ignore_index=True)

    # Add some empty rows to demonstrate cleaning
    empty_row = pd.DataFrame([{col: None for col in df.columns}])
    df = pd.concat([df, empty_row, empty_row], ignore_index=True)

    filepath = os.path.join(OUTPUT_DIR, filename)
    df.to_excel(filepath, index=False, engine="openpyxl")
    print(f"  Created: {filename} ({len(df)} rows)")


def main():
    """Generate all sample files."""
    print("Generating sample Excel files...\n")

    samples = [
        ("sales_north_jan.xlsx", 20, "North", 42),
        ("sales_south_jan.xlsx", 25, "South", 43),
        ("sales_east_jan.xlsx", 18, "East", 44),
        ("sales_west_jan.xlsx", 22, "West", 45),
        ("sales_central_jan.xlsx", 15, "Central", 46),
    ]

    for filename, rows, region, seed in samples:
        generate_sales_file(filename, rows, region, seed)

    print(f"\nDone. {len(samples)} files created in {OUTPUT_DIR}/")
    print("\nTo test the toolkit, copy these files to the input/ folder:")
    print(f"  cp {OUTPUT_DIR}/*.xlsx input/")


if __name__ == "__main__":
    main()
