import streamlit as st
import pandas as pd
import json
import data_entry
import explore
import data_sync
import data_import
import participation_analysis
import phase_two_sync
import phase_two_entry
import selection_management

# Page Config
st.set_page_config(page_title="Survey Data Dashboard", layout="wide")

st.markdown("""
<style>
    /* Vertically align tabs with Deploy button */
    .stTabs { margin-top: -64px !important; }
</style>
""", unsafe_allow_html=True)


def ensure_phase2_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure Phase 2 columns exist with correct types. Idempotent."""
    phase2_columns = ['ind_confirm', 'ide_python', 'ide_sql', 'txt_usecase_data',
                      'txt_usecase_visual', 'txt_usecase_automate', 'ind_session',
                      'ind_waitlist', 'ind_facilitate', 'ind_review_phasetwo']
    for col in phase2_columns:
        if col not in df.columns:
            df[col] = 0 if col.startswith('ind_') else ''

    default_zero_cols = ['ind_confirm', 'ind_facilitate', 'ind_session', 'ind_waitlist', 'ind_review_phasetwo']
    for col in default_zero_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    return df


# Load config
with open('config.json') as f:
    config = json.load(f)

excel_path = config['excel_path']
sheet = config['excel_interpreter_spec']['sheet_name']

# Load dataframe - preserve column order from config
usecols = [col['column'] for col in config['excel_interpreter_spec']['columns']]

# Load dataframe from session state or Excel
if 'df' not in st.session_state:
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet, header=None, usecols=usecols, skiprows=1, engine='openpyxl')
        df.columns = [str(i) for i in usecols]
    except FileNotFoundError:
        st.error(f"Excel file not found at {excel_path}. Please check the path in config.json.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        st.stop()

    # Map columns based on config
    for col_spec in config['excel_interpreter_spec']['columns']:
        if col_spec['column_id'] != 'skip':
            column_idx = str(col_spec['column'])
            if column_idx in df.columns:
                df[col_spec['column_id']] = df[column_idx]

    # Keep only the mapped columns
    mapped_columns = [col_spec['column_id'] for col_spec in config['excel_interpreter_spec']['columns'] if col_spec['column_id'] != 'skip']
    df = df[mapped_columns]

    df = ensure_phase2_columns(df)
    st.session_state['df'] = df
else:
    df = ensure_phase2_columns(st.session_state['df'])
    st.session_state['df'] = df

# --- Sidebar ---
st.sidebar.title("📊 Survey Data Dashboard")
st.sidebar.markdown("Data entry and visualization")

# Filters
filter_columns = ['nvl_excel', 'nvl_python', 'nvl_sas', 'nvl_sql', 'nvl_vba']
filters = {}
# Identity / phase-one / phase-two multiselect filters, described as data.
# Each spec is (column, label, coerce_int); groups are rendered with a
# sidebar divider between them, matching the original sidebar layout.
# coerce_int=True maps the phase-2 ind_* values to int before sorting.
sidebar_filter_groups = [
    [
        ('company', "Filter by Company", False),
        ('place', "Filter by Place", False),
    ],
    [
        ('ind_review', "Filter by Ind Review", False),
        ('ind_select', "Filter by Ind Select", False),
        ('ind_1to1', "Filter by Ind 1to1", False),
    ],
    [
        ('ind_confirm', "Filter by Confirmed (Phase 2)", True),
        ('ind_session', "Filter by Session Selected", True),
        ('ind_waitlist', "Filter by Waitlist", True),
        ('ind_review_phasetwo', "Filter by Review (Phase 2)", True),
    ],
]

for group_idx, group in enumerate(sidebar_filter_groups):
    if group_idx > 0:
        st.sidebar.markdown("---")
    for col, label, coerce_int in group:
        if coerce_int:
            unique_vals = sorted(set(int(x) for x in df[col].dropna().unique()))
        else:
            unique_vals = sorted(df[col].dropna().unique())
        options = ['All'] + unique_vals
        selected = st.sidebar.multiselect(
            label,
            options,
            default=['All'],
            key=f"{col}_multiselect"
        )
        if 'All' in selected:
            filters[col] = unique_vals
        else:
            filters[col] = selected

st.sidebar.markdown("---")

for col in filter_columns:
    unique_vals = sorted(df[col].dropna().unique())
    options = ['All'] + unique_vals
    selected = st.sidebar.multiselect(
        f"Filter by {col.replace('nvl_', '').replace('_', ' ').title()}",
        options,
        default=['All'],
        key=f"{col}_multiselect"
    )
    if 'All' in selected:
        filters[col] = unique_vals
    else:
        filters[col] = selected

# Add hierarchy filters
st.sidebar.markdown("---")

# Additional filters
additional_filter_columns = ['des_red', 'des_dt', 'des_dg', 'des_dan','des_centro_ges' ]
for col in additional_filter_columns:
    unique_vals = sorted(df[col].dropna().unique())
    options = ['All'] + unique_vals
    selected = st.sidebar.multiselect(
        f"Filter by {col.replace('_', ' ').title()}",
        options,
        default=['All'],
        key=f"{col}_multiselect"
    )
    if 'All' in selected:
        filters[col] = unique_vals
    else:
        filters[col] = selected

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Data entry", "Explore", "Data Sync", "Data Import", "Participation Analysis",
    "Phase 2 Sync", "Phase 2 Entry", "Selection Management"
])

with tab1:
    df = data_entry.run(df, filters, config)
    st.session_state['df'] = df

with tab2:
    explore.run(df, filters, config)

with tab3:
    data_sync.run(df, filters, config)

with tab4:
    data_import.run(df, filters, config)

with tab5:
    participation_analysis.run(df, filters, config)

with tab6:
    df = phase_two_sync.run(df, filters, config)
    st.session_state['df'] = df

with tab7:
    df = phase_two_entry.run(df, filters, config)
    st.session_state['df'] = df

with tab8:
    df = selection_management.run(df, filters, config)
    st.session_state['df'] = df