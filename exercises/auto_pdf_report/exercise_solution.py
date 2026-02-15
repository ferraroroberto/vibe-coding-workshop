import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend (no display needed)
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from fpdf import FPDF
from datetime import datetime
import os

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
INPUT_FILE = os.path.join(DATA_DIR, "quarterly_sales.csv")
OUTPUT_PDF = os.path.join(DATA_DIR, "quarterly_report.pdf")

# Temporary chart files
CHART_BAR = os.path.join(DATA_DIR, "_temp_bar_chart.png")
CHART_PIE = os.path.join(DATA_DIR, "_temp_pie_chart.png")

# Brand colors (RGB 0-255)
BRAND_BLUE = (41, 98, 163)
BRAND_LIGHT_BLUE = (220, 235, 250)
BRAND_DARK = (44, 62, 80)
BRAND_GRAY = (149, 165, 166)
TEXT_DARK = (33, 33, 33)


# -------------------------------------------------------
# CUSTOM PDF CLASS WITH HEADER & FOOTER
# -------------------------------------------------------
class SalesReport(FPDF):
    """Custom PDF class with consistent header and footer."""

    def header(self):
        """Called automatically at the top of every page."""
        if self.page_no() == 1:
            return  # Skip header on cover page

        # Blue line at top
        self.set_draw_color(*BRAND_BLUE)
        self.set_line_width(0.8)
        self.line(10, 10, 200, 10)

        # Header text
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*BRAND_BLUE)
        self.set_y(12)
        self.cell(0, 6, "Quarterly Sales Report | Q4 2026", align="L")
        self.cell(0, 6, "CONFIDENTIAL", align="R")
        self.ln(10)

    def footer(self):
        """Called automatically at the bottom of every page."""
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*BRAND_GRAY)

        # Page number
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


