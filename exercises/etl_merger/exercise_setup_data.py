import pandas as pd
import os
import random
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# Default folder as requested. 
# Students/Users can change this to "." to generate in the current folder.
# BASE_DIR = 'data'  # Not used anymore, using script directory

# --- DATA GENERATION CONFIG ---
PRODUCTS = ["Widget A", "Widget B", "Gadget X", "Gadget Y", "SuperTool"]
START_DATE = datetime(2026, 1, 1)
RECORDS_PER_FILE = 50

def ensure_directory(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Created directory: {path}")
        except Exception as e:
            print(f"Error creating directory {path}: {e}")
            # Fallback to current directory if permission denied
            return "." 
    return path

def generate_sales_data(quarter_offset):
    data = []
    # Calculate start month based on quarter (0=Jan, 3=Apr, 6=Jul)
    start_month_offset = quarter_offset * 3
    
    for _ in range(RECORDS_PER_FILE):
        # Random date within the quarter (~90 days)
        day_offset = random.randint(0, 90)
        date_val = START_DATE + timedelta(days=(start_month_offset * 30) + day_offset)
        
        product = random.choice(PRODUCTS)
        revenue = round(random.uniform(100.0, 5000.0), 2)
        
        data.append({
            "Date": date_val.strftime("%Y-%m-%d"),
            "Product": product,
            "Revenue": revenue
        })
    return pd.DataFrame(data)

def main():
    print("--- Setting up Exercise Environment ---")
    
    # Setup directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    actual_dir = data_dir
    
    # Generate 3 files
    quarters = [
        ("sales_q1.xlsx", 0),
        ("sales_q2.xlsx", 1),
        ("sales_q3.xlsx", 2)
    ]
    
    for filename, q_offset in quarters:
        print(f"Generating {filename}...")
        df = generate_sales_data(q_offset)
        file_path = os.path.join(actual_dir, filename)
        df.to_excel(file_path, index=False)
        print(f"Saved: {file_path}")

    print("\n--- Setup Complete ---")
    print(f"Files are ready in: {actual_dir}")
    print("You can now proceed with the exercise.")

if __name__ == "__main__":
    main()
