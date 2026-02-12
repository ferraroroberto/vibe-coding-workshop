# Exercise Card: The Report Generator

## Title & Problem Statement
**Context:** After presenting your charts, your manager asks for the underlying data. Sending multiple CSV files is messy and unprofessional.
**The Problem:** You need to bundle a summary view and the granular data into one cohesive file (`.xlsx`) to simplify distribution.
**The Fix:** Use `pd.ExcelWriter` to write multiple dataframes to specific sheets within the same workbook.

## Difficulty & Estimated Time
*   **Difficulty:** Beginner - Intermediate
*   **Time:** 25-30 Minutes

## Required Libraries
*   `pandas`: For data manipulation and Excel export.
*   `openpyxl`: The engine Pandas uses to create `.xlsx` files.

## Didactic Step-by-Step
1.  **Load Data:** Ingest the `clean_sales_data.csv`.
2.  **Aggregate:** Create the "Summary" dataframe by grouping data (e.g., `df.groupby('Category')['Revenue'].sum()`).
3.  **Initialize Writer:** Create a `pd.ExcelWriter` object context. This acts as the "file handle" for the Excel workbook.
4.  **Write Sheets:** 
    *   Use `summary_df.to_excel(writer, sheet_name='Executive Summary')`.
    *   Use `clean_df.to_excel(writer, sheet_name='Backing Data')`.
5.  **Save:** The context manager (`with ... as writer:`) automatically saves and closes the file.

## Tips for coding and vibe-coding
1.  **Context Managers:** Always use `with pd.ExcelWriter(...) as writer:` to ensure the file saves properly even if errors occur.
2.  **Sheet Names:** Excel sheet names are limited to 31 characters. Keep them short!
3.  **Index Handling:** Decide if you want the index (like row numbers) in your Excel file. Often `index=False` looks cleaner for the raw data tab.
4.  **Formatting:** You can perform basic number formatting during export using the `float_format="%.2f"` argument.
5.  **Validation:** Always open the generated Excel file to manually verify the tabs exist and look correct.

## Copilot Master Prompt
> "I have a pandas dataframe named `df`. I want to create a summary dataframe that groups by 'Category' and sums 'Revenue'. Then, I want to save BOTH the summary dataframe and the original dataframe into a single Excel file named 'final_report.xlsx'. Put the summary on a sheet named 'Executive Summary' and the original data on a sheet named 'Backing Data'. Use the 'openpyxl' engine."