# -------------------------------------------------------
# CHART GENERATION FUNCTIONS
# -------------------------------------------------------
def generate_bar_chart(category_revenue):
    """Create a professional bar chart and save as PNG."""
    fig, ax = plt.subplots(figsize=(8, 4.5))

    categories = category_revenue.index.tolist()
    revenues = category_revenue.values.tolist()

    # Gradient-like colors
    colors = ["#2962A3", "#3A7BD5", "#5B9BD5", "#7FB3E0", "#A4CCE9"]
    bars = ax.barh(categories, revenues, color=colors[:len(categories)], edgecolor="white", height=0.6)

    # Add value labels on bars
    for bar, rev in zip(bars, revenues):
        ax.text(
            bar.get_width() + max(revenues) * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"${rev:,.0f}",
            va="center",
            fontsize=10,
            color="#333333",
            fontweight="bold",
        )

    ax.set_xlabel("Total Revenue ($)", fontsize=11, color="#555555")
    ax.set_title("Revenue by Category", fontsize=14, fontweight="bold", color="#2C3E50", pad=15)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f"${x:,.0f}"))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(colors="#555555")

    plt.tight_layout()
    plt.savefig(CHART_BAR, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Bar chart saved: {CHART_BAR}")


def generate_pie_chart(category_revenue):
    """Create a professional pie chart and save as PNG."""
    fig, ax = plt.subplots(figsize=(6, 6))

    labels = category_revenue.index.tolist()
    sizes = category_revenue.values.tolist()
    colors = ["#2962A3", "#3A7BD5", "#5B9BD5", "#7FB3E0", "#A4CCE9"]
    explode = [0.03] * len(labels)

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors[:len(labels)],
        explode=explode[:len(labels)],
        textprops={"fontsize": 10},
        pctdistance=0.75,
    )

    for autotext in autotexts:
        autotext.set_fontweight("bold")
        autotext.set_color("white")

    ax.set_title("Revenue Distribution", fontsize=14, fontweight="bold", color="#2C3E50", pad=20)

    plt.tight_layout()
    plt.savefig(CHART_PIE, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Pie chart saved: {CHART_PIE}")


# -------------------------------------------------------
# MAIN REPORT BUILDER
# -------------------------------------------------------
def main():
    print("=" * 50)
    print("PDF REPORT GENERATOR")
    print("=" * 50)

    # -------------------------------------------------------
    # STEP 1: Load and prepare data
    # -------------------------------------------------------
    print("\n[Step 1] Loading data...")
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run 'exercise_setup_data.py' first.")
        return

    df = pd.read_csv(INPUT_FILE)
    df["Date"] = pd.to_datetime(df["Date"])
    print(f"  Loaded {len(df)} rows.")

    # Aggregations
    category_revenue = df.groupby("Category")["Revenue"].sum().sort_values(ascending=True)
    total_revenue = df["Revenue"].sum()
    total_orders = len(df)
    avg_order = df["Revenue"].mean()
    top_category = category_revenue.idxmax()
    top_10 = df.nlargest(10, "Revenue")

    # -------------------------------------------------------
    # STEP 2: Generate charts
    # -------------------------------------------------------
    print("\n[Step 2] Generating charts...")
    generate_bar_chart(category_revenue)
    generate_pie_chart(category_revenue)

    # -------------------------------------------------------
    # STEP 3: Build PDF
    # -------------------------------------------------------
    print("\n[Step 3] Building PDF...")

    pdf = SalesReport()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # --- COVER PAGE ---
    pdf.add_page()
    pdf.ln(60)

    # Title
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(*BRAND_BLUE)
    pdf.cell(0, 15, "Quarterly Sales Report", align="C", new_x="LMARGIN", new_y="NEXT")

    # Subtitle
    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(*BRAND_DARK)
    pdf.cell(0, 12, "Q4 2026 Performance Summary", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(10)

    # Date
    pdf.set_font("Helvetica", "I", 12)
    pdf.set_text_color(*BRAND_GRAY)
    report_date = datetime.now().strftime("%B %d, %Y")
    pdf.cell(0, 10, f"Generated: {report_date}", align="C", new_x="LMARGIN", new_y="NEXT")

    # Decorative line
    pdf.ln(15)
    pdf.set_draw_color(*BRAND_BLUE)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())

    pdf.ln(20)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*BRAND_DARK)
    pdf.cell(0, 8, "Prepared by: Data Analytics Team", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Classification: CONFIDENTIAL", align="C", new_x="LMARGIN", new_y="NEXT")

    # --- KPI PAGE ---
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*BRAND_DARK)
    pdf.cell(0, 12, "Key Performance Indicators", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # KPI boxes
    kpis = [
        ("Total Revenue", f"${total_revenue:,.2f}"),
        ("Total Orders", f"{total_orders:,}"),
        ("Average Order Value", f"${avg_order:,.2f}"),
        ("Top Category", top_category),
    ]

    box_width = 90
    box_height = 30
    x_start = 10

    for i, (label, value) in enumerate(kpis):
        col = i % 2
        row = i // 2

        x = x_start + col * (box_width + 5)
        y = pdf.get_y() + row * (box_height + 5)

        # Box background
        pdf.set_fill_color(*BRAND_LIGHT_BLUE)
        pdf.set_draw_color(*BRAND_BLUE)
        pdf.rect(x, y, box_width, box_height, style="FD")

        # Label
        pdf.set_xy(x + 3, y + 3)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*BRAND_BLUE)
        pdf.cell(box_width - 6, 5, label)

        # Value
        pdf.set_xy(x + 3, y + 12)
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(*BRAND_DARK)
        pdf.cell(box_width - 6, 12, value)

    pdf.set_y(pdf.get_y() + 2 * (box_height + 5) + 10)

    # --- CHARTS PAGE ---
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*BRAND_DARK)
    pdf.cell(0, 12, "Revenue Analysis", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Bar chart
    if os.path.exists(CHART_BAR):
        pdf.image(CHART_BAR, x=10, w=190)
        pdf.ln(5)

    # Pie chart (may need new page)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*BRAND_DARK)
    pdf.cell(0, 12, "Revenue Distribution", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    if os.path.exists(CHART_PIE):
        pdf.image(CHART_PIE, x=35, w=140)
        pdf.ln(5)

    # --- TABLE PAGE ---
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*BRAND_DARK)
    pdf.cell(0, 12, "Top 10 Transactions", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # Table header
    col_widths = [25, 35, 40, 30, 30, 30]
    headers = ["Order ID", "Date", "Product", "Category", "Qty", "Revenue"]

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(*BRAND_BLUE)
    pdf.set_text_color(255, 255, 255)

    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, border=1, fill=True, align="C")
    pdf.ln()

    # Table rows with alternating colors
    pdf.set_font("Helvetica", "", 8)

    for row_idx, (_, row) in enumerate(top_10.iterrows()):
        if row_idx % 2 == 0:
            pdf.set_fill_color(245, 248, 252)
        else:
            pdf.set_fill_color(255, 255, 255)

        pdf.set_text_color(*TEXT_DARK)

        cells = [
            str(row["Order_ID"]),
            str(row["Date"].strftime("%Y-%m-%d") if hasattr(row["Date"], "strftime") else row["Date"]),
            str(row["Product"])[:20],
            str(row["Category"]),
            str(row["Quantity"]),
            f"${row['Revenue']:,.2f}",
        ]

        for i, cell_val in enumerate(cells):
            align = "R" if i == 5 else "L"
            pdf.cell(col_widths[i], 7, cell_val, border=1, fill=True, align=align)
        pdf.ln()

    # --- SAVE ---
    pdf.output(OUTPUT_PDF)
    print(f"\nSUCCESS: PDF report saved to {OUTPUT_PDF}")

    # Clean up temp chart files
    for temp_file in [CHART_BAR, CHART_PIE]:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"  Cleaned up: {os.path.basename(temp_file)}")

    print(f"\n{'=' * 50}")
    print("REPORT GENERATION COMPLETE!")
    print(f"  Pages: ~5 (Cover + KPIs + Charts + Table)")
    print(f"  Output: {OUTPUT_PDF}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
