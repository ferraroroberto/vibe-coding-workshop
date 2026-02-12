import pandas as pd
import random
from faker import Faker
import os

# --- DOCUMENTATION ---
"""
This script generates a 'messy' dataset simulating an HR export.
It includes:
1. Inconsistent string casing and spacing.
2. Mixed date formats.
3. Free text comments hidden with keywords and emails.
"""

# --- CONFIGURATION ---
FILE_NAME = "hr_survey_raw.csv"
script_dir = os.path.dirname(__file__)
DATA_DIR = os.path.join(script_dir, "data")
ROW_COUNT = 1000

# Setup Faker
fake = Faker()

def generate_messy_gender():
    # A distribution of messy inputs for Gender
    options = [
        'Male', 'male', 'M', 'm', '  Male', 'Male  ',
        'Female', 'female', 'F', 'f', '  Female', 'Fem',
        'Other', 'Unknown', 'N/A'
    ]
    weights = [
        0.3, 0.1, 0.05, 0.05, 0.02, 0.02, # Male variants (~54%)
        0.3, 0.1, 0.05, 0.05, 0.02, 0.02, # Female variants (~50%)
        0.02, 0.02, 0.02                  # Other
    ]
    # Normalize weights to sum to 1
    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]
    
    return random.choices(options, weights=normalized_weights, k=1)[0]

def generate_messy_date(start_date='-5y', end_date='today'):
    # Generate a date object
    dt = fake.date_between(start_date=start_date, end_date=end_date)
    
    # Return it in various string formats randomly
    format_choice = random.choice(['iso', 'us', 'eu', 'text'])
    
    if format_choice == 'iso':
        return dt.isoformat() # 2023-01-25
    elif format_choice == 'us':
        return dt.strftime('%m/%d/%Y') # 01/25/2023
    elif format_choice == 'eu':
        return dt.strftime('%d-%m-%Y') # 25-01-2023
    elif format_choice == 'text':
        return dt.strftime('%d %B, %Y') # 25 January, 2023

def generate_comment_with_hidden_data():
    # 20% chance of mentioning salary
    # 10% chance of including an email
    # 70% generic filler
    
    roll = random.random()
    base_text = fake.sentence(nb_words=10)
    
    if roll < 0.2:
        return f"{base_text} I am worried about my salary and money."
    elif roll < 0.3:
        return f"{base_text} Contact me at {fake.email()} for details."
    else:
        return base_text

def create_dataset():
    data = []
    
    print(f"Generating {ROW_COUNT} rows of messy data...")
    
    for i in range(1, ROW_COUNT + 1):
        row = {
            "Employee_ID": 1000 + i,
            "Name": fake.name(),
            "Gender": generate_messy_gender(),
            "Join_Date": generate_messy_date(),
            "Comments": generate_comment_with_hidden_data(),
            "Satisfaction_Score": random.randint(1, 10)
        }
        data.append(row)
        
    df = pd.DataFrame(data)
    
    # Create directory if not exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    file_path = os.path.join(DATA_DIR, FILE_NAME)
    df.to_csv(file_path, index=False)
    print(f"SUCCESS: Created {file_path}")
    print("Sample of messy data:")
    print(df[['Gender', 'Join_Date']].head(5))

if __name__ == "__main__":
    create_dataset()
