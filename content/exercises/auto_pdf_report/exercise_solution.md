# Exercise Card: Auto 3 - The PDF Report Generator (The Executive Deliverable)

## Title & Problem Statement
**The Executive Deliverable: Automating Professional PDF Reports with Python**

In many organizations, the "last mile" of data analysis is a PDF report. Dashboards are great for exploration, but when the CFO needs something for the board meeting, it's a PDF. Creating these manually — screenshotting charts, pasting into Word, formatting tables — is tedious and error-prone. In this exercise, you will automate the entire process: generate charts with matplotlib, build tables, compose a multi-page PDF with cover page and branding, all from a single Python script. Run it once, and it works every quarter.

## Difficulty & Estimated Time
*   **Difficulty:** Intermediate (Automation Focus)
*   **Estimated Time:** 35-45 Minutes

## Required Libraries
*   `pandas`: Data loading and aggregation.
*   `matplotlib`: Generating the charts (bar chart, pie chart) as image files.
*   `fpdf2`: A lightweight library for creating PDF documents from Python. It handles text, images, tables, headers, footers, and multi-page layout.

## Didactic Step-by-Step

### 1. Data Preparation
**Concept:** Aggregate your data into the shapes needed for each report section.
*   **Action:** Load the sales CSV. Create aggregations: revenue by category (for bar chart), revenue distribution (for pie chart), and top 10 transactions (for the table).

### 2. Chart Generation
**Concept:** Generate charts as PNG images first, then embed them into the PDF.
*   **Action:** Use matplotlib to create a styled bar chart and pie chart. Save them as temporary PNG files using `plt.savefig()`. These will be inserted into the PDF.

### 3. PDF Setup with FPDF
**Concept:** FPDF lets you build PDF pages programmatically — add text, images, tables, headers, and footers.
*   **Action:** Create a custom class extending `FPDF` that overrides `header()` and `footer()` methods for consistent branding on every page. Set fonts, colors, and margins.

### 4. Cover Page
**Concept:** The first impression matters. A cover page sets the professional tone.
*   **Action:** Add a page, center the report title in a large font, add the date, and a subtitle. Use `cell()` and `ln()` for positioning.

### 5. KPI Section
**Concept:** Large, bold numbers that executives can read in 2 seconds.
*   **Action:** Calculate Total Revenue, Total Orders, and Top Category. Display them in a formatted section using colored cells and bold fonts.

### 6. Charts & Table Pages
**Concept:** Embedding images and drawing formatted tables.
*   **Action:** Use `pdf.image()` to insert the chart PNGs. For the table, use `pdf.cell()` in a loop with alternating background colors for readability.

## Tips for Coding and Vibe-Coding

1.  **FPDF vs ReportLab:** FPDF (specifically `fpdf2`) is simpler and has no complex dependencies. ReportLab is more powerful but heavier. For business reports, FPDF is usually enough.
2.  **Chart resolution matters:** When saving matplotlib charts for PDF embedding, use `dpi=150` or higher. Low-DPI charts look blurry when printed.
3.  **Color consistency:** Define your brand colors once at the top (e.g., `BRAND_BLUE = (79, 129, 189)`) and reuse them across charts, headers, and table styling.
4.  **Font limitations:** FPDF comes with Helvetica, Times, and Courier. For custom fonts, use `pdf.add_font()`. Stick with the defaults for this exercise.
5.  **Temporary files:** Generate chart PNGs in the data directory and clean them up after the PDF is built — or leave them as a bonus deliverable.

## Copilot Master Prompt
*You can use this prompt to generate the solution code:*

> "I have a pandas DataFrame with columns: Date, Category, Product, Revenue, Quantity.
> Using fpdf2 and matplotlib, create a Python script that generates a professional multi-page PDF report containing:
> 1. A cover page with title 'Quarterly Sales Report', the current date, and a subtitle.
> 2. A KPI summary section showing Total Revenue, Total Orders, and Top Category in large bold text.
> 3. A bar chart (matplotlib, saved as PNG, embedded in PDF) showing Revenue by Category.
> 4. A pie chart showing revenue distribution by category.
> 5. A formatted table of the top 10 transactions with alternating row colors.
> 6. Page numbers in the footer on every page.
> Use a professional blue color scheme throughout."
