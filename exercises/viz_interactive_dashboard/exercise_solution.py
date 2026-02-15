import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
INPUT_FILE = os.path.join(DATA_DIR, "sales_data_full.csv")
OUTPUT_HTML = os.path.join(DATA_DIR, "dashboard.html")
THEME = "plotly_dark"  # Try: "plotly_dark", "seaborn", "ggplot2", "presentation"


def main():
    # -------------------------------------------------------
    # STEP 1: Load and prepare data
    # -------------------------------------------------------
    print("Loading data...")
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run 'exercise_setup_data.py' first.")
        return

    df = pd.read_csv(INPUT_FILE)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    print(f"Loaded {len(df)} rows.\n")

    # -------------------------------------------------------
    # STEP 2: Calculate KPIs
    # -------------------------------------------------------
    total_revenue = df["Revenue"].sum()
    total_orders = len(df)
    avg_order_value = df["Revenue"].mean()

    print(f"KPIs -> Revenue: ${total_revenue:,.2f} | Orders: {total_orders:,} | AOV: ${avg_order_value:,.2f}")

    # -------------------------------------------------------
    # STEP 3: Create KPI Indicators
    # -------------------------------------------------------
    fig_kpi = make_subplots(
        rows=1, cols=3,
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]],
        column_widths=[0.33, 0.33, 0.34],
    )

    fig_kpi.add_trace(
        go.Indicator(
            mode="number",
            value=total_revenue,
            title={"text": "Total Revenue", "font": {"size": 18}},
            number={"prefix": "$", "valueformat": ",.0f", "font": {"size": 36}},
        ),
        row=1, col=1,
    )

    fig_kpi.add_trace(
        go.Indicator(
            mode="number",
            value=total_orders,
            title={"text": "Total Orders", "font": {"size": 18}},
            number={"valueformat": ",", "font": {"size": 36}},
        ),
        row=1, col=2,
    )

    fig_kpi.add_trace(
        go.Indicator(
            mode="number",
            value=avg_order_value,
            title={"text": "Avg Order Value", "font": {"size": 18}},
            number={"prefix": "$", "valueformat": ",.2f", "font": {"size": 36}},
        ),
        row=1, col=3,
    )

    fig_kpi.update_layout(
        template=THEME,
        height=200,
        margin=dict(t=40, b=20, l=20, r=20),
    )

    # -------------------------------------------------------
    # STEP 4: Sunburst Chart (Region > Category > Product)
    # -------------------------------------------------------
    print("Creating sunburst chart...")

    fig_sunburst = px.sunburst(
        df,
        path=["Region", "Category", "Product"],
        values="Revenue",
        color="Region",
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="Revenue Breakdown: Region → Category → Product",
    )

    fig_sunburst.update_layout(
        template=THEME,
        height=550,
        margin=dict(t=60, b=20, l=20, r=20),
        title_font_size=20,
    )

    # -------------------------------------------------------
    # STEP 5: Time-Series Line Chart (Monthly Revenue by Region)
    # -------------------------------------------------------
    print("Creating time-series chart...")

    monthly_region = (
        df.groupby(["Month", "Region"])["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Month")
    )

    fig_timeseries = px.line(
        monthly_region,
        x="Month",
        y="Revenue",
        color="Region",
        title="Monthly Revenue Trend by Region",
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )

    fig_timeseries.update_layout(
        template=THEME,
        height=450,
        margin=dict(t=60, b=40, l=60, r=20),
        title_font_size=20,
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        yaxis_tickprefix="$",
        yaxis_tickformat=",",
        legend_title="Region",
        hovermode="x unified",
    )

    # -------------------------------------------------------
    # STEP 6: Top 10 Products Bar Chart
    # -------------------------------------------------------
    print("Creating top products chart...")

    top_products = (
        df.groupby("Product")
        .agg(
            Total_Revenue=("Revenue", "sum"),
            Total_Quantity=("Quantity", "sum"),
            Avg_Unit_Price=("Unit_Price", "mean"),
            Order_Count=("Order_ID", "count"),
        )
        .reset_index()
        .sort_values("Total_Revenue", ascending=True)
        .tail(10)
    )

    top_products["Avg_Unit_Price"] = top_products["Avg_Unit_Price"].round(2)

    fig_bar = px.bar(
        top_products,
        x="Total_Revenue",
        y="Product",
        orientation="h",
        title="Top 10 Products by Revenue",
        color="Total_Revenue",
        color_continuous_scale="Viridis",
        hover_data={
            "Total_Quantity": True,
            "Avg_Unit_Price": ":.2f",
            "Order_Count": True,
            "Total_Revenue": ":$,.0f",
        },
    )

    fig_bar.update_layout(
        template=THEME,
        height=450,
        margin=dict(t=60, b=40, l=150, r=20),
        title_font_size=20,
        xaxis_title="Total Revenue ($)",
        yaxis_title="",
        xaxis_tickprefix="$",
        xaxis_tickformat=",",
        coloraxis_showscale=False,
    )

    # -------------------------------------------------------
    # STEP 7: Combine into a single HTML dashboard
    # -------------------------------------------------------
    print("\nAssembling dashboard...")

    # Convert each figure to an HTML div (without full page wrapper)
    kpi_html = fig_kpi.to_html(full_html=False, include_plotlyjs=False)
    sunburst_html = fig_sunburst.to_html(full_html=False, include_plotlyjs=False)
    timeseries_html = fig_timeseries.to_html(full_html=False, include_plotlyjs=False)
    bar_html = fig_bar.to_html(full_html=False, include_plotlyjs=False)

    # Build the full HTML page
    dashboard_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales Dashboard 2026</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #111111;
            color: #e0e0e0;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            padding: 20px 0;
            border-bottom: 2px solid #333;
            margin-bottom: 20px;
        }}
        .header h1 {{
            font-size: 2.2em;
            color: #00d4ff;
            margin-bottom: 5px;
        }}
        .header p {{
            font-size: 1.1em;
            color: #888;
        }}
        .chart-section {{
            background: #1a1a2e;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }}
        .grid-row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        .footer {{
            text-align: center;
            padding: 20px 0;
            color: #555;
            font-size: 0.9em;
            border-top: 1px solid #333;
            margin-top: 20px;
        }}
        @media (max-width: 900px) {{
            .grid-row {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Sales Performance Dashboard 2026</h1>
        <p>Interactive Executive Report &mdash; Generated with Python &amp; Plotly</p>
    </div>

    <div class="chart-section">
        {kpi_html}
    </div>

    <div class="grid-row">
        <div class="chart-section">
            {sunburst_html}
        </div>
        <div class="chart-section">
            {bar_html}
        </div>
    </div>

    <div class="chart-section">
        {timeseries_html}
    </div>

    <div class="footer">
        <p>Dashboard generated automatically using Python, Pandas &amp; Plotly.
        &copy; 2026 Workshop</p>
    </div>
</body>
</html>"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(dashboard_html)

    print(f"\nSUCCESS: Dashboard saved to {OUTPUT_HTML}")
    print("Open this file in any web browser to explore the interactive charts!")


if __name__ == "__main__":
    main()
