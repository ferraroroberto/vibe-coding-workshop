# Exercise Card: Viz 3 - The Interactive Dashboard (The Wow Factor)

## Title & Problem Statement
**The Wow Factor: Building an Interactive Executive Dashboard with Plotly**

Static charts are great for slide decks, but modern stakeholders expect interactivity — hover tooltips, click-to-filter, zoom, and pan. In this exercise, you graduate from matplotlib/seaborn to **Plotly**, a library that produces JavaScript-powered visualizations directly from Python. The output is a standalone HTML file that anyone can open in a browser — no Python installation required on the viewer's end. This is the tool that bridges the gap between "data analysis" and "data product."

## Difficulty & Estimated Time
*   **Difficulty:** Intermediate-Advanced (Visualization Focus)
*   **Estimated Time:** 35-45 Minutes

## Required Libraries
*   `pandas`: Data loading, aggregation, and time-series manipulation.
*   `plotly`: The star of the show. Specifically:
    *   `plotly.express` — High-level API for quick, beautiful charts.
    *   `plotly.graph_objects` — Lower-level API for full customization.
    *   `plotly.subplots` — For combining multiple charts into a dashboard layout.

## Didactic Step-by-Step

### 1. Data Preparation
**Concept:** Before visualizing, reshape the data into the formats each chart type expects.
*   **Action:** Load the CSV, ensure `Date` is a datetime, and create aggregated views (monthly revenue, top products, regional breakdown).

### 2. KPI Calculation
**Concept:** Key Performance Indicators are single-number summaries that executives look at first.
*   **Action:** Calculate Total Revenue, Total Orders, and Average Order Value. Display them as `plotly.graph_objects.Indicator` with formatted numbers.

### 3. Sunburst Chart
**Concept:** A hierarchical chart that shows part-to-whole relationships across multiple levels (Region → Category → Product).
*   **Action:** Use `plotly.express.sunburst()` with `path=['Region', 'Category', 'Product']` and `values='Revenue'`. The result is a gorgeous, clickable, drill-down chart.

### 4. Time-Series Line Chart
**Concept:** Showing trends over time with the ability to toggle regions on/off.
*   **Action:** Group data by month and region, then use `plotly.express.line()` with `color='Region'`. Plotly automatically adds a legend that acts as a filter.

### 5. Top Products Bar Chart
**Concept:** A ranked bar chart with rich hover information.
*   **Action:** Aggregate revenue by product, take the top 10, and use `plotly.express.bar()` with `hover_data` to show quantity and average price on hover.

### 6. Combining into a Dashboard
**Concept:** Using `plotly.subplots.make_subplots()` or writing a combined HTML page.
*   **Action:** Combine all figures into a single HTML file using Plotly's `to_html()` method with inline JavaScript.

## Tips for Coding and Vibe-Coding

1.  **`plotly.express` first, `graph_objects` second:** Start with the high-level `px` API for quick results. Only drop down to `go` when you need fine-grained control.
2.  **`.update_layout()` is your styling powerhouse:** After creating any figure, chain `.update_layout(template='plotly_dark', title_font_size=20)` to instantly transform the look.
3.  **Templates matter:** Try `"plotly_dark"`, `"seaborn"`, `"ggplot2"`, or `"presentation"` for instant theme changes.
4.  **HTML output is portable:** `fig.write_html("dashboard.html", include_plotlyjs=True)` creates a fully self-contained file. No server, no dependencies on the viewer's side.
5.  **Sunburst + Treemap:** If the sunburst feels too circular, swap to `px.treemap()` for a rectangular alternative with the exact same code structure.

## Copilot Master Prompt
*You can use this prompt to generate the solution code:*

> "I have a pandas DataFrame with columns: Date, Region, Category, Product, Revenue, Quantity, Unit_Price.
> Using Plotly, create a professional interactive dashboard saved as a single HTML file that contains:
> 1. KPI indicators at the top showing Total Revenue, Total Orders, and Average Order Value.
> 2. A sunburst chart showing revenue breakdown by Region > Category > Product.
> 3. A monthly time-series line chart of revenue colored by Region.
> 4. A horizontal bar chart of the top 10 products by total revenue with hover details.
> Use a dark professional theme and make the HTML self-contained."
