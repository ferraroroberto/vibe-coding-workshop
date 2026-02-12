# Solution: The Big Data Stress Test

## Problem Statement
In the corporate world, data grows. A script that runs instantly on 500 rows might drag on 50,000 and crash on 5,000,000. When data exceeds your available RAM (Random Access Memory), standard libraries like Pandas often fail because they try to hold the entire dataset in memory.

We need a strategy called **Out-of-Core Processing**: processing data in chunks from the hard drive, only keeping what we need in memory (results/aggregations).

## Difficulty & Estimated Time
**Intermediate** | 30 Minutes

## Required Libraries
*   `duckdb`: An in-process SQL OLAP database. It acts like an "engine" that sits on your files and queries them super fast without loading everything.
*   `pandas`: Used here to demonstrate the limitation (and for smaller data tasks).

## Didactic Step-by-Step
1.  **The "Crash" (Conceptual):** We attempt to read extensive logs. In this exercise, we simulate the environment where `pd.read_csv()` would choke.
2.  **Lazy Loading:** Instead of `read`, we `connect`. DuckDB sees the files as a database table.
3.  **SQL Aggregation:** We write SQL queries. DuckDB optimizes the execution, reading only the necessary columns and rows from disk in a streamed fashion.
4.  **Parquet:** We convert CSV (text, heavy, slow) to Parquet (binary, compressed, column-oriented). This typically reduces file size by 60-80% and speeds up future reads by 10-50x.

## Tips for Coding and "Vibe-Coding"
1.  **Think SQL:** If you know SQL, you already know DuckDB. `SELECT * FROM 'myfile.csv'` is valid!
2.  **Columnar Speed:** DuckDB is a *column-oriented* database. It's incredibly fast at calculating averages/counts on a single column because it ignores the other columns.
3.  **Glob Patterns:** Use `*` wildcards. `data/*.csv` lets you treat 100 files as one table.
4.  **Parquet is King:** In Big Data, CSV is for humans, Parquet is for machines. Always convert if you read the data more than once.
5.  **Memory Limit:** You can explicitly tell DuckDB how much memory to use: `SET memory_limit='2GB'`.

## Copilot Master Prompt
> "I have a folder 'data/server_logs' containing multiple large CSV files. I need a Python script using DuckDB to:
> 1. Query all CSV files at once using a glob pattern.
> 2. Calculate the count of errors grouped by hour.
> 3. Save the combined data into a single 'optimized_logs.parquet' file.
> Explain why this is better than using Pandas for 10GB of data."

---
## Solution Code Breakdown
See `exercise_solution.py` for the implementation.
