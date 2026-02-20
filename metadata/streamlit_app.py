import streamlit as st
import pandas as pd
import json

# Page Config
st.set_page_config(page_title="Survey Data Dashboard", layout="wide")

st.markdown("""
<style>
    /* Vertically align tabs with Deploy button */
    .stTabs {margin-top: -64px !important;
</style>
""", unsafe_allow_html=True)


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
    
    # Ensure Phase 2 columns exist with default values
    phase2_columns = ['ind_confirm', 'ide_python', 'ide_sql', 'txt_usecase_data', 
                      'txt_usecase_visual', 'txt_usecase_automate', 'ind_session', 
                      'ind_waitlist', 'ind_facilitate', 'ind_review_phasetwo']
    for col in phase2_columns:
        if col not in df.columns:
            df[col] = 0 if col.startswith('ind_') else ''
    
    # Set default values for ALL indicator columns (replace NULLs with 0)
    default_zero_cols = ['ind_confirm', 'ind_facilitate', 'ind_session', 'ind_waitlist', 'ind_review_phasetwo']
    for col in default_zero_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    st.session_state['df'] = df
else:
    df = st.session_state['df']
    
    # Ensure Phase 2 columns exist with default values (for existing sessions)
    phase2_columns = ['ind_confirm', 'ide_python', 'ide_sql', 'txt_usecase_data', 
                      'txt_usecase_visual', 'txt_usecase_automate', 'ind_session', 
                      'ind_waitlist', 'ind_facilitate', 'ind_review_phasetwo']
    for col in phase2_columns:
        if col not in df.columns:
            df[col] = 0 if col.startswith('ind_') else ''

    # Set default values for ALL indicator columns (replace NULLs with 0)
    default_zero_cols = ['ind_confirm', 'ind_facilitate', 'ind_session', 'ind_waitlist', 'ind_review_phasetwo']
    for col in default_zero_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    st.session_state['df'] = df

# --- Sidebar ---
st.sidebar.title("📊 Survey Data Dashboard")
st.sidebar.markdown("Data entry and visualization")

# Filters
filter_columns = ['nvl_excel', 'nvl_python', 'nvl_sas', 'nvl_sql', 'nvl_vba']
filters = {}
# Add company filter
company_vals = sorted(df['company'].dropna().unique())
company_options = ['All'] + company_vals
company_selected = st.sidebar.multiselect(
    "Filter by Company",
    company_options,
    default=['All'],
    key="company_multiselect"
)
filters['company'] = company_vals if 'All' in company_selected else company_selected
# Add place filter
place_vals = sorted(df['place'].dropna().unique())
place_options = ['All'] + place_vals
place_selected = st.sidebar.multiselect(
    "Filter by Place",
    place_options,
    default=['All'],
    key="place_multiselect"
)

# Add phase one filters
st.sidebar.markdown("---")


filters['place'] = place_vals if 'All' in place_selected else place_selected
# Add ind_review filter
ind_review_vals = sorted(df['ind_review'].dropna().unique())
ind_review_options = ['All'] + list(ind_review_vals)
ind_review_selected = st.sidebar.multiselect(
    "Filter by Ind Review",
    ind_review_options,
    default=['All'],
    key="ind_review_multiselect"
)
filters['ind_review'] = list(ind_review_vals) if 'All' in ind_review_selected else ind_review_selected
# Add ind_select filter
ind_select_vals = sorted(df['ind_select'].dropna().unique())
ind_select_options = ['All'] + list(ind_select_vals)
ind_select_selected = st.sidebar.multiselect(
    "Filter by Ind Select",
    ind_select_options,
    default=['All'],
    key="ind_select_multiselect"
)
filters['ind_select'] = list(ind_select_vals) if 'All' in ind_select_selected else ind_select_selected
# Add ind_1to1 filter
ind_1to1_vals = sorted(df['ind_1to1'].dropna().unique())
ind_1to1_options = ['All'] + list(ind_1to1_vals)
ind_1to1_selected = st.sidebar.multiselect(
    "Filter by Ind 1to1",
    ind_1to1_options,
    default=['All'],
    key="ind_1to1_multiselect"
)
filters['ind_1to1'] = list(ind_1to1_vals) if 'All' in ind_1to1_selected else ind_1to1_selected

# Add phase two filters
st.sidebar.markdown("---")

# Add ind_confirm filter (Phase 2 confirmation)
ind_confirm_vals = sorted(set(int(x) for x in df['ind_confirm'].dropna().unique()))
ind_confirm_options = ['All'] + ind_confirm_vals
ind_confirm_selected = st.sidebar.multiselect(
    "Filter by Confirmed (Phase 2)",
    ind_confirm_options,
    default=['All'],
    key="ind_confirm_multiselect"
)
filters['ind_confirm'] = list(ind_confirm_vals) if 'All' in ind_confirm_selected else ind_confirm_selected

# Add ind_session filter
ind_session_vals = sorted(set(int(x) for x in df['ind_session'].dropna().unique()))
ind_session_options = ['All'] + ind_session_vals
ind_session_selected = st.sidebar.multiselect(
    "Filter by Session Selected",
    ind_session_options,
    default=['All'],
    key="ind_session_multiselect"
)
filters['ind_session'] = list(ind_session_vals) if 'All' in ind_session_selected else ind_session_selected

# Add ind_waitlist filter
ind_waitlist_vals = sorted(set(int(x) for x in df['ind_waitlist'].dropna().unique()))
ind_waitlist_options = ['All'] + ind_waitlist_vals
ind_waitlist_selected = st.sidebar.multiselect(
    "Filter by Waitlist",
    ind_waitlist_options,
    default=['All'],
    key="ind_waitlist_multiselect"
)
filters['ind_waitlist'] = list(ind_waitlist_vals) if 'All' in ind_waitlist_selected else ind_waitlist_selected

# Add ind_review_phasetwo filter
ind_review_phasetwo_vals = sorted(set(int(x) for x in df['ind_review_phasetwo'].dropna().unique()))
ind_review_phasetwo_options = ['All'] + ind_review_phasetwo_vals
ind_review_phasetwo_selected = st.sidebar.multiselect(
    "Filter by Review (Phase 2)",
    ind_review_phasetwo_options,
    default=['All'],
    key="ind_review_phasetwo_multiselect"
)
filters['ind_review_phasetwo'] = list(ind_review_phasetwo_vals) if 'All' in ind_review_phasetwo_selected else ind_review_phasetwo_selected

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
    import data_entry
    df = data_entry.run(df, filters, config)
    st.session_state['df'] = df

with tab2:
    import explore
    explore.run(df, filters, config)

with tab3:
    import data_sync
    data_sync.run(df, filters, config)

with tab4:
    import data_import
    data_import.run(df, filters, config)

with tab5:
    import participation_analysis
    participation_analysis.run(df, filters, config)

with tab6:
    import phase_two_sync
    df = phase_two_sync.run(df, filters, config)
    st.session_state['df'] = df

with tab7:
    import phase_two_entry
    df = phase_two_entry.run(df, filters, config)
    st.session_state['df'] = df

with tab8:
    import selection_management
    df = selection_management.run(df, filters, config)
    st.session_state['df'] = df