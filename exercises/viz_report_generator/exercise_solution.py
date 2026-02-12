import pandas as pd
import os

# --- CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
INPUT_FILE = os.path.join(DATA_DIR, "clean_sales_data.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "final_report.xlsx")

def main():
    print("--- Starting Report Generation ---")
    
    # 1. Load the clean dataset
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file not found at {INPUT_FILE}. Please run exercise_setup_data.py first.")
        return

    df = pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} rows from {INPUT_FILE}")

    # 2. Create the 'Executive Summary' (Aggregation)
    # Group by Category and sum the Revenue
    summary_df = df.groupby("Category")[["Revenue"]].sum().reset_index()
    
    # Sort for better readability (highest revenue first)
    summary_df = summary_df.sort_values(by="Revenue", ascending=False)
    
    print("\nGenerated Summary:")
    print(summary_df)

    # 3. Write both dataframes to Excel (Multiple Sheets)
    print(f"\nWriting to {OUTPUT_FILE}...")
    
    # using 'with' ensures the file is saved and closed properly
    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
        
        # Sheet 1: Executive Summary
        # startrow=1 leaves a blank line at the top, or 0 starts at top
        summary_df.to_excel(writer, sheet_name='Executive Summary', index=False)
        
        # Sheet 2: Backing Data
        # float_format="%.2f" forces 2 decimal places in Excel
        df.to_excel(writer, sheet_name='Backing Data', index=False, float_format="%.2f")
        
    print(f"Success! Report generated at: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
