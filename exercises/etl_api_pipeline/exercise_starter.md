## English

# Bonus: ETL API Pipeline (From Web to Warehouse)

## The Scenario
Your company has adopted a new CRM system that exposes customer and order data via a REST API (JSON format). Management wants a single, flat Excel report combining customer profiles with their order history — but the API returns deeply nested JSON with inconsistent fields.

## Your Mission
Build a Python ETL pipeline that: **reads** paginated JSON (simulating API responses), **flattens** nested structures into clean DataFrames, **joins** customer data with orders, **handles** missing values and type inconsistencies, and **exports** the consolidated dataset to CSV and Excel.

## Expected Outcome
A clean `customer_orders_consolidated.csv` with one row per order enriched with customer details, plus a `pipeline_report.xlsx` with "Orders Detail" and "Customer Summary" sheets.

---

## Español

# Bonus: ETL API Pipeline (From Web to Warehouse)

## The Scenario
Your company has adopted a new CRM system that exposes customer and order data via a REST API (JSON format). Management wants a single, flat Excel report combining customer profiles with their order history — but the API returns deeply nested JSON with inconsistent fields.

## Your Mission
Build a Python ETL pipeline that: **reads** paginated JSON (simulating API responses), **flattens** nested structures into clean DataFrames, **joins** customer data with orders, **handles** missing values and type inconsistencies, and **exports** the consolidated dataset to CSV and Excel.

## Expected Outcome
A clean `customer_orders_consolidated.csv` with one row per order enriched with customer details, plus a `pipeline_report.xlsx` with "Orders Detail" and "Customer Summary" sheets.
