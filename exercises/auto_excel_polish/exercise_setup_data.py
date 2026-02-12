import pandas as pd
import os
import numpy as np

# --- CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "raw_sales_data.xlsx")

def setup_data():
    """Generates a dummy sales dataset for the exercise."""
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created directory: {DATA_DIR}")

    print("Generating dummy data...")
    
    # Create dummy data
    data = {
        'Order_Date': pd.date_range(start='2023-01-01', periods=20, freq='W'),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 20),
        'Product': np.random.choice(['Widget A', 'Gadget B', 'Thingamajig C', 'Doohickey D'], 20),
        'Sales_Rep': np.random.choice(['Alice', 'Bob', 'Charlie', 'Dana'], 20),
        'Units': np.random.randint(1, 50, 20),
        'Unit_Price': np.random.choice([10.5, 25.0, 50.0, 99.99], 20),
    }
    
    df = pd.DataFrame(data)
    
    # Calculate Revenue (and make some high for the conditional formatting)
    df['Revenue'] = df['Units'] * df['Unit_Price']
    
    # Intentionally manipulate a few to be high performers (> 10,000 is the target, so let's scale up)
    # The random numbers above usually result in lower values, let's force some big ones.
    df.loc[0, 'Revenue'] = 12500
    df.loc[5, 'Revenue'] = 15000
    df.loc[10, 'Revenue'] = 10500
    
    # Save to Excel (Plain, no formatting)
    df.to_excel(OUTPUT_FILE, index=False)
    
    print(f"--> SUCCESS: Created raw data file at: {OUTPUT_FILE}")
    print("--> You are ready to start the exercise!")

if __name__ == "__main__":
    setup_data()
