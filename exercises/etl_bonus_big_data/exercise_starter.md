# Exercise: The Big Data Stress Test

## The Goal
Fast forward two years. Your company has grown, and the "Sales Data" is no longer just 3 simple files—it's gigabytes of server logs.

Your mission is to process these simulated large datasets without crashing your computer. You will move from memory-heavy tools (like Pandas) to an "Out-of-Core" processing engine that handles data larger than your RAM.

## The Problem
*   **System Crashes:** Traditional scripts try to load everything into RAM at once.
*   **Slow Performance:** CSV files are slow to read and process.
*   **Storage Costs:** Text-based logs take up too much space.

## The Expected Outcome
1.  Experience why the "old way" fails.
2.  Use a new tool (**DuckDB**) to query data *without* loading it all first.
3.  Convert bulky CSVs into the efficient **Parquet** format.
