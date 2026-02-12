# Exercise Solution: The Great Merger

## Title & Problem Statement
**The Great Merger: Combining Multiple Excel Files**

**Context:** You have received three separate Excel files representing sales for Quarter 1, Quarter 2, and Quarter 3. Your task is to combine them into a single dataset for analysis. This is the classic "Excel Killer" use case—replacing manual copy-pasting with a repeatable script.

## Difficulty & Estimated Time
**Beginner | 25-45 Minutes**

## Required Libraries
*   `pandas`: The industry standard for data manipulation in Python. used here to read Excel files and handle the data in DataFrame format.
*   `openpyxl`: A dependency required by pandas to read/write Excel (`.xlsx`) files.

## Didactic Step-by-Step

1.  **Importing the Library:** We start by importing `pandas`. It's the toolbox that gives us the "superpowers" to handle data.
2.  **Loading Data:** We use `pd.read_excel()` to pull data from the hard drive into memory (DataFrames). Think of a DataFrame as a programmable Excel worksheet living in your RAM.
3.  **Concatenation:** The core of this exercise is `pd.concat()`. This function takes a list of DataFrames and stacks them on top of each other, like stacking sheets of paper.
4.  **Verification:** We check `df.shape` (rows, columns) to ensure no data was lost during the merge. The sum of rows in the individual files should equal the rows in the combined file.
5.  **Export:** Finally, `to_csv()` saves our work back to the hard drive so it can be shared or opened in Excel.

## Tips for Coding & Vibe-Coding

1.  **Variable Names Matter:** Using names like `df_q1`, `df_q2` helps you keep track of what each variable holds. `df` is the standard shorthand for "DataFrame".
2.  **Check Your Work:** Always run `print(df.head())` or `print(df.shape)` after loading data. It's the "sanity check" that prevents hours of debugging later.
3.  **Relative Paths:** When working with files, ensure your script knows where to look. Keeping the data in a folder named `data` or `input` is a good habit.
4.  **Don't Fear Errors:** If `read_excel` fails, it's usually a missing library (`openpyxl`) or a typo in the filename. Read the error message at the bottom of the stack trace!
5.  **The "Index" Trap:** When saving to CSV, usually use `index=False`. Otherwise, pandas saves the row numbers (0, 1, 2...) as the first column, which usually isn't what your boss wants.

## Copilot Master Prompt

> "I have three Excel files named 'sales_q1.xlsx', 'sales_q2.xlsx', and 'sales_q3.xlsx' in a folder. I want to use Python and Pandas to load them all, combine them into one single dataframe, and save the result as 'combined_sales.csv'. Please explain the code step by step."
