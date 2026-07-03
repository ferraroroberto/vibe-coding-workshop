# VibeCoding Survey Data Dashboard

## Overview
VibeCoding is a Streamlit-based dashboard for visualizing and analyzing survey data about skill levels, use cases, and organizational breakdowns. It is designed for non-technical users and runs as a Streamlit web app.

The app spans two phases of a community selection workflow. **Phase 1** covers survey entry, data import, enrichment, exploration, and participation analysis. **Phase 2** adds candidate selection management: syncing Phase 2 form responses, editing per-person flags with a team-balance view, and managing bulk selection and waitlist decisions for the final cohort.

## Features
- Interactive filters by company, place, and skill levels
- Pie charts and bar charts for data breakdowns
- Heatmap visualization of skill distributions
- Export filtered results to Excel
- Data entry with calendar selector for timestamp fields (robust datetime handling)
- **Data Import**: Enrich survey data with employee and work center information from CSV files
- **Participation Analysis**: Visualize survey participation rates across organizational hierarchy using treemaps
- **Phase 2 Sync**: Ingest Phase 2 form responses and fuzzy-match them to existing Phase 1 records, with preview and conflict detection before saving
- **Phase 2 Entry**: Review and edit per-person Phase 2 flags (`ind_session`, `ind_waitlist`) alongside a live team-balance view and selection-decision table
- **Selection Management**: Bulk review all Phase 2 candidates (`ind_confirm = 1`), mark selected or waitlisted, inspect team balance across hierarchy levels, and export the final selection report

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
- **Hierarchy Levels**: Analyzes participation across DAN (N+1), DG (N+2), and DT (N+3) levels
- **Visualization**: Treemaps where box size represents total employees and color intensity shows participation rate
- **Filtering**: Applies the same sidebar filters as other tabs, showing participation only for filtered survey responses
- **Metrics**: Displays overall participation rates and top areas by participation rate and absolute numbers
- **Color Scheme**: Top performing area in blue (#1E88E5), others in grey shades

## Requirements
- Windows 10 or later
- Python 3.11 or later
- Streamlit and required Python packages (see root `requirements.txt`)
- `config.sample.json` (tracked config template) — copy it to `config.json` (gitignored, per-machine) and set your data-file paths before running; see "Private data inputs" below
- **Private data inputs — not included in this repo.** The workbook and CSVs below contain real survey/employee data and are never committed. You must obtain them separately from the data owner and tell `config.json` where they live (see "Private data inputs" below):
   - `python_community.xlsx` (Excel data file — path configured via `excel_path` in `config.json`)
   - `DC_TD_EMPLEADOS_PH.csv` (employee data for Data Import, semicolon separated — path via `source_path_employees` in `config.json`)
   - `CTM_TM_CENTROS_JER.csv` (work center hierarchy for Data Import, comma separated — path via `source_path_workcenters` in `config.json`)
   - The Phase 1 / Phase 2 form-response workbooks (`source_path`, `phase_two_path` in `config.json`)

## Private data inputs

The repo tracks **`config.sample.json`** — a portable template whose `excel_path`, `source_path`, `phase_two_path`, and `source_path_employees` / `source_path_workcenters` paths are **relative defaults** (bare filenames / `.`, i.e. "files sit next to the app"), never anyone's absolute machine path. The app resolves its config at runtime as: use `config.json` if it exists, otherwise fall back to `config.sample.json`.

**`config.json` is your per-machine override and is gitignored** — it never gets committed, so your personal paths can't leak back into the repo (and schema/column changes still live in the tracked `config.sample.json`). To run against your own data, copy the template and edit it:

```powershell
copy config.sample.json config.json
```

Then set the path fields in `config.json` one of two ways:

1. **Place the files beside the app and keep the relative filenames.** Copy your private workbook/CSVs into the `metadata/` folder (next to `streamlit_app.py`); the sample's default filenames then already resolve, so no edit is needed.
2. **Keep the files wherever they already live.** Edit the path fields in `config.json` to the files' real absolute location on your machine.

A fresh clone still runs with no `config.json` at all (it falls back to `config.sample.json`) — it just needs the private data files placed beside the app to load anything real.

## Installation & Usage
1. **Clone the repo.** `metadata/streamlit_app.py` and `metadata/config.sample.json` are included; `config.json` (your per-machine copy) and the private workbook/CSVs are not — see "Private data inputs" above.
2. **Install dependencies** from the repo root:
   ```powershell
   pip install -r requirements.txt
   ```
3. **Copy `config.sample.json` to `config.json` and point it at your private data files** as described above.
4. **Run the app with Streamlit** from the `metadata/` folder:
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
- `config.sample.json` — Tracked config template (columns + portable relative default paths); copy to `config.json` (gitignored per-machine override) and set `excel_path` etc. to your actual file locations — see "Private data inputs" above
- `python_community.xlsx` — Survey data workbook; **not tracked in this repo** (filename/location set via `excel_path` in `config.json`, see "Private data inputs" above)
- `data_entry.py` — Data entry module with calendar selectors
- `phase_two_entry.py` — Phase-two data entry
- `explore.py` — Data exploration with charts and filters
- `data_sync.py` — Data synchronization utilities
- `phase_two_sync.py` — Phase-two synchronization utilities
- `data_import.py` — Data enrichment with employee and work center information
- `selection_management.py` — Selection management tab
- `participation_analysis.py` — Participation analysis with treemap visualizations

## Notes
- The workbook/CSV inputs are private and not tracked in this repo — see "Private data inputs" above for how to point `config.json` at your own copies.
- The Excel file path in `config.json` must match the actual file location or be placed in the same folder as the script.
- For best results, keep all files together when sharing.
- **Configuration uses numeric column indexes**: The `config.json` file uses zero-based numeric indexes (0, 1, 2...) instead of Excel letter-based column references (A, B, C...) for improved clarity and consistency with standard programming conventions.

## License
MIT License

---
For questions or support, contact the project maintainer.