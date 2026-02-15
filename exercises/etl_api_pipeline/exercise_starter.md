# Exercise: ETL 4 - The API Pipeline (From Web to Warehouse)

## The Goal

Your company has adopted a new CRM system that exposes customer and order data via a REST API (JSON format). Management wants a single, flat Excel report combining customer profiles with their order history — but the API returns deeply nested JSON with inconsistent fields.

**Your Mission:**
Build a Python ETL pipeline that:
1. Reads paginated JSON data files (simulating API responses).
2. Flattens and normalizes the nested structures into clean tabular DataFrames.
3. Joins customer data with their orders.
4. Handles missing values and data type inconsistencies.
5. Exports the final consolidated dataset to both CSV and Excel.

**Expected Outcome:**
- A clean `customer_orders_consolidated.csv` with one row per order, enriched with customer details.
- A summary `pipeline_report.xlsx` with two sheets: "Orders Detail" and "Customer Summary" (total spend per customer).
