# Solution: The File Organizer

## Title & Problem Statement

**Title:** The File Organizer: Cleaning Up Your Workspace
**Context:** Manually sorting files is tedious and prone to error. In this exercise, you will build a script that acts as your personal digital assistant, sweeping through a cluttered folder and filing everything into the correct location instantly. This is a fundamental automation task that saves hours over time.

## Difficulty & Estimated Time

*   **Difficulty:** Beginner
*   **Time:** 25 Minutes

## Required Libraries

*   `os`: For interacting with the operating system (listing files, creating directories).
*   `shutil`: High-level file operations (moving files).
*   *Note: Both are standard Python libraries, so no installation is required.*

## Didactic Step-by-Step

1.  **Define the Scope:** We need to know *where* to look (source directory) and *where* to put things (destination categories).
2.  **Scan the Directory:** We use `os.listdir()` or `os.scandir()` to get a list of all items in the folder.
3.  **Filter for Files:** We need to ignore directories (we don't want to move a folder inside another folder recursively for this basic exercise).
4.  **Determine File Type:** We extract the file extension (e.g., `.pdf`) using `os.path.splitext()`.
5.  **Map to Category:** We check which category that extension belongs to (e.g., `.pdf` -> `Documents`).
6.  **Create Destination:** Before moving, we ensure the destination folder exists using `os.makedirs(exist_ok=True)`.
7.  **Move the File:** We use `shutil.move()` to physically relocate the file.

## Tips for Coding and "Vibe-Coding"

1.  **Safety First:** Always use `shutil.move` carefully. If a file with the same name exists in the destination, it might be overwritten depending on the implementation.
2.  **Path Handling:** Use `os.path.join()` to construct paths. It handles the slash differences between Windows (`\`) and Mac/Linux (`/`) automatically.
3.  **Case Insensitivity:** File extensions can be `.CSV` or `.csv`. Convert extensions to lowercase (`.lower()`) before comparing.
4.  **The "Dry Run":** When building automation that deletes or moves files, add a `print()` statement instead of the actual `shutil.move()` first to see what *would* happen.
5.  **Extension Mapping:** A dictionary is the perfect data structure to map extensions to folder names (e.g., `{'png': 'Images', 'jpg': 'Images'}`).

## Copilot Master Prompt

You can use this prompt in Microsoft Copilot to generate a similar solution:

> "Write a Python script to organize files in a specific directory.
> I have a folder with mixed file types (.csv, .xlsx, .pdf, .txt, .jpg).
> Please create a script that:
> 1. Scans the 'data' folder.
> 2. Creates subfolders named 'Spreadsheets', 'Documents', and 'Images' if they don't exist.
> 3. Moves the files into these subfolders based on their extension.
> 4. Prints a summary of how many files were moved."

