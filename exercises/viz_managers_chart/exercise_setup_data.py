import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

# --- CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

def create_dummy_data():
    """Generates clean sales data for visualization exercises."""
    print("Generating data...")
    
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Setup parameters
    num_rows = 500
    categories = ['Electronics', 'Office Supplies', 'Furniture', 'Software']
    
    products = {
        'Electronics': ['Laptop', 'Monitor', 'Keyboard', 'Mouse', 'Headphones'],
        'Office Supplies': ['Binder', 'Pen Set', 'Desk Organizer', 'Stapler', 'Paper'],
        'Furniture': ['Office Chair', 'Desk', 'Bookshelf', 'File Cabinet', 'Lamp'],
        'Software': ['OS License', 'Antivirus', 'Office Suite', 'Design Tool', 'Cloud Storage']
    }
    
    data = []
    
    start_date = datetime(2026, 1, 1)
    
    for i in range(1, num_rows + 1):
        cat = random.choice(categories)
        prod = random.choice(products[cat])
        
        # Revenue logic (somewhat realistic ranges)
        if cat == 'Electronics':
            rev = random.uniform(200, 2000)
        elif cat == 'Furniture':
            rev = random.uniform(100, 1500)
        elif cat == 'Software':
            rev = random.uniform(50, 500)
        else: # Office Supplies
            rev = random.uniform(10, 100)
            
        date = start_date + timedelta(days=random.randint(0, 364))
        
        row = {
            'Order_ID': f"ORD-{10000+i}",
            'Date': date.strftime('%Y-%m-%d'),
            'Category': cat,
            'Product': prod,
            'Revenue': round(rev, 2),
            'Quantity': random.randint(1, 10)
        }
        data.append(row)
        
    df = pd.DataFrame(data)
    
    output_path = os.path.join(DATA_DIR, "clean_sales_data.csv")
    df.to_csv(output_path, index=False)
    print(f"File created: {output_path}")
    print(f"Rows: {len(df)}")
    print("Columns:", list(df.columns))

if __name__ == "__main__":
    create_dummy_data()
