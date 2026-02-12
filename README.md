# Python Workshop

A collection of Python exercises and tools designed for learning data manipulation, automation, and best practices in a corporate environment. This workshop focuses on practical skills using libraries like pandas, numpy, matplotlib, and office automation tools.

## Features

- **Library Testing**: Verify installation and basic functionality of required libraries
- **Environment Setup**: Tools for configuring Python environments and pip settings
- **Structured Exercises**: Hands-on learning modules with starter files, solutions, and data
- **Data Reconciliation**: Example exercise demonstrating customer data merging and analysis

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd workshop
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Test the installation:
   ```bash
   python test_libraries.py
   ```

## Project Structure

- `pip_ini_finder.py`: Utility to locate pip configuration files in your environment
- `test_libraries.py`: Script to verify that all required libraries are installed and working
- `requirements.txt`: List of Python packages needed for the workshop
- `exercises/`: Directory containing learning exercises
  - `metaprompt.md`: Template for creating new exercises
  - `data_join/`: Example exercise on customer data reconciliation
    - `exercise_starter.md`: Problem description for students
    - `exercise_solution.md`: Complete solution with explanations
    - `exercise_solution.py`: Python code implementation
    - `exercise_setup_data.py`: Script to generate sample data
    - `data/`: Sample CSV files for the exercise

## Exercises

Exercises follow a structured format:
- **Starter**: Problem description and goals
- **Solution**: Complete code with step-by-step explanations
- **Data**: Sample datasets for hands-on practice

### Current Exercises
- **Customer Data Reconciliation**: Merge CRM and ERP customer datasets, identify duplicates, and analyze differences

## Usage

1. Navigate to an exercise directory (e.g., `exercises/data_join/`)
2. Read the `exercise_starter.md` to understand the problem
3. Implement your solution or review `exercise_solution.py`
4. Run the code to see the results

## Contributing

To add new exercises:
1. Follow the format described in `exercises/metaprompt.md`
2. Create a new directory under `exercises/`
3. Include starter, solution, setup, and data files
4. Update this README with the new exercise description

## Requirements

- Python 3.7+
- Libraries listed in `requirements.txt`:
  - pandas: Data manipulation
  - numpy: Numerical computing
  - matplotlib: Data visualization
  - seaborn: Statistical visualization
  - openpyxl: Excel file handling
  - python-docx: Word document processing
  - python-pptx: PowerPoint processing
  - xlrd/xlwt: Legacy Excel support
  - pywin32: Windows API access

## License

[Add license information if applicable]
