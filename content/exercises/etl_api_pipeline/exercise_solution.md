# Exercise Card: ETL 4 - The API Pipeline (From Web to Warehouse)

## Title & Problem Statement
**From Web to Warehouse: Building a JSON-to-Excel ETL Pipeline**

In the modern enterprise, data rarely arrives as neat CSV files. APIs return nested JSON, pagination tokens split data across multiple responses, and fields can be missing or inconsistent between records. This exercise teaches you to handle the *real* shape of business data: hierarchical, messy, and spread across multiple endpoints. You will simulate reading paginated API responses, flatten nested JSON, join datasets, and produce a polished deliverable.

## Difficulty & Estimated Time
*   **Difficulty:** Intermediate (API & JSON Focus)
*   **Estimated Time:** 30-45 Minutes

## Required Libraries
*   `pandas`: Core data manipulation — loading, joining, aggregating, exporting.
*   `json`: Python's built-in JSON parser for reading API response files.
*   `os` / `glob`: For discovering and iterating over multiple JSON files (simulating pagination).
*   `openpyxl`: Excel engine for writing multi-sheet `.xlsx` output.

## Didactic Step-by-Step

### 1. Loading Paginated JSON
**Concept:** Real APIs return data in pages. Each page is a separate JSON response.
*   **Action:** Use `glob` to find all `customers_page_*.json` and `orders_page_*.json` files. Load each with `json.load()` and collect records into a list.

### 2. Flattening Nested JSON
**Concept:** JSON objects can contain objects inside objects (e.g., `address.city`).
*   **Action:** Use `pd.json_normalize()` to automatically flatten nested dictionaries into columns with dot notation (e.g., `address.city` becomes a column).

### 3. Joining Datasets
**Concept:** Relational joins — combining two tables on a shared key.
*   **Action:** Use `pd.merge(orders_df, customers_df, on='customer_id')` to enrich each order row with customer details.

### 4. Cleaning & Type Conversion
**Concept:** APIs return everything as strings. Dates, numbers, and booleans need explicit conversion.
*   **Action:** Convert `order_date` with `pd.to_datetime()`, fill missing `phone` numbers with "N/A", and ensure `amount` is numeric.

### 5. Aggregation & Export
**Concept:** Summarizing data for management and writing multi-sheet Excel files.
*   **Action:** Group by `customer_id` to compute total spend, then use `pd.ExcelWriter` to write detail and summary sheets.

## Tips for Coding and Vibe-Coding

1.  **`pd.json_normalize()` is your best friend:** Don't try to manually loop through nested dicts. This function handles arbitrarily deep nesting and creates clean column names.
2.  **Accumulate, then convert:** When loading multiple JSON pages, append all records to a Python list first, *then* create the DataFrame once. This is much faster than `pd.concat` in a loop.
3.  **Always check `dtypes` after loading JSON:** Numbers might be strings, dates will definitely be strings. Run `df.info()` immediately.
4.  **Left Join vs Inner Join:** Use `how='left'` in your merge if you want to keep all orders even if a customer record is missing. Use `how='inner'` for a strict match.
5.  **Parameterize your paths:** Keep all file paths in a `# --- CONFIGURATION ---` block at the top so the script works on any machine.

## Copilot Master Prompt
*You can use this prompt to generate the solution code:*

> "I have multiple JSON files simulating paginated API responses:
> - `customers_page_*.json` — each contains a list of customer objects with nested 'address' fields (street, city, state, zip).
> - `orders_page_*.json` — each contains a list of order objects with customer_id, order_date, product, quantity, and amount.
>
> Write a Python ETL script that:
> 1. Loads all JSON pages using glob and json.load.
> 2. Flattens the nested customer address using pd.json_normalize.
> 3. Merges orders with customers on customer_id.
> 4. Converts order_date to datetime, fills missing phone numbers with 'N/A'.
> 5. Creates a summary DataFrame of total spend per customer.
> 6. Exports to an Excel file with two sheets: 'Orders Detail' and 'Customer Summary'."
