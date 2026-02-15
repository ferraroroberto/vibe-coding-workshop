import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import os

# --- CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
INPUT_FILE = os.path.join(DATA_DIR, "clean_sales_data.csv")
OUTPUT_IMAGE = os.path.join(DATA_DIR, "revenue_by_category.png")

def main():
    # 1. Load the Data
    print(f"Loading data from: {INPUT_FILE}")
    if not os.path.exists(INPUT_FILE):
        print("Error: File not found. Please run 'exercise_setup_data.py' first.")
        return

    df = pd.read_csv(INPUT_FILE)

    # 2. Aggregation: Sum Revenue by Category
    # We group by 'Category' and sum the numeric columns, then reset index to keep 'Category' as a column
    category_sales = df.groupby('Category')['Revenue'].sum().reset_index()
    
    # Sort values for a better chart (highest revenue first)
    category_sales = category_sales.sort_values(by='Revenue', ascending=False)
    
    print("\nAggregated Data Preview:")
    print(category_sales)

    # 3. Setup the Plot Style
    # sns.set_theme(style="whitegrid") # Optional: Makes it look cleaner
    plt.figure(figsize=(10, 6)) # Size: 10 inches wide, 6 inches tall

    # 4. Create the Bar Chart
    chart = sns.barplot(
        data=category_sales,
        x='Category',
        y='Revenue',
        palette='viridis' # A nice professional color palette
    )

    # 5. Formatting
    plt.title('2026 Sales Performance by Category', fontsize=16, weight='bold')
    plt.xlabel('Product Category', fontsize=12)
    plt.ylabel('Total Revenue', fontsize=12)
    
    # Rotate x-axis labels to prevent overlap
    plt.xticks(rotation=45)

    # Format Y-axis as Currency (The "Master" touch)
    # This defines a function that converts 10000 -> $10,000
    def currency_format(x, pos):
        return '${:,.0f}'.format(x)
    
    chart.yaxis.set_major_formatter(FuncFormatter(currency_format))

    # Adjust layout to prevent cutting off labels
    plt.tight_layout()

    # 6. Show or Save
    # plt.show() # Uncomment to see it in a window
    plt.savefig(OUTPUT_IMAGE)
    print(f"\nChart saved successfully to: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
