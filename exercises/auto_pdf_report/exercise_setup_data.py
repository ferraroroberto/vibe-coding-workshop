import pandas as pd
import random
import os
from datetime import datetime, timedelta

# --- DOCUMENTATION ---
"""
This script generates a sales dataset for the PDF Report Generator exercise.
It creates a realistic quarterly sales CSV with categories, products,
regions, and sales reps suitable for aggregation and charting.
"""

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
FILE_NAME = "quarterly_sales.csv"
NUM_ROWS = 500

# --- REFERENCE DATA ---
CATEGORIES = {
    "Electronics": {
        "products": ["Laptop Pro X1", "Wireless Monitor 27", "Mechanical Keyboard", "Noise-Cancel Headphones", "Docking Station"],
        "price_range": (200, 2500),
    },
    "Software": {
        "products": ["Cloud Suite Annual", "Security Platform", "Analytics Dashboard", "Project Manager Pro", "CRM Enterprise"],
        "price_range": (100, 1200),
    },
    "Office Supplies": {
        "products": ["Premium Pen Set", "Executive Notebook", "Desk Organizer Kit", "Label Maker", "Paper Shredder"],
        "price_range": (15, 150),
    },
    "Furniture": {
        "products": ["Ergonomic Chair", "Standing Desk", "Monitor Arm", "Filing Cabinet", "Acoustic Panel Set"],
        "price_range": (100, 2000),
    },
    "Services": {
        "products": ["IT Consulting (8h)", "Training Workshop", "System Migration", "Security Audit", "Data Recovery"],
        "price_range": (500, 5000),
    },
}

REGIONS = ["North", "South", "East", "West"]

SALES_REPS = [
    "Alice Chen", "Bob Martinez", "Carla Fischer", "David Okafor",
    "Elena Volkov", "Finn Johansson", "Grace Tanaka", "Hassan Ali",
]

PAYMENT_METHODS = ["Credit Card", "Wire Transfer", "Purchase Order", "PayPal"]


def create_dataset():
    """Generate the quarterly sales dataset."""
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Generating {NUM_ROWS} rows of quarterly sales data...\n")

    records = []
    # Q4 2026 (Oct - Dec)
    start_date = datetime(2026, 10, 1)
    end_date = datetime(2026, 12, 31)
    total_days = (end_date - start_date).days

    for i in range(1, NUM_ROWS + 1):
        category = random.choice(list(CATEGORIES.keys()))
        cat_info = CATEGORIES[category]
        product = random.choice(cat_info["products"])

        min_price, max_price = cat_info["price_range"]
        unit_price = round(random.uniform(min_price, max_price), 2)
        quantity = random.randint(1, 12)
        revenue = round(unit_price * quantity, 2)

        order_date = start_date + timedelta(days=random.randint(0, total_days))

        records.append({
            "Order_ID": f"Q4-{50000 + i}",
            "Date": order_date.strftime("%Y-%m-%d"),
            "Region": random.choice(REGIONS),
            "Sales_Rep": random.choice(SALES_REPS),
            "Category": category,
            "Product": product,
            "Quantity": quantity,
            "Unit_Price": unit_price,
            "Revenue": revenue,
            "Payment_Method": random.choice(PAYMENT_METHODS),
        })

    df = pd.DataFrame(records)

    # Save
    output_path = os.path.join(DATA_DIR, FILE_NAME)
    df.to_csv(output_path, index=False)

    print(f"SUCCESS: Created {output_path}")
    print(f"  Rows: {len(df)}")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"\nRevenue by Category:")
    cat_rev = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
    for cat, rev in cat_rev.items():
        print(f"  {cat}: ${rev:,.2f}")
    print(f"\n  Total Revenue: ${df['Revenue'].sum():,.2f}")
    print(f"\nYou are ready to generate your PDF report!")


if __name__ == "__main__":
    create_dataset()
