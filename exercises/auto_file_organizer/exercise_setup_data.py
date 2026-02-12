import os
import random
import pandas as pd

# --- CONFIGURATION ---
# Define the root directory for the exercise
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")

def create_environment():
    """Sets up the messy folder with various file types."""
    
    # 1. Ensure the data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created directory: {DATA_DIR}")
    else:
        print(f"Directory already exists: {DATA_DIR}")

    # 2. List of dummy files to create
    files_to_create = [
        ("report_q1.xlsx", "excel"),
        ("report_q2.xlsx", "excel"),
        ("financials_2023.csv", "csv"),
        ("employee_list.csv", "csv"),
        ("meeting_notes_jan.txt", "text"),
        ("project_plan.docx", "text"), # Just a dummy text file with docx extension
        ("invoice_101.pdf", "text"),   # Just a dummy text file with pdf extension
        ("invoice_102.pdf", "text"),
        ("logo_v1.png", "text"),       # Just a dummy text file
        ("banner.jpg", "text"),
        ("unknown_file.xyz", "text"),
        ("notes.md", "text")
    ]

    print("Generating files...")

    for filename, type_ in files_to_create:
        file_path = os.path.join(DATA_DIR, filename)
        
        # Don't overwrite if exists, just to be safe, or do? 
        # For setup scripts, overwriting is usually better to ensure clean state.
        
        if type_ == "excel":
            # Create a simple Excel file
            df = pd.DataFrame({'Data': [random.randint(1, 100) for _ in range(5)]})
            try:
                df.to_excel(file_path, index=False)
            except ImportError:
                 # Fallback if openpyxl/pandas generic issue
                 with open(file_path, 'w') as f:
                    f.write("Dummy Excel Content")
        
        elif type_ == "csv":
            # Create a simple CSV
            df = pd.DataFrame({'Data': [random.randint(1, 100) for _ in range(5)]})
            df.to_csv(file_path, index=False)
            
        else:
            # Create a text-based dummy file for other extensions
            with open(file_path, 'w') as f:
                f.write(f"This is a dummy file for testing: {filename}")
        
        print(f" - Created: {filename}")

    print("\nSetup complete! Your messy 'data' folder is ready for organization.")

if __name__ == "__main__":
    create_environment()
