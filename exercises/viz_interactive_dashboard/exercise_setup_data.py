import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

# --- DOCUMENTATION ---
"""
This script generates a rich sales dataset for the Interactive Dashboard exercise.
It includes regional data, multiple product categories, and a full year of dates
to enable compelling time-series, sunburst, and ranking visualizations.
"""

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
FILE_NAME = "sales_data_full.csv"
NUM_ROWS = 2000

# --- REFERENCE DATA ---
REGIONS = ["North America", "Europe", "Asia Pacific", "Latin America"]

CATEGORIES = {
    "Electronics": {
        "products": ["Laptop Pro", "Wireless Monitor", "Mechanical Keyboard", "Noise-Cancel Headphones", "USB-C Hub"],
        "price_range": (150, 2500),
    },
    "Software": {
        "products": ["Cloud Suite License", "Security Platform", "Analytics Pro", "DevOps Toolkit", "CRM Module"],
        "price_range": (50, 800),
    },
    "Office Supplies": {
        "products": ["Premium Pen Set", "Executive Binder", "Smart Whiteboard", "Ergonomic Stapler", "Recycled Paper Box"],
        "price_range": (10, 120),
    },
    "Furniture": {
        "products": ["Standing Desk", "Ergonomic Chair", "Monitor Arm", "Filing Cabinet", "LED Desk Lamp"],
        "price_range": (80, 1800),
    },
    "Services": {
        "products": ["IT Consulting Hour", "Training Workshop", "Support Package", "Migration Service", "Audit Session"],
        "price_range": (200, 3000),
    },
}

# Regional weights (some regions sell more of certain categories)
REGION_CATEGORY_WEIGHTS = {
    "North America": {"Electronics": 0.3, "Software": 0.3, "Office Supplies": 0.15, "Furniture": 0.15, "Services": 0.1},
    "Europe": {"Electronics": 0.25, "Software": 0.2, "Office Supplies": 0.2, "Furniture": 0.2, "Services": 0.15},
    "Asia Pacific": {"Electronics": 0.35, "Software": 0.25, "Office Supplies": 0.1, "Furniture": 0.15, "Services": 0.15},
    "Latin America": {"Electronics": 0.2, "Software": 0.15, "Office Supplies": 0.25, "Furniture": 0.25, "Services": 0.15},
}


def create_dataset():
    """Generate a comprehensive sales dataset."""
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Generating {NUM_ROWS} rows of sales data...\n")

    records = []
    start_date = datetime(2024, 1, 1)

    for i in range(1, NUM_ROWS + 1):
        # Pick region
        region = random.choice(REGIONS)

        # Pick category weighted by region
        weights = REGION_CATEGORY_WEIGHTS[region]
        category = random.choices(
            list(weights.keys()),
            weights=list(weights.values()),
            k=1
        )[0]

        # Pick product from that category
        cat_info = CATEGORIES[category]
        product = random.choice(cat_info["products"])

        # Generate price and quantity
        min_price, max_price = cat_info["price_range"]
        unit_price = round(random.uniform(min_price, max_price), 2)
        quantity = random.randint(1, 15)
        revenue = round(unit_price * quantity, 2)

        # Generate date with some seasonal variation (more sales in Q4)
        day_offset = random.randint(0, 364)
        # Boost Q4 probability
        if random.random() < 0.15:
            day_offset = random.randint(274, 364)  # Oct-Dec

        order_date = start_date + timedelta(days=day_offset)

        # Sales rep
        reps = ["Alice Chen", "Bob Martinez", "Carla Fischer", "David Okafor",
                "Elena Volkov", "Finn Johansson", "Grace Tanaka", "Hassan Ali"]
        sales_rep = random.choice(reps)

        records.append({
            "Order_ID": f"ORD-{30000 + i}",
            "Date": order_date.strftime("%Y-%m-%d"),
            "Region": region,
            "Category": category,
            "Product": product,
            "Sales_Rep": sales_rep,
            "Quantity": quantity,
            "Unit_Price": unit_price,
            "Revenue": revenue,
        })

    df = pd.DataFrame(records)

    # Save
    output_path = os.path.join(DATA_DIR, FILE_NAME)
    df.to_csv(output_path, index=False)

    print(f"SUCCESS: Created {output_path}")
    print(f"  Rows: {len(df)}")
    print(f"  Columns: {list(df.columns)}")
    print(f"\nData preview:")
    print(df.head(5).to_string(index=False))
    print(f"\nRevenue by Region:")
    print(df.groupby("Region")["Revenue"].sum().sort_values(ascending=False).to_string())
    print(f"\nYou are ready to build your dashboard!")


if __name__ == "__main__":
    create_dataset()
