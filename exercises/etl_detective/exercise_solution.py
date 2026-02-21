import pandas as pd
import os

# --- CONFIGURATION ---
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
INPUT_FILE = "combined_sales.csv"
OUTPUT_FILE = "solutions/clean_sales_data.csv"


# Ensure solutions directory exists
os.makedirs(os.path.join(BASE_DIR, 'solutions'), exist_ok=True)

def main():
    print("--- Starting ETL 2: The Data Detective ---")
    
    # 1. Load the Data
    file_path = os.path.join(BASE_DIR, INPUT_FILE)
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        print("Tip: Run 'exercise_setup_data.py' first.")
        return

    df = pd.read_csv(file_path)
    initial_count = len(df)
    print(f"Initial Row Count: {initial_count}")
    
    # --- TIER 1: CLEANING BASICS ---

    # 2. Remove Duplicates
    # we look for duplicates specifically in Order_ID.
    # keep='first' is default, but explicit is better than implicit.
    df_clean = df.drop_duplicates(subset=['Order_ID'], keep='first')
    
    duplicates_removed = initial_count - len(df_clean)
    print(f"Duplicates removed: {duplicates_removed}")

    # 3. Filter Negative Numbers
    # Logic: We only want rows where Revenue is greater than 0
    df_clean = df_clean[df_clean['Revenue'] > 0]
    
    # Calculate how many were removed by this filter
    # Note: We compare against current length, not initial
    negatives_removed = (initial_count - duplicates_removed) - len(df_clean)
    print(f"Negative values removed: {negatives_removed}")

    # --- TIER 2: ADVANCED LOGIC (Outliers) ---
    
    # Calculate stats
    mean_rev = df_clean['Revenue'].mean()
    std_rev = df_clean['Revenue'].std()
    threshold = mean_rev + (3 * std_rev)

    print(f"\n--- Tier 2 Analysis ---")
    print(f"Mean Revenue: ${mean_rev:.2f}")
    print(f"Outlier Threshold (3x STD): ${threshold:.2f}")

    # Identify outliers (just for reporting, maybe we don't delete them automatically)
    outliers = df_clean[df_clean['Revenue'] > threshold]
    
    if not outliers.empty:
        print(f"WARNING: Found {len(outliers)} suspiciously high transactions:")
        print(outliers)
    else:
        print("No statistical outliers found.")

    # 4. Export Clean Data
    # For the final file, we might decide to exclude the outliers too, 
    # but for this exercise, we'll save the Tier 1 cleaned data.
    
    output_path = os.path.join(BASE_DIR, OUTPUT_FILE)
    df_clean.to_csv(output_path, index=False)
    
    print(f"\nSuccess! Clean data saved to: {output_path}")
    print(f"Final Row Count: {len(df_clean)}")

if __name__ == "__main__":
    main()
