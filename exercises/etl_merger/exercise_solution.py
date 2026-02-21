import pandas as pd
import os

# --- CONFIGURATION ---
# Path where the input files are located (must match setup script)
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Names of the files to process
FILES = ["sales_q1.xlsx", "sales_q2.xlsx", "sales_q3.xlsx"]
OUTPUT_FILE = "solutions/combined_sales.csv"


# Ensure solutions directory exists
os.makedirs(os.path.join(BASE_DIR, 'solutions'), exist_ok=True)

def main():
    print("--- Starting ETL Process: The Great Merger ---")
    
    # 1. Define the full paths
    file_paths = [os.path.join(BASE_DIR, f) for f in FILES]
    
    # List to hold our dataframes
    all_dataframes = []

    # 2. Load the files
    for path in file_paths:
        if os.path.exists(path):
            print(f"Loading: {path}")
            df = pd.read_excel(path)
            
            # --- OPTIONAL: TIER 2 (Source Tracking) ---
            # Extract just the filename to tag the data
            filename = os.path.basename(path)
            df['Source_File'] = filename
            # ------------------------------------------
            
            all_dataframes.append(df)
        else:
            print(f"Error: File not found at {path}")
            return

    # 3. Merge (Concatenate)
    print("Merging data...")
    if all_dataframes:
        master_df = pd.concat(all_dataframes, ignore_index=True)
    else:
        print("No data loaded.")
        return

    # 4. Check results
    print(f"Total rows loaded: {len(master_df)}")
    print("Sample data:")
    print(master_df.head())

    # 5. Export
    output_path = os.path.join(BASE_DIR, OUTPUT_FILE)
    master_df.to_csv(output_path, index=False)
    print(f"Success! Combined file saved to: {output_path}")

if __name__ == "__main__":
    main()

# --- ALTERNATIVE: TIER 2 (The Glob Pattern) ---
# simpler version for handling many files:
# 
# import glob
# all_files = glob.glob(os.path.join(BASE_DIR, "*.xlsx"))
# df_list = [pd.read_excel(f) for f in all_files]
# final_df = pd.concat(df_list, ignore_index=True)
