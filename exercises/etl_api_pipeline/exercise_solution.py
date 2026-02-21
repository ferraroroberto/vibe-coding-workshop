import pandas as pd
import json
import glob
import os

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
OUTPUT_CSV = os.path.join(DATA_DIR, "solutions", "customer_orders_consolidated.csv")
OUTPUT_EXCEL = os.path.join(DATA_DIR, "solutions", "pipeline_report.xlsx")


def load_json_pages(pattern):
    """Load all JSON pages matching a glob pattern and return a flat list of records."""
    all_records = []
    files = sorted(glob.glob(os.path.join(DATA_DIR, pattern)))

    if not files:
        print(f"WARNING: No files found matching '{pattern}' in {DATA_DIR}")
        return all_records

    for filepath in files:
        with open(filepath, "r") as f:
            response = json.load(f)

        # Extract the 'results' array from the API response envelope
        records = response.get("results", [])
        all_records.extend(records)
        print(f"  Loaded {len(records)} records from {os.path.basename(filepath)}")

    return all_records



# Ensure solutions directory exists
os.makedirs(os.path.join(DATA_DIR, 'solutions'), exist_ok=True)

def main():
    print("=" * 50)
    print("ETL PIPELINE: API JSON -> Consolidated Report")
    print("=" * 50)

    # -------------------------------------------------------
    # STEP 1: Load all paginated JSON files
    # -------------------------------------------------------
    print("\n[Step 1] Loading customer pages...")
    customer_records = load_json_pages("customers_page_*.json")

    print("\n[Step 1] Loading order pages...")
    order_records = load_json_pages("orders_page_*.json")

    if not customer_records or not order_records:
        print("\nError: Data files not found. Please run 'exercise_setup_data.py' first.")
        return

    # -------------------------------------------------------
    # STEP 2: Flatten nested JSON into DataFrames
    # -------------------------------------------------------
    print("\n[Step 2] Flattening and normalizing data...")

    # Customers have a nested 'address' object — json_normalize handles this
    customers_df = pd.json_normalize(customer_records)
    print(f"  Customers DataFrame: {customers_df.shape[0]} rows, {customers_df.shape[1]} columns")
    print(f"  Columns: {list(customers_df.columns)}")

    # Orders are flat — but we still use json_normalize for consistency
    orders_df = pd.json_normalize(order_records)
    print(f"  Orders DataFrame: {orders_df.shape[0]} rows, {orders_df.shape[1]} columns")

    # -------------------------------------------------------
    # STEP 3: Clean & type-convert
    # -------------------------------------------------------
    print("\n[Step 3] Cleaning data types...")

    # Convert order_date to datetime
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"], errors="coerce")

    # Fill missing phone numbers (some customers don't have one)
    if "phone" in customers_df.columns:
        customers_df["phone"] = customers_df["phone"].fillna("N/A")
    else:
        customers_df["phone"] = "N/A"

    # Ensure amount is numeric
    orders_df["amount"] = pd.to_numeric(orders_df["amount"], errors="coerce")

    print("  - order_date converted to datetime")
    print("  - Missing phone numbers filled with 'N/A'")
    print("  - amount ensured numeric")

    # -------------------------------------------------------
    # STEP 4: Join orders with customer details
    # -------------------------------------------------------
    print("\n[Step 4] Joining orders with customers...")

    merged_df = pd.merge(
        orders_df,
        customers_df,
        on="customer_id",
        how="left"  # Keep all orders, even if customer record is missing
    )

    print(f"  Merged DataFrame: {merged_df.shape[0]} rows, {merged_df.shape[1]} columns")

    # -------------------------------------------------------
    # STEP 5: Create summary
    # -------------------------------------------------------
    print("\n[Step 5] Creating customer summary...")

    summary_df = (
        merged_df.groupby(["customer_id", "name", "company", "tier"])
        .agg(
            total_orders=("order_id", "count"),
            total_spend=("amount", "sum"),
            avg_order_value=("amount", "mean"),
            first_order=("order_date", "min"),
            last_order=("order_date", "max"),
        )
        .reset_index()
        .sort_values(by="total_spend", ascending=False)
    )

    # Round monetary columns
    summary_df["total_spend"] = summary_df["total_spend"].round(2)
    summary_df["avg_order_value"] = summary_df["avg_order_value"].round(2)

    print(f"  Summary: {summary_df.shape[0]} unique customers")
    print("\n  Top 5 Customers by Spend:")
    print(summary_df[["name", "company", "total_spend"]].head().to_string(index=False))

    # -------------------------------------------------------
    # STEP 6: Export
    # -------------------------------------------------------
    print("\n[Step 6] Exporting results...")

    # CSV — full detail
    merged_df.to_csv(OUTPUT_CSV, index=False)
    print(f"  CSV saved: {OUTPUT_CSV}")

    # Excel — multi-sheet report
    with pd.ExcelWriter(OUTPUT_EXCEL, engine="openpyxl") as writer:
        merged_df.to_excel(writer, sheet_name="Orders Detail", index=False)
        summary_df.to_excel(writer, sheet_name="Customer Summary", index=False)

    print(f"  Excel saved: {OUTPUT_EXCEL}")

    print("\n" + "=" * 50)
    print("PIPELINE COMPLETE!")
    print(f"  Total orders processed: {len(merged_df)}")
    print(f"  Unique customers: {len(summary_df)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
