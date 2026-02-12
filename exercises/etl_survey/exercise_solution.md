# Exercise Card: ETL 3 - The Messy Survey (The Human Factor)

## Title & Problem Statement
**The Human Factor: Cleaning Messy User-Generated Data**

In real-world business scenarios, manual data entry is the biggest source of dirty data. In this exercise, we simulate a raw export from an internal survey tool where validation was turned off. You need to normalize categories, parse chaotic date formats, and extract value from unstructured text fields. This is a critical skill for preparing data for downstream BI tools like Power BI or Tableau.

## Difficulty & Estimated Time
*   **Difficulty:** Intermediate (Data Cleaning Focus)
*   **Estimated Time:** 30-45 Minutes

## Required Libraries
*   `pandas`: The Swiss Army knife for data manipulation.
*   `re`: (Optional) Python's built-in Regex library, though we will use the pandas accessor `.str` which handles most of it.

## Didactic Step-by-Step

### 1. String Normalization
**Concept:** usage of `.str` accessor.
User input is unpredictable. "Male", "male", "  Male ", and "M" are considered four different categories by a computer.
*   **Action:** Convert everything to lowercase first (`.str.lower()`) and strip whitespace (`.str.strip()`). Then use a mapping dictionary or `.replace()` to unify them.

### 2. Date Parsing
**Concept:** `pd.to_datetime` resilience.
Dates like "2023-01-01" and "01/01/2023" break simple sorting.
*   **Action:** Use `pd.to_datetime(col, errors='coerce')`. The `coerce` argument turns unparseable garbage into `NaT` (Not a Time) instead of crashing your script.

### 3. Text Flagging
**Concept:** Boolean indexing with strings.
We want to categorize rows based on contents of a string.
*   **Action:** `df['col'].str.contains('keyword')` returns a Truth Series (True/False) which is perfect for creating binary flag columns.

### 4. Regex Extraction (Tier 2)
**Concept:** Pattern matching.
Finding an email isn't about finding a specific word, but a *structure* (text @ text . text).
*   **Action:** `df['col'].str.extract(r'pattern')` allows you to pull these matching patterns out into a new column.

## Tips for coding and vibe-coding

1.  **Chaining is Key:** In pandas, try to chain string methods: `df['col'].str.lower().str.strip()`.
2.  **Safety First:** When testing Regex or replacements, assign the result to a *new* column (e.g., `Gender_Clean`) first so you can compare it side-by-side with the original before overwriting.
3.  **Check your `dtypes`:** Always run `df.info()` after loading. If a date column says `object`, it's not a date yet.
4.  **Save Memory:** Converting low-cardinality string columns (like Gender, Region, Status) to `category` type can reduce memory usage by 90%.
5.  **Regex Helper:** If you are stuck on a regex pattern, ask Copilot or use sites like regex101.com. A simple email pattern is `r'(\b[\w.-]+?@\w+?\.\w+?\b)'`.

## Copilot Master Prompt
*You can use this prompt to generate the solution code*

> "I have a pandas dataframe with a 'Gender' column that has mixed values (M, Male, m, F, Female) and a 'Join_Date' column with mixed date formats. 
> 1. Normalize the Gender column to just 'Male', 'Female', 'Other'.
> 2. Convert Join_Date to datetime, coercing errors.
> 3. Create a 'Compensation_Issue' column that is True if the 'Comments' column contains 'salary' or 'money'.
> 4. Extract email addresses from 'Comments' into a new column using regex."

