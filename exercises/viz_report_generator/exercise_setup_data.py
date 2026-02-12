import pandas as pd
import numpy as np
import os
import random

# --- CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
FILE_NAME = "clean_sales_data.csv"

# --- DATA GENERATION ---
def create_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    print(f"Generating data in {DATA_DIR}...")
    
    categories = ['Electronics', 'Furniture', 'Office Supplies', 'Software']
    products = {
        'Electronics': ['Laptop', 'Monitor', 'Mouse', 'Keyboard'],
        'Furniture': ['Chair', 'Desk', 'Lamp', 'Shelf'],
        'Office Supplies': ['Pen', 'Paper', 'Binder', 'Stapler'],
        'Software': ['OS License', 'Antivirus', 'Office Suite', 'Cloud Storage']
    }
    
    rows = []
    dates = pd.date_range(start='2024-01-01', end='2024-03-31', freq='D')
    
    # Generate 500 rows of sales data
    for _ in range(500):
        category = random.choice(categories)
        product = random.choice(products[category])
        date = random.choice(dates.tolist())
        revenue = round(random.uniform(50.0, 2000.0), 2)
        quantity = random.randint(1, 10)
        
        rows.append({
            "Date": date,
            "Category": category,
            "Product": product,
            "Revenue": revenue,
            "Quantity": quantity
        })
        
    df = pd.DataFrame(rows)
    
    # Save file
    file_path = os.path.join(DATA_DIR, FILE_NAME)
    df.to_csv(file_path, index=False)
    print(f"Success! Created {FILE_NAME} at {file_path}")

if __name__ == "__main__":
    create_data()
