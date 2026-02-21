import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")
INPUT_FILE = os.path.join(DATA_DIR, "employee_performance.csv")

OUTPUT_HEATMAP = os.path.join(DATA_DIR, "solutions", "correlation_heatmap.png")
OUTPUT_VIOLIN = os.path.join(DATA_DIR, "solutions", "satisfaction_violins.png")
OUTPUT_PAIRPLOT = os.path.join(DATA_DIR, "solutions", "metrics_pairplot.png")
OUTPUT_BOXSTRIP = os.path.join(DATA_DIR, "solutions", "revenue_by_seniority.png")

# Seniority order for plotting
SENIORITY_ORDER = ["Junior", "Mid-Level", "Senior", "Lead", "Director"]



# Ensure solutions directory exists
os.makedirs(os.path.join(DATA_DIR, 'solutions'), exist_ok=True)

def main():
    # -------------------------------------------------------
    # STEP 1: Load data
    # -------------------------------------------------------
    print("Loading data...")
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run 'exercise_setup_data.py' first.")
        return

    df = pd.read_csv(INPUT_FILE)

    # Restore ordered categorical for Seniority
    df["Seniority"] = pd.Categorical(
        df["Seniority"], categories=SENIORITY_ORDER, ordered=True
    )

    print(f"Loaded {len(df)} rows.\n")

    # Numeric columns for correlation
    numeric_cols = [
        "Years_Experience", "Satisfaction_Score",
        "Revenue_Generated", "Deals_Closed", "Training_Hours"
    ]

    # -------------------------------------------------------
    # CHART 1: Correlation Heatmap
    # -------------------------------------------------------
    print("[Chart 1] Creating correlation heatmap...")
    sns.set_theme(style="white", context="talk")

    corr_matrix = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8))

    # Generate a mask for the upper triangle (avoid redundancy)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    sns.heatmap(
        corr_matrix,
        mask=mask,
        annot=True,              # Show numbers in each cell
        fmt=".2f",               # Two decimal places
        cmap="RdBu_r",          # Diverging: red positive, blue negative
        center=0,                # Center colorbar at 0
        vmin=-1, vmax=1,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8, "label": "Correlation"},
        ax=ax,
    )

    ax.set_title("Correlation Matrix — Employee Metrics",
                 fontsize=18, fontweight="bold", pad=20)

    plt.tight_layout()
    plt.savefig(OUTPUT_HEATMAP, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved: {OUTPUT_HEATMAP}")

    # -------------------------------------------------------
    # CHART 2: Violin Plot — Satisfaction by Department
    # -------------------------------------------------------
    print("[Chart 2] Creating violin plot...")
    sns.set_theme(style="whitegrid", context="talk", palette="Set2")

    fig, ax = plt.subplots(figsize=(12, 7))

    sns.violinplot(
        data=df,
        x="Department",
        y="Satisfaction_Score",
        hue="Gender",
        split=True,             # Split violin: each half = one gender
        inner="quart",          # Show quartile lines inside
        linewidth=1.2,
        ax=ax,
    )

    ax.set_title("Satisfaction Score Distribution by Department & Gender",
                 fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Department", fontsize=13)
    ax.set_ylabel("Satisfaction Score (1-10)", fontsize=13)
    ax.set_ylim(0, 11)

    ax.legend(title="Gender", fontsize=11, title_fontsize=12)

    plt.tight_layout()
    plt.savefig(OUTPUT_VIOLIN, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved: {OUTPUT_VIOLIN}")

    # -------------------------------------------------------
    # CHART 3: Pair Plot — Multi-variable exploration
    # -------------------------------------------------------
    print("[Chart 3] Creating pair plot (this may take a moment)...")
    sns.set_theme(style="ticks", context="notebook", palette="deep")

    pair_vars = ["Revenue_Generated", "Satisfaction_Score",
                 "Years_Experience", "Deals_Closed"]

    g = sns.pairplot(
        df,
        vars=pair_vars,
        hue="Department",
        diag_kind="kde",         # Kernel density on diagonal (smoother than hist)
        plot_kws={"alpha": 0.5, "s": 20, "edgecolor": "white", "linewidth": 0.3},
        diag_kws={"linewidth": 1.5},
        height=2.5,
    )

    g.figure.suptitle("Pair Plot — Key Metrics by Department",
                       fontsize=16, fontweight="bold", y=1.02)

    plt.tight_layout()
    plt.savefig(OUTPUT_PAIRPLOT, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved: {OUTPUT_PAIRPLOT}")

    # -------------------------------------------------------
    # CHART 4: Box + Strip Combo — Revenue by Seniority
    # -------------------------------------------------------
    print("[Chart 4] Creating box + strip plot...")
    sns.set_theme(style="whitegrid", context="talk", palette="viridis")

    fig, ax = plt.subplots(figsize=(12, 7))

    # Box plot first (background layer)
    sns.boxplot(
        data=df,
        x="Seniority",
        y="Revenue_Generated",
        order=SENIORITY_ORDER,
        showfliers=False,        # Hide default outlier dots (strip will show them)
        boxprops={"alpha": 0.4},
        width=0.6,
        ax=ax,
    )

    # Strip plot on top (individual data points)
    sns.stripplot(
        data=df,
        x="Seniority",
        y="Revenue_Generated",
        order=SENIORITY_ORDER,
        size=4,
        alpha=0.4,
        jitter=True,
        color="black",
        ax=ax,
    )

    ax.set_title("Revenue Distribution by Seniority Level",
                 fontsize=16, fontweight="bold", pad=15)
    ax.set_xlabel("Seniority Level", fontsize=13)
    ax.set_ylabel("Revenue Generated ($)", fontsize=13)

    # Currency formatting on Y axis
    from matplotlib.ticker import FuncFormatter
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f"${x:,.0f}"))

    plt.tight_layout()
    plt.savefig(OUTPUT_BOXSTRIP, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved: {OUTPUT_BOXSTRIP}")

    # -------------------------------------------------------
    # Summary
    # -------------------------------------------------------
    print(f"\nSUCCESS: All 4 statistical charts generated!")
    print(f"  1. {OUTPUT_HEATMAP}")
    print(f"  2. {OUTPUT_VIOLIN}")
    print(f"  3. {OUTPUT_PAIRPLOT}")
    print(f"  4. {OUTPUT_BOXSTRIP}")


if __name__ == "__main__":
    main()
