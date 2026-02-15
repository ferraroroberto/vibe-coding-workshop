import pandas as pd
import numpy as np
import random
import os

# --- DOCUMENTATION ---
"""
This script generates a rich product-level sales dataset designed for
advanced Seaborn scatter plots. Each row is a single transaction with
numeric fields (Unit_Price, Revenue, Quantity) and categorical fields
(Category, Region, Product) that map naturally to scatter aesthetics
(x, y, hue, size, style, facet).
"""

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
FILE_NAME = "product_transactions.csv"
NUM_ROWS = 1200

# --- REFERENCE DATA ---
REGIONS = ["North America", "Europe", "Asia Pacific", "Latin America"]

CATEGORIES = {
    "Electronics": {
        "products": ["Laptop Pro", "Wireless Monitor", "Mechanical Keyboard", "Noise-Cancel Headphones", "USB-C Dock"],
        "price_range": (150, 2500),
        "satisfaction_mean": 7.5,
    },
    "Software": {
        "products": ["Cloud Suite", "Security Platform", "Analytics Pro", "DevOps Kit", "CRM Module"],
        "price_range": (30, 800),
        "satisfaction_mean": 7.0,
    },
    "Office Supplies": {
        "products": ["Premium Pen Set", "Executive Binder", "Smart Whiteboard", "Desk Organizer", "Paper Ream"],
        "price_range": (5, 120),
        "satisfaction_mean": 6.0,
    },
    "Furniture": {
        "products": ["Ergonomic Chair", "Standing Desk", "Monitor Arm", "Filing Cabinet", "LED Desk Lamp"],
        "price_range": (80, 1800),
        "satisfaction_mean": 8.0,
    },
    "Services": {
        "products": ["Consulting Hour", "Training Workshop", "Support Plan", "Migration Service", "Audit Session"],
        "price_range": (200, 3000),
        "satisfaction_mean": 7.2,
    },
}


def create_dataset():
    """Generate a transaction-level dataset for scatter visualization."""
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Generating {NUM_ROWS} transactions for scatter plots...\n")

    records = []

    for i in range(1, NUM_ROWS + 1):
        region = random.choice(REGIONS)
        category = random.choice(list(CATEGORIES.keys()))
        cat_info = CATEGORIES[category]

        product = random.choice(cat_info["products"])
        min_p, max_p = cat_info["price_range"]
        unit_price = round(random.uniform(min_p, max_p), 2)

        # Quantity has a realistic relationship with price (cheaper = buy more)
        base_qty = max(1, int(15 - (unit_price / max_p) * 12))
        quantity = max(1, base_qty + random.randint(-2, 5))

        # Revenue = price * quantity + small noise
        revenue = round(unit_price * quantity * random.uniform(0.95, 1.05), 2)

        # Satisfaction score: correlated with category, some noise
        satisfaction = round(
            np.clip(
                np.random.normal(cat_info["satisfaction_mean"], 1.2),
                1.0, 10.0
            ), 1
        )

        # Discount percentage: random, higher for bigger deals
        discount = round(random.uniform(0, 0.15) if revenue > 1000 else random.uniform(0, 0.05), 3)

        records.append({
            "Transaction_ID": f"TXN-{60000 + i}",
            "Region": region,
            "Category": category,
            "Product": product,
            "Unit_Price": unit_price,
            "Quantity": quantity,
            "Revenue": revenue,
            "Discount": discount,
            "Satisfaction_Score": satisfaction,
        })

    df = pd.DataFrame(records)

    output_path = os.path.join(DATA_DIR, FILE_NAME)
    df.to_csv(output_path, index=False)

    print(f"SUCCESS: Created {output_path}")
    print(f"  Rows: {len(df)}")
    print(f"  Columns: {list(df.columns)}")
    print(f"\nSample data:")
    print(df.head(5).to_string(index=False))
    print(f"\nCategory distribution:")
    print(df["Category"].value_counts().to_string())
    print(f"\nPrice range: ${df['Unit_Price'].min():.2f} - ${df['Unit_Price'].max():.2f}")
    print(f"Revenue range: ${df['Revenue'].min():.2f} - ${df['Revenue'].max():.2f}")
    print(f"\nReady for scatter plot visualization!")


if __name__ == "__main__":
    create_dataset()
