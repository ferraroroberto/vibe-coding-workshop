import pandas as pd
import os
import random
import uuid

# --- CONFIGURATION ---
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
FILE_NAME = "combined_sales.csv"
RECORD_COUNT = 200

# --- DATA GENERATION ---
PRODUCTS = ["Widget A", "Widget B", "Gadget X", "Gadget Y", "SuperTool"]

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def generate_dirty_data():
    data = []
    
    # 1. Generate clean base data
    for _ in range(RECORD_COUNT):
        data.append({
            "Order_ID": str(uuid.uuid4())[:8], # Short random ID
            "Product": random.choice(PRODUCTS),
            "Revenue": round(random.uniform(50.0, 500.0), 2),
            "Date": "2024-01-15"
        })
    
    df = pd.DataFrame(data)
    
    # 2. Inject Duplicates (The "Glitch")
    # Take random 10 rows and append them again to the bottom
    duplicates = df.sample(n=10)
    df = pd.concat([df, duplicates], ignore_index=True)
    print(f"Injected 10 duplicate rows.")

    # 3. Inject Negatives (The "Refund Errors")
    # Select 5 random indices and make revenue negative
    random_indices = random.sample(range(len(df)), 5)
    df.loc[random_indices, 'Revenue'] = df.loc[random_indices, 'Revenue'] * -1
    print(f"Injected 5 negative revenue values.")

    # 4. Inject Outliers (The "Suspiciously High")
    # Select 2 indices and create massive values
    outlier_indices = random.sample(range(len(df)), 2)
    df.loc[outlier_indices, 'Revenue'] = df.loc[outlier_indices, 'Revenue'] * 100
    print(f"Injected 2 suspicious outliers.")

    return df

def main():
    print("--- Setting up Exercise Environment (Detective Mode) ---")
    ensure_directory(BASE_DIR)
    
    df = generate_dirty_data()
    
    output_path = os.path.join(BASE_DIR, FILE_NAME)
    df.to_csv(output_path, index=False)
    
    print(f"Created '{output_path}' with {len(df)} rows.")
    print("Setup Complete. You are ready to clean!")

if __name__ == "__main__":
    main()
