# VibeCoding Survey Data Dashboard

## Overview
VibeCoding is a Streamlit-based dashboard for visualizing and analyzing survey data about skill levels, use cases, and organizational breakdowns. It is designed for non-technical users and runs as a Streamlit web app.

## Features
- Interactive filters by company, place, and skill levels
- Pie charts and bar charts for data breakdowns
- Heatmap visualization of skill distributions
- Export filtered results to Excel
- Data entry with calendar selector for timestamp fields (robust datetime handling)
- Immediate DataFrame reload after add/edit/delete (no manual refresh needed)
- New/empty records always visible, even if some columns are missing
- All changes synced with Streamlit session state for a smoother user experience
- ArrowTypeError fix for timestamp fields
- **Data Import**: Enrich survey data with employee and work center information from CSV files
- **Participation Analysis**: Visualize survey participation rates across organizational hierarchy using treemaps

## Data Import & Participation Analysis

### Data Import
The Data Import feature enriches the survey data with organizational information:
- **Source Files**: Loads employee data (`DC_TD_EMPLEADOS_PH.csv`) and work center hierarchy (`CTM_TM_CENTROS_JER.csv`)
- **Matching Process**: Matches survey responses with employee records using concatenated names (first name + last name1 + last name2)
- **Data Enrichment**: Adds work center information including DAN (N+1), DG (N+2), DT (N+3), and RED hierarchy levels
- **Validation**: Shows preview with duplicate detection and allows confirmation before saving to Excel
- **Atomic Writes**: Uses temporary files for safe Excel updates

### Participation Analysis
The Participation Analysis feature provides hierarchical insights into survey adoption:
- **Data Sources**: Uses enriched survey data and full employee database
- **Hierarchy Levels**: Analyzes participation across DAN (N+1), DG (N+2), DT (N+3), and RED levels
- **Visualization**: Treemaps where box size represents total employees and color intensity shows participation rate
- **Filtering**: Applies the same sidebar filters as other tabs, showing participation only for filtered survey responses
- **Metrics**: Displays overall participation rates and top areas by participation rate and absolute numbers
- **Color Scheme**: Top performing area in blue (#1E88E5), others in grey shades

## Requirements
- Windows 10 or later
- Python 3.11 or later
- Streamlit and required Python packages (see `requirements.txt`)
- The following files must be present in the same folder as the script:
   - `config.json` (configuration file)
   - `Te interesa aprender Python.xlsx` (Excel data file)
   - `DC_TD_EMPLEADOS_PH.csv` (employee data for Data Import - semicolon separated)
   - `CTM_TM_CENTROS_JER.csv` (work center hierarchy for Data Import - comma separated)

## Installation & Usage
1. **Clone the repo** (all required files are in the `metadata/` folder — no separate download step needed):
   - `metadata/streamlit_app.py` — main dashboard app
   - `metadata/config.json` — column and path configuration
   - `metadata/Te interesa aprender Python.xlsx` — survey data file
2. **Install dependencies** from the `metadata/` folder:
   ```powershell
   pip install -r requirements.txt
   ```
3. **Run the app with Streamlit** from the `metadata/` folder:
   ```powershell
   streamlit run streamlit_app.py
   ```
   - The app will open in your default web browser.

## How to Run (for developers)
If you want to run or modify the app:
1. Install Python 3.11 and all dependencies (see `requirements.txt`).
2. Run the app with Streamlit as shown above.

## Project Structure

### Shared helpers (introduced in dedup refactor)
- `excel_io.py` — Atomic Excel write helper (`save_dataframe_to_excel`): owns column-mapping, id-column lookup, and safe temp-file replace; all tab modules import from here
- `fuzzy_search.py` — Shared fuzzy-name filter (`fuzzy_filter_by_name`) using `fuzzywuzzy.process`; used by data-entry and phase-two-entry tabs
- `charts.py` — Reusable chart builders (`build_breakdown_pie`, `grey_ramp`); used by explore and participation-analysis tabs
- `sync_rules.py` — Shared sync-rule transformations (`apply_replicate_rules`, `apply_binary_checks`); used by data-sync and phase-two-sync tabs

### Tab modules
- `streamlit_app.py` — Main dashboard app
- `config.json` — Configuration for columns and Excel path
- `Te interesa aprender Python.xlsx` — Survey data
- `requirements.txt` — Python dependencies
- `data_entry.py` — Data entry module with calendar selectors
- `phase_two_entry.py` — Phase-two data entry
- `explore.py` — Data exploration with charts and filters
- `data_sync.py` — Data synchronization utilities
- `phase_two_sync.py` — Phase-two synchronization utilities
- `data_import.py` — Data enrichment with employee and work center information
- `selection_management.py` — Selection management tab
- `participation_analysis.py` — Participation analysis with treemap visualizations

## Notes
- The Excel file path in `config.json` must match the actual file location or be placed in the same folder as the script.
- For best results, keep all files together when sharing.
- **Configuration uses numeric column indexes**: The `config.json` file uses zero-based numeric indexes (0, 1, 2...) instead of Excel letter-based column references (A, B, C...) for improved clarity and consistency with standard programming conventions.

## License
MIT License

---
For questions or support, contact the project maintainer.