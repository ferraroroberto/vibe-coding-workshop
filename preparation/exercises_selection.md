# **Workshop Plan: The "Day in the Life" of a Data Analyst**

## **Summary & Flow**

This workshop is designed as a continuous narrative. You play the role of a new Data Analyst whose responsibilities grow from "just checking the tools" to "automating the entire reporting pipeline."

| Section | Exercise | Scenario / Narrative | Tech Focus |
|:---|:---|:---|:---|
| **Intro** | **Hello World** | **Day 1:** Setting up your cockpit. Proving you can fly. | Environment, Simple Python |
| **ETL** | **1. The Great Merger** | **The First Request:** The boss sends you 3 separate quarterly sales files. You need to combine them into one Year-To-Date report. | `pd.read_excel`, `pd.concat` |
| **ETL** | **2. The Detective** | **The Sanity Check:** The combined data looks suspicious (duplicates, negative sales). You need to clean it before anyone notices. | Filtering, `duplicated()`, Logic |
| **ETL** | **3. The Messy Survey** | **The Ad-Hoc Request:** HR wants to correlate sales with employee satisfaction. They send you a messy CSV with mixed formats. | String cleaning, Regex |
| **Viz** | **4. The Manager's Chart** | **The Presentation:** The Sales data is clean. Now the manager wants a chart showing "Revenue by Category" for the slides. | `seaborn`, `groupby` |
| **Viz** | **5. The Report Generator** | **The Deliverable:** The boss wants the numbers *behind* the chart. You need an Excel file with a Summary tab and a Data tab. | `pd.ExcelWriter`, Multiple Sheets |
| **Auto** | **6. The Professional Polish** | **The Refinement:** The Excel file looks plain. You automate the formatting (bold headers, auto-fit columns) to impress the C-Suite. | `xlsxwriter`, Styles |
| **Auto** | **7. The File Organizer** | **The Cleanup:** The project is done, but your folder is full of random dumps. Organize your workspace automatically. | `os`, `shutil` |
| **Bonus** | **8. The Big Data Stress Test** | **The Future:** The company scales 100x. Your laptop can't handle the files anymore. | `duckdb`, Parquet, Performance |

---

## **Intro**

### **Intro: Hello World**

**Focus:** Environment familiarity, breaking the fear barrier, and the first "Win" with Copilot.

#### **One-Pager: Instructor & Student Guide**

**Scenario:** It's your first day. You have installed VS Code and Python, but it looks like a cockpit of a plane you don't know how to fly. You need to print "Hello World" and do your first calculation to prove to your boss (and yourself) that your setup is working.

**Dataset:** None (Pure Python).

**Tier 1: The Standard Path (Time: 20 mins)**

1. **The Environment:** Open VS Code. Create a file `hello.py`.
2. **The First Prompt:** Use GitHub Copilot (or ChatGPT window) to ask: *"How do I print 'Hello World' in Python?"* Run it.
3. **The Calculator:** Ask Copilot: *"Create a variable for revenue = 1000 and cost = 400. Calculate profit and print it."*
4. **The Loop:** Ask Copilot: *"Write a loop that prints numbers 1 to 5."* Watch it generate the code. Run it.

---

## **ETL**

### **ETL 1: The Great Merger**

**Focus:** `pd.concat`, file loading, and basic cleaning. The classic "Excel Killer."

#### **One-Pager: Instructor & Student Guide**

**Scenario:** Your setup works. Immediately, your boss emails you three separate Excel files for quarterly sales (Q1, Q2, Q3). She wants a single Year-To-Date report by lunch. Copy-pasting takes too long and risks errors. You decide to use Python.

**Dataset:** `sales_q1.xlsx`, `sales_q2.xlsx`, `sales_q3.xlsx` (Standard columns: `Date`, `Product`, `Revenue`).

**Tier 1: The Standard Path (Time: 25 mins)**

1. **Load:** Use Copilot: *"How do I load three excel files into pandas dataframes?"*
2. **Merge:** Ask Copilot: *"How do I stack these three dataframes on top of each other into one master dataframe?"* (Expect `pd.concat`).
3. **Check:** Run `df.shape` to verify the row count matches the sum of the three files.
4. **Export:** Save the result to `combined_sales.csv`.

**Tier 2: The Fast Track (Extra 20 mins)**

* **Task A (Source Tracking):** Before merging, add a column to each dataframe called `Quarter` (e.g., "Q1") so you can track where the row came from effectively.
* **Task B (The Glob Pattern):** Instead of loading files 1-by-1, ask Copilot to *"Load all Excel files in the folder and combine them automatically"* using a loop or `glob`. This scales to 100 files.

