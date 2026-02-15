import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
INPUT_FILE = os.path.join(DATA_DIR, "product_transactions.csv")
OUTPUT_SCATTER = os.path.join(DATA_DIR, "executive_scatter.png")
OUTPUT_REGRESSION = os.path.join(DATA_DIR, "category_regression.png")
OUTPUT_FACETED = os.path.join(DATA_DIR, "regional_scatter.png")


def currency_format(x, pos):
    """Format axis values as currency."""
    if x >= 1000:
        return f"${x:,.0f}"
    return f"${x:.0f}"


def main():
    # -------------------------------------------------------
    # STEP 1: Load and validate data
    # -------------------------------------------------------
    print("Loading data...")
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run 'exercise_setup_data.py' first.")
        return

    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} transactions.\n")

    # Ensure numeric types
    df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")
    df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

    # -------------------------------------------------------
    # CHART 1: Main Scatter — 4 dimensions in one chart
    # -------------------------------------------------------
    print("[Chart 1] Creating executive scatter plot...")

    # Set the theme BEFORE creating figures
    sns.set_theme(style="whitegrid", context="talk", palette="deep")

    fig, ax = plt.subplots(figsize=(14, 9))

    scatter = sns.scatterplot(
        data=df,
        x="Unit_Price",
        y="Revenue",
        hue="Category",
        size="Quantity",
        sizes=(20, 400),        # Min and max bubble sizes
        alpha=0.6,              # Transparency to handle overplotting
        edgecolor="white",      # White border on bubbles for clarity
        linewidth=0.5,
        ax=ax,
    )

    # Formatting
    ax.set_title("Sales Performance: Price vs Revenue by Category",
                 fontsize=18, fontweight="bold", pad=20)
    ax.set_xlabel("Unit Price", fontsize=14)
    ax.set_ylabel("Total Revenue", fontsize=14)

    # Currency formatting on both axes
    ax.xaxis.set_major_formatter(FuncFormatter(currency_format))
    ax.yaxis.set_major_formatter(FuncFormatter(currency_format))

    # Move legend outside the plot
    ax.legend(
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        borderaxespad=0,
        title="Legend",
        fontsize=10,
        title_fontsize=12,
    )

    plt.tight_layout()
    plt.savefig(OUTPUT_SCATTER, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved: {OUTPUT_SCATTER}")

    # -------------------------------------------------------
    # CHART 2: Regression lines per category (lmplot)
    # -------------------------------------------------------
    print("[Chart 2] Creating regression plot...")

    sns.set_theme(style="whitegrid", context="notebook", palette="deep")

    g = sns.lmplot(
        data=df,
        x="Unit_Price",
        y="Revenue",
        hue="Category",
        height=7,
        aspect=1.4,
        scatter_kws={"alpha": 0.4, "s": 30, "edgecolor": "white"},
        line_kws={"linewidth": 2},
        ci=95,  # 95% confidence interval band
    )

    g.figure.suptitle("Revenue vs Price — Regression by Category",
                       fontsize=16, fontweight="bold", y=1.02)
    g.set_axis_labels("Unit Price ($)", "Revenue ($)")

    # Currency formatting
    for ax in g.axes.flat:
        ax.xaxis.set_major_formatter(FuncFormatter(currency_format))
        ax.yaxis.set_major_formatter(FuncFormatter(currency_format))

    plt.tight_layout()
    plt.savefig(OUTPUT_REGRESSION, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved: {OUTPUT_REGRESSION}")

    # -------------------------------------------------------
    # CHART 3: Faceted scatter by Region (relplot)
    # -------------------------------------------------------
    print("[Chart 3] Creating faceted regional scatter...")

    sns.set_theme(style="whitegrid", context="notebook", palette="husl")

    g2 = sns.relplot(
        data=df,
        x="Unit_Price",
        y="Revenue",
        hue="Category",
        size="Quantity",
        sizes=(15, 250),
        alpha=0.5,
        col="Region",
        col_wrap=2,
        height=5,
        aspect=1.2,
        edgecolor="white",
        linewidth=0.3,
    )

    g2.figure.suptitle("Sales Scatter by Region",
                        fontsize=18, fontweight="bold", y=1.02)
    g2.set_axis_labels("Unit Price ($)", "Revenue ($)")

    # Currency formatting for all panels
    for ax in g2.axes.flat:
        ax.xaxis.set_major_formatter(FuncFormatter(currency_format))
        ax.yaxis.set_major_formatter(FuncFormatter(currency_format))

    plt.tight_layout()
    plt.savefig(OUTPUT_FACETED, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved: {OUTPUT_FACETED}")

    # -------------------------------------------------------
    # Summary
    # -------------------------------------------------------
    print(f"\nSUCCESS: All 3 charts generated!")
    print(f"  1. {OUTPUT_SCATTER}  — Main scatter (4D)")
    print(f"  2. {OUTPUT_REGRESSION}  — Regression by category")
    print(f"  3. {OUTPUT_FACETED}  — Faceted by region")


if __name__ == "__main__":
    main()
