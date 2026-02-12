# Exercise: ETL 3 - The Messy Survey (The Human Factor)

## The Goal
A clear, concise explanation of the problem we are solving and what the expected outcome is.

**Scenario:**
While you are finalizing the sales data, HR pings you. They have an "Employee Satisfaction Survey" (~1000 rows) and want to know if happy sales reps sell more. But their data is a disaster:
*   **Inconsistent Data:** Some people typed "Male", others "M", "m", or " F ".
*   **Mixed Dates:** Join dates are in every format imaginable (YYYY-MM-DD, DD/MM/YYYY, etc.).
*   **Unstructured Text:** The comments section is free-text, containing hidden gems like personal email addresses or keywords about complaints.

**Your Mission:**
Clean this dataset so it can eventually be accurately joined with your Sales data and used for analysis.

**Expected Outcome:**
A clean DataFrame (and CSV) with:
1.  Standardized `Gender` column (Male/Female/Other).
2.  Standardized `Join_Date` (Datetime objects).
3.  A new flag column `Compensation_Issue` (True/False) based on keywords.
4.  (Optional) A new column `extracted_email` pulled from the comments using Regex.
