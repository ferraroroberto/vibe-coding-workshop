import os
import shutil

# --- CONFIGURATION ---
# We use the current script's location to find the 'data' folder
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, "data")

# Construct absolute paths for our organization categories
# We define where each type of file should go
DIRECTORIES = {
    "Spreadsheets": [".csv", ".xlsx", ".xls"],
    "Documents": [".pdf", ".docx", ".txt", ".md"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Archives": [".zip", ".tar", ".rar"]
}

def organize_files():
    """Scans the data directory and moves files into subfolders."""
    
    # 1. Verify the data directory exists
    if not os.path.exists(DATA_DIR):
        print(f"Error: The folder '{DATA_DIR}' does not exist. Please run the setup script first.")
        return

    print(f"Scanning folder: {DATA_DIR}...\n")

    # 2. List all files in the directory
    # os.listdir includes files and folders, so we need to filter
    items = os.listdir(DATA_DIR)

    files_moved = 0

    for item in items:
        source_path = os.path.join(DATA_DIR, item)

        # Skip if it is a directory (we don't want to move folders)
        if os.path.isdir(source_path):
            continue

        # 3. Determine file extension
        # os.path.splitext returns a tuple: ('filename', '.ext')
        _, extension = os.path.splitext(item)
        extension = extension.lower() # Normalize to lowercase for comparison

        # 4. Find the matching category
        target_folder_name = "Others" # Default folder
        
        for folder, extensions_list in DIRECTORIES.items():
            if extension in extensions_list:
                target_folder_name = folder
                break
        
        # 5. Create the destination path
        target_folder_path = os.path.join(DATA_DIR, target_folder_name)
        
        # Create folder if it doesn't exist
        os.makedirs(target_folder_path, exist_ok=True)

        # 6. Move the file
        destination_path = os.path.join(target_folder_path, item)
        
        try:
            shutil.move(source_path, destination_path)
            print(f"Moved: {item} -> {target_folder_name}/")
            files_moved += 1
        except Exception as e:
            print(f"Error moving {item}: {e}")

    print(f"\nSuccess! Organized {files_moved} files.")

if __name__ == "__main__":
    organize_files()