---

### **ETL 2: The Detective**

**Focus:** Logic, Filtering, and `duplicated()`.

#### **One-Pager: Instructor & Student Guide**

**Scenario:** You merged the files into `combined_sales.csv` in the previous step. Great job! But wait... looking closely, some Order IDs appear twice (glitch in the system?), and some Revenue numbers are negative (refunds? errors?). You can't report this yet. You need to clean the data.

**Dataset:** `combined_sales.csv` (Output from ETL 1).

**Tier 1: The Standard Path (Time: 25 mins)**

1. **Find Duplicates:** Ask Copilot: *"How do I find duplicate rows in my dataframe based on 'Order_ID'?"*
2. **Filter Logic:** Ask Copilot: *"Show me all rows where Revenue is less than 0."*
3. **The Fix:** Create a `clean_df` that drops duplicates and filters out negative values.
4. **Summary:** Print the number of rows removed (Original Count - Clean Count).
5. **Save:** Export to `clean_sales_data.csv`.

**Tier 2: The Fast Track (Extra 20 mins)**

* **Task A (Complex Logic):** Find rows that are "Suspiciously High." Calculate the Mean and Standard Deviation of Revenue. Filter for rows that are > 3 Standard Deviations from the mean (Outliers).
* **Task B (The "Why"):** Instead of just dropping duplicates, keep the *last* occurrence (assuming it's the most recent update) using `keep='last'`.

---

### **ETL 3: The Messy Survey (The Human Factor)**

**Focus:** String Manipulation, Regex (Light), and Categorical Data.

#### **One-Pager: Instructor & Student Guide**

**Scenario:** While you are finalizing the sales data, HR pings you. They have an "Employee Satisfaction Survey" and want to know if happy sales reps sell more. But their data is a disaster: some people typed "Male", others "M", dates are mixed formats. You need to clean this so it can eventually be joined with your Sales data.

**Dataset:** `hr_survey_raw.csv` (~1000 rows). Columns: `Employee_ID`, `Gender` (Messy: M, Male, m), `Comments`, `Join_Date`.

**Tier 1: The Standard Path (Time: 25 mins)**

1. **String Normalization:** Use `.str.lower()` and `.str.strip()` to clean the `Gender` column. Use `.map()` or `.replace()` to standardize to "Male"/"Female"/"Other".
2. **Date Parsing:** Use `pd.to_datetime()` with `errors='coerce'` to handle the mixed formats in `Join_Date`.
3. **Basic Sentiment:** Create a simple flag column: if `Comments` contains the word "salary" or "money", tag as "Compensation Issue".

**Tier 2: The Fast Track (Extra 15 mins)**

* **Task A (Regex):** The `Comments` section contains email addresses. Use `str.extract()` with a Regex pattern to pull these emails into a new column.
* **Task B (Optimization):** Convert `Gender` to the `category` data type to save memory.

---

## **Viz**

### **Viz 1: The Manager's Chart**

**Focus:** `matplotlib` / `seaborn`, GroupBy, and aesthetics.

#### **One-Pager: Instructor & Student Guide**

**Scenario:** Your `clean_sales_data.csv` is ready. Now the Manager wants a visual for the board meeting. She specifically wants to see "Total Revenue by Product Category." She is picky about colors and titles.

**Dataset:** `clean_sales_data.csv` (Output from ETL 2).

**Tier 1: The Standard Path (Time: 25 mins)**

1. **Aggregation:** Ask Copilot: *"Group by Category and sum the Revenue."*
2. **Basic Plot:** Ask Copilot: *"Create a bar chart of this data using Seaborn."*
3. **Formatting:** Ask Copilot: *"Add a title '2026 Sales Performance', rotate the x-axis labels 45 degrees, and add dollar signs to the y-axis."*

**Tier 2: The Fast Track (Extra 15 mins)**

* **Task A (Dual Axis):** Create a Combo Chart. Bar chart for "Revenue" and a Line chart for "Transaction Count" on the same plot.
* **Task B (Theme):** Use `plt.style.use()` to apply a professional theme (e.g., "fivethirtyeight") instantly.

---

### **Viz 2: The Report Generator**

**Focus:** `to_excel` (Multiple Sheets) or simple HTML/Markdown.

#### **One-Pager: Instructor & Student Guide**

**Scenario:** The chart is great, but the Manager also wants the raw numbers in Excel to play with. She asks for *one* Excel file containing:
1. An "Executive Summary" sheet (The aggregated data).
2. A "Backing Data" sheet (The full clean dataset).

**Dataset:** `clean_sales_data.csv` + The aggregated table from Viz 1.

**Tier 1: The Standard Path (Time: 25 mins)**

1. **Excel Writer:** Ask Copilot: *"How do I save two different dataframes to the same Excel file on different sheets?"* (Target: `pd.ExcelWriter`).
2. **Execution:** Write the "Summary" df to sheet 'Executive Summary' and the "Clean Data" df to sheet 'Backing Data'. Save as `final_report.xlsx`.
3. **Verification:** Open the resulting Excel file to prove it worked.

**Tier 2: The Fast Track (Extra 20 mins)**

* **Task A (HTML Report):** Also generate a `report.html` webpage using `to_html()`.
* **Task B (Currency):** Ask Copilot to format the 'Revenue' column as Currency (`$#,##0.00`) during export using the `float_format` parameter or engine options.

---

## **Auto**

### **Auto 1: The Professional Polish ("The Bridge")**

**Focus:** Formatting Excel *styles* via Python (`openpyxl` or `xlsxwriter`).

#### **One-Pager: Instructor & Student Guide**

**Scenario:** You sent `final_report.xlsx` to the boss. She says: *"Can you make the headers bold and blue? And the columns are too narrow, I can't read the product names."* You don't want to do this manually every quarter. You script the formatting.

**Dataset:** `final_report.xlsx` (Output from Viz 2) or regenerate it directly.

**Tier 1: The Standard Path (Time: 30 mins)**

1. **Load & Write:** Set up the Pandas Excel Writer with `engine='xlsxwriter'`.
2. **The Workbook Object:** Access the underlying workbook and worksheet objects.
3. **The Style:** Ask Copilot: *"How do I add a header format with bold text and a blue background using xlsxwriter?"*
4. **Apply:** Write the data, then loop through the header columns to apply the format. Auto-fit column widths.

**Tier 2: The Fast Track (Extra 20 mins)**

* **Task A (Conditional Formatting):** Ask Copilot: *"Apply conditional formatting to the Revenue column. If value > 10000, make cell green (High Performance)."*
* **Task B (Auto-Fit Script):** Write a robust script that measures the string length in every column and adjusts the Excel width automatically.

---

### **Auto 2: The File Organizer**

**Focus:** `os`, `shutil`, and file manipulation. Non-Data Automation.

#### **One-Pager: Instructor & Student Guide**

**Scenario:** The project is a success! But now your "Downloads" and project folder are a mess of raw CSVs, PDFs from HR, and temp Excel files. You need to archive everything into folders like `Raw_Data`, `Reports`, and `Archive` before you clock out.

**Dataset:** Your literal workspace folder (or a dummy folder generated for the exercise).

**Tier 1: The Standard Path (Time: 25 mins)**

1. **Scan:** Ask Copilot: *"How do I list all files in the current directory?"*
2. **Identify:** Write a loop to check file extensions (`.csv`, `.xlsx`, `.pdf`).
3. **Move:** Ask Copilot: *"How do I move files to a new subfolder using shutil based on their extension?"*
4. **Run:** Execute the script and watch the files organize themselves.

**Tier 2: The Fast Track (Extra 15 mins)**

* **Task A (Date Sorting):** Sort by *Date Created* (e.g., Folder `2026-Feb`) instead of file type.
* **Task B (Safety):** Add a "Dry Run" feature that prints what *would* happen without actually moving files.

---

## **Bonus / Advanced**

### **Bonus: The Big Data Stress Test**

**Focus:** Performance, File Formats (Parquet), and Out-of-Core Processing.

#### **One-Pager: Instructor & Student Guide**

**Scenario:** Fast forward two years. The company has grown. The "Sales Data" is no longer 3 files; it's 10GB of server logs. Your old Pandas scripts crash your laptop. You need a new engine.

**Dataset:** `server_logs_large` (Simulated large dataset).

**Tier 1: The Standard Path (Time: 30 mins)**

1. **The Crash:** Intentional failure. Try to load the huge CSV into Pandas. Watch it fail.
2. **Lazy Loading:** Use `duckdb.sql("SELECT * FROM 'logs/*.csv'")` to query without loading.
3. **The Transformation:** Aggregate error counts by hour using SQL.
4. **Format Conversion:** Convert the CSVs to **Parquet**. Compare the file size (Parquet should be much smaller).

**Instructor Notes**

* **Key Learning:** "Push-down execution." Don't bring data to the code; bring code to the data (DuckDB).
