# --- CONFIGURATION ---
import os
import duckdb
import time

# Use the current file's folder as the root
script_dir = os.path.dirname(__file__)
DATA_DIR = os.path.join(script_dir, "data")
LOGS_DIR = os.path.join(DATA_DIR, "server_logs")
PARQUET_FILE = os.path.join(DATA_DIR, "logs_optimized.parquet")

# The Glob pattern to match ALL csv files in the logs directory
CSV_PATTERN = os.path.join(LOGS_DIR, "*.csv")

print(f"Targeting files: {CSV_PATTERN}")

# --- PART 1: THE DUCKDB WAY (Lazy Loading) ---

print("\n--- 1. Querying Data without Loading (DuckDB) ---")
start_time = time.time()

# We act like the CSVs are a table. We don't import them.
# Let's count errors by hour.
query = f"""
    SELECT 
        date_trunc('hour', CAST(timestamp AS TIMESTAMP)) as log_hour,
        count(*) as error_count
    FROM '{CSV_PATTERN}'
    WHERE level = 'ERROR'
    GROUP BY log_hour
    ORDER BY error_count DESC
    LIMIT 5
"""

# execute() runs the query. df() converts just the RESULT (5 rows) to pandas for nice printing.
result_df = duckdb.sql(query).df()

end_time = time.time()
print(f"Query completed in {end_time - start_time:.4f} seconds.")
print(result_df)


# --- PART 2: OPTIMIZATION (Convert to Parquet) ---

print("\n--- 2. Converting CSVs to Parquet ---")
print("Converting... (This performs a one-time read-write)")

start_time = time.time()

# DuckDB can convert massive CSVs to Parquet very efficiently
convert_query = f"""
    COPY (SELECT * FROM '{CSV_PATTERN}') 
    TO '{PARQUET_FILE}' 
    (FORMAT 'PARQUET', CODEC 'SNAPPY')
"""
duckdb.sql(convert_query)

end_time = time.time()
print(f"Conversion completed in {end_time - start_time:.4f} seconds.")

# Verify the file size difference
def get_dir_size(path):
    total = 0
    if os.path.isdir(path):
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
    return total

csv_size = get_dir_size(LOGS_DIR) / (1024 * 1024)
parquet_size = os.path.getsize(PARQUET_FILE) / (1024 * 1024)

print(f"\nOriginal CSV Size: {csv_size:.2f} MB")
print(f"Parquet File Size: {parquet_size:.2f} MB")
print(f"Compression Ratio: {csv_size / parquet_size:.1f}x smaller")


# --- PART 3: QUERY THE PARQUET (Super Speed) ---

print("\n--- 3. Querying the Parquet File ---")
start_time = time.time()

# Same query, but targeting the single parquet file
parquet_query = f"""
    SELECT 
        date_trunc('hour', CAST(timestamp AS TIMESTAMP)) as log_hour,
        count(*) as error_count
    FROM '{PARQUET_FILE}'
    WHERE level = 'ERROR'
    GROUP BY log_hour
    ORDER BY error_count DESC
    LIMIT 5
"""

# Use .df() and print() for Windows console compatibility (avoids UnicodeEncodeError from .show())
print(duckdb.sql(parquet_query).df())

end_time = time.time()
print(f"Parquet Query completed in {end_time - start_time:.4f} seconds.")
