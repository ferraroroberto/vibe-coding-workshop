# Exercise Solution: ETL 2 - The Detective

**Title:** Data Cleaning & Logic with Pandas
**Difficulty:** Beginner-Intermediate | 30 Minutes
**Scenario:** Cleaning a sales dataset that contains duplicates and erroneous values before reporting.

---

### Required Libraries
*   `pandas`: The standard tool for tabular data manipulation.
*   `os`: To handle file paths regardless of the operating system.

### Didactic Step-by-Step

1.  **Loading Data:** We read the CSV file into a DataFrame.
2.  **Identifying Duplicates:**
    *   `df.duplicated()` returns a boolean Series (True/False) for each row.
    *   We use `subset=['Order_ID']` because the same order shouldn't exist twice, even if other columns changed slightly.
    *   `df.drop_duplicates()` actually removes them.
3.  **Filtering Logic (Boolean Indexing):**
    *   We create a condition: `df['Revenue'] > 0`.
    *   We apply this mask to the DataFrame to keep only valid rows.
4.  **Verification:** Always print the `shape` (rows, columns) of the data before and after cleaning to know how much data was removed.
5.  **Exporting:** Save the result using `to_csv(index=False)` so we don't save the pandas row numbers.

### Tips for Coding
1.  **Check your Shape:** `print(df.shape)` is your best friend. exact counts matter.
2.  **In-Place vs Reassignment:** Most pandas operations return a *new* copy. You must assign it back: `df = df.drop_duplicates(...)`.
3.  **Chaining:** You can chain commands like `df.drop_duplicates().reset_index()`, but be careful with readability.
4.  **Describe is Magic:** Use `df.describe()` to instantly spot negative numbers (min) or crazy high numbers (max).
5.  **Keep Argument:** When dropping duplicates, `keep='first'` (default) keeps the first occurrence. `keep='last'` is useful if the dataset is time-ordered and the last one is the correction.

### Copilot Master Prompt
> "I have a pandas DataFrame named 'df' with columns 'Order_ID' and 'Revenue'.
> 1. Remove rows where 'Order_ID' is a duplicate.
> 2. Remove rows where 'Revenue' is less than or equal to 0.
> 3. Calculate statistics to identify outliers in 'Revenue' defined as values > 3 standard deviations from the mean.
> Provide well-commented Python code."

---

### Tier 2 Solution (The "Fast Track" Logic)
For the outlier detection, we calculate the Z-score logic manually or just use the formula:
`limit = mean + (3 * std)`
`suspicious_rows = df[df['Revenue'] > limit]`

This is a very common "sanity check" in financial reporting.
