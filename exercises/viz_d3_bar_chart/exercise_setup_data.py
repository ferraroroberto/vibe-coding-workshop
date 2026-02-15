import pandas as pd
import random
import os
from datetime import datetime, timedelta

# --- DOCUMENTATION ---
"""
This script generates 12 months of product sales data designed for a
D3.js animated bar chart race. Products have varying growth trajectories
so that rankings shift meaningfully over time — some products start
strong and fade, others ramp up in later months.
"""

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
FILE_NAME = "monthly_product_sales.csv"

# --- PRODUCT DEFINITIONS ---
# Each product has a category and a "growth profile" controlling how
# its monthly revenue evolves over the year.
PRODUCTS = {
    # (category, base_revenue, monthly_growth_factor, volatility)
    "Laptop Pro":           ("Electronics",     80000, 1.03, 0.15),
    "Wireless Monitor":     ("Electronics",     45000, 1.05, 0.12),
    "Mechanical Keyboard":  ("Electronics",     20000, 1.08, 0.20),
    "Cloud Suite":          ("Software",        60000, 1.06, 0.10),
    "Security Platform":    ("Software",        35000, 1.04, 0.18),
    "Analytics Pro":        ("Software",        15000, 1.12, 0.25),
    "Ergonomic Chair":      ("Furniture",       50000, 1.02, 0.10),
    "Standing Desk":        ("Furniture",       30000, 1.07, 0.15),
    "Consulting Hour":      ("Services",        70000, 1.01, 0.20),
    "Training Workshop":    ("Services",        25000, 1.09, 0.22),
    "Support Package":      ("Services",        40000, 1.03, 0.12),
    "Premium Pen Set":      ("Office Supplies", 10000, 1.15, 0.30),
    "Smart Whiteboard":     ("Office Supplies", 18000, 1.10, 0.20),
    "CRM Module":           ("Software",        22000, 1.11, 0.18),
    "USB-C Dock":           ("Electronics",     12000, 1.14, 0.25),
}


def create_dataset():
    """Generate monthly product sales with varying growth curves."""
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Generating monthly product sales data...\n")

    records = []
    months = pd.date_range(start="2024-01-01", periods=12, freq="MS")

    for product_name, (category, base_rev, growth, volatility) in PRODUCTS.items():
        current_rev = base_rev

        for month_idx, month_date in enumerate(months):
            # Apply growth with random volatility
            noise = random.uniform(1 - volatility, 1 + volatility)
            monthly_revenue = round(current_rev * noise, 2)

            # Generate individual transactions that sum to the monthly revenue
            num_transactions = random.randint(15, 50)
            per_txn = monthly_revenue / num_transactions

            for t in range(num_transactions):
                # Distribute transactions across days within the month
                day_offset = random.randint(0, 27)
                txn_date = month_date + timedelta(days=day_offset)
                txn_revenue = round(per_txn * random.uniform(0.5, 1.5), 2)
                quantity = random.randint(1, 10)

                records.append({
                    "Date": txn_date.strftime("%Y-%m-%d"),
                    "Month": month_date.strftime("%Y-%m"),
                    "Product": product_name,
                    "Category": category,
                    "Quantity": quantity,
                    "Revenue": txn_revenue,
                })

            # Compound growth for next month
            current_rev *= growth

    df = pd.DataFrame(records)

    output_path = os.path.join(DATA_DIR, FILE_NAME)
    df.to_csv(output_path, index=False)

    print(f"SUCCESS: Created {output_path}")
    print(f"  Rows: {len(df)}")
    print(f"  Products: {df['Product'].nunique()}")
    print(f"  Categories: {df['Category'].nunique()}")
    print(f"  Months: {df['Month'].nunique()}")

    # Show monthly totals
    monthly = df.groupby("Month")["Revenue"].sum().reset_index()
    print(f"\nMonthly revenue totals:")
    for _, row in monthly.iterrows():
        print(f"  {row['Month']}: ${row['Revenue']:,.0f}")

    print(f"\nReady to build the bar chart race!")


if __name__ == "__main__":
    create_dataset()
