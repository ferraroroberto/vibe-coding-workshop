import pandas as pd
import os

# --- CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
INPUT_FILE = os.path.join(DATA_DIR, "raw_sales_data.xlsx")
OUTPUT_FILE = os.path.join(DATA_DIR, "polished_report.xlsx")

def main():
    print(f"Reading data from {INPUT_FILE}...")
    df = pd.read_excel(INPUT_FILE)

    print("Creating formatted Excel file...")
    
    # 1. Setup the ExcelWriter with xlsxwriter engine
    writer = pd.ExcelWriter(OUTPUT_FILE, engine='xlsxwriter')
    
    # Convert the dataframe to an XlsxWriter Excel object.
    # We turn off the default header styling so we can apply our own.
    df.to_excel(writer, sheet_name='Sales Report', index=False, startrow=1, header=False)

    # 2. Get the workbook and worksheet objects
    workbook  = writer.book
    worksheet = writer.sheets['Sales Report']

    # 3. Define the formats
    
    # Header Format: Bold, White Text, Blue Background
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#4F81BD', # Corporate Blue
        'font_color': '#FFFFFF',
        'border': 1
    })

    # Money Format
    money_format = workbook.add_format({'num_format': '$#,##0.00'})
    
    # Green Format for high revenue
    green_format = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
    
    # 4. Write the header manually with the format
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    # 5. Auto-fit logic (Approximate)
    for i, col in enumerate(df.columns):
        # find length of column name and max length of data
        column_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
        worksheet.set_column(i, i, column_len)

    # 6. Apply Conditional Formatting
    # We find the column index for 'Revenue'
    revenue_col_idx = df.columns.get_loc('Revenue')
    # Use excel notation (e.g., F2:F21) or (row, col, row, col)
    # We'll use the (first_row, first_col, last_row, last_col) syntax
    # Data starts at row 1 (0-indexed is row 2 in Excel)
    worksheet.conditional_format(1, revenue_col_idx, len(df), revenue_col_idx,
                                 {'type':     'cell',
                                  'criteria': '>',
                                  'value':    10000,
                                  'format':   green_format})

    # Apply money format to the Revenue column (entire column)
    worksheet.set_column(revenue_col_idx, revenue_col_idx, 15, money_format)

    # Save
    writer.close()
    print(f"--> SUCCESS: Polished report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
