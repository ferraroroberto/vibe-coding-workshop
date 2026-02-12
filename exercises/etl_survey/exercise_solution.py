import pandas as pd
import os

# --- CONFIGURATION ---
script_dir = os.path.dirname(__file__)
INPUT_FILE = os.path.join(script_dir, "data", "hr_survey_raw.csv")
OUTPUT_FILE = os.path.join(script_dir, "data", "hr_survey_clean.csv")

def clean_survey_data():
    # 1. Load Data
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run setup script first.")
        return

    print(f"Loading {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    
    print(f"Original Shape: {df.shape}")
    
    # 2. String Normalization (Gender)
    print("Normalizing Gender column...")
    # Step A: Lowercase and strip whitespace
    df['Gender_Clean'] = df['Gender'].str.lower().str.strip()
    
    # Step B: Map to standard categories
    # We define a map or use replace. Let's use a function or replace for simplicity.
    gender_map = {
        'm': 'Male',
        'male': 'Male',
        'f': 'Female',
        'female': 'Female',
        'fem': 'Female',
        # Any other value will become NaN or stay as is, let's handle 'other'
    }
    # map() is strict (converts non-matches to NaN), replace() is gentle. 
    # Let's use replace for the specific known typos, then fillna 'Other'
    
    df['Gender_Standardized'] = df['Gender_Clean'].map(gender_map).fillna('Other')
    
    # Optimization: Convert to category
    df['Gender_Standardized'] = df['Gender_Standardized'].astype('category')


    # 3. Date Parsing (Join_Date)
    print("Parsing Join_Date...")
    # errors='coerce' turns unparseable dates into NaT (Not a Time)
    df['Join_Date_Clean'] = pd.to_datetime(df['Join_Date'], errors='coerce')


    # 4. Text Analysis (Sentiment/Flagging)
    print("Flagging text issues...")
    # Check for keywords "salary" OR "money" (case insensitive)
    df['Compensation_Flag'] = df['Comments'].str.contains(r'salary|money', case=False, regex=True)


    # 5. Regex Extraction (Emails)
    print("Extracting emails...")
    # Pattern: something @ something . something
    email_pattern = r'([\w\.-]+@[\w\.-]+\.\w+)'
    df['Extracted_Email'] = df['Comments'].str.extract(email_pattern)


    # 6. Review and Save
    print("-" * 30)
    print("Data Cleaning Summary:")
    print(df[['Gender', 'Gender_Standardized', 'Join_Date', 'Join_Date_Clean']].head())
    print("\nRows with Compensation Issues:", df['Compensation_Flag'].sum())
    print("Emails Extracted:", df['Extracted_Email'].notna().sum())
    
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSUCCESS: Saved clean data to {OUTPUT_FILE}")

if __name__ == "__main__":
    clean_survey_data()
