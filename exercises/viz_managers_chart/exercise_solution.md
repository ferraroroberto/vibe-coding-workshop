# Solution: The Manager's Chart (Visualization)

## Problem Statement
Your data cleaning efforts paid off, and you now have a pristine `clean_sales_data.csv`. The Manager needs a visual for the upcoming board meeting. She specifically wants to see **"Total Revenue by Product Category"**. 

She has emphasized that she is picky about aesthetics: the chart must have a clear title, readable labels (not overlapping), and currency formatting on the axis so executives don't have to count zeros.

## Difficulty & Estimated Time
Beginner | 25 Minutes

## Required Libraries
*   **`pandas`**: To load the CSV and perform the aggregation (summing revenue by category).
*   **`seaborn`**: A high-level visualization library based on matplotlib that draws attractive statistical graphics.
*   **`matplotlib.pyplot`**: The underlying engine used to fine-tune the chart details (titles, axis labels, rotation).

## Didactic Step-by-Step
1.  **Data Loading**: Read the clean data into a DataFrame.
2.  **Aggregation**: Visualizations often need summarized data. Use `groupby('Category')['Revenue'].sum()` to condense thousands of rows into a few category totals.
3.  **Plotting**: Use `seaborn.barplot` to render the data. It handles colors and basic layout automatically.
4.  **Formatting**: This is where the specific requirements are met.
    *   **Title**: Set using `plt.title()`.
    *   **Rotation**: Use `plt.xticks(rotation=45)` so long category names don't overlap.
    *   **Currency**: Use `FuncFormatter` from matplotlib to turn raw numbers (e.g., 500000) into currency strings (e.g., $500,000).

## Tips for Coding & Vibe-Coding
1.  **Pre-Aggregate**: While some tools plot raw data, explicitly grouping your data (`groupby`) gives you full control over what is being shown (Sum vs Average vs Count).
2.  **Themes**: Use `plt.style.use('fivethirtyeight')` or `sns.set_theme()` to instantly make your charts look less "default" and more professional.
3.  **Data Types Matter**: If your 'Revenue' column is loaded as text (strings), the plot will fail or look wrong. Always check `df.info()` first.
4.  **No Overlap**: Rotating x-axis labels is the #1 fix for messy categorical charts.
5.  **Save It**: `plt.show()` is great for you, but `plt.savefig('chart.png')` is what you send to the boss.

## Copilot Master Prompt
> "I have a pandas DataFrame named `df` with columns 'Category' and 'Revenue'. Write a Python script using Seaborn to:
> 1. Group the data by 'Category' and sum the total 'Revenue'.
> 2. Create a bar chart of the results.
> 3. Add a title '2026 Sales Performance'.
> 4. Rotate the x-axis labels 45 degrees so they are readable.
> 5. Format the y-axis with dollar signs and commas (e.g., $1,000)."
