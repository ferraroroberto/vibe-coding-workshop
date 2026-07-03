import streamlit as st
import json
import os
import data_entry
import explore
import data_sync
import data_import
import participation_analysis
import phase_two_sync
import phase_two_entry
import selection_management

from excel_io import load_mapped_dataframe, ensure_phase2_columns

# Page Config
st.set_page_config(page_title="Survey Data Dashboard", layout="wide")

st.markdown("""
<style>
    /* Vertically align tabs with Deploy button */
    .stTabs { margin-top: -64px !important; }
</style>
""", unsafe_allow_html=True)


# Load config. `config.json` is the per-machine override (gitignored, holds
# real data-file paths); it falls back to the tracked `config.sample.json`
# template so a fresh clone runs without editing committed files. Paths in the
# sample are portable relative defaults (files placed beside this app).
_config_file = 'config.json' if os.path.exists('config.json') else 'config.sample.json'
with open(_config_file) as f:
    config = json.load(f)

# Load dataframe from session state or Excel (column order preserved by the
# loader). Data logic lives in excel_io; this file only wires UI and feedback.
if 'df' not in st.session_state:
    try:
        df = load_mapped_dataframe(config)
    except FileNotFoundError:
        st.error(f"Excel file not found at {config['excel_path']}. Please check the path in config.json.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        st.stop()

    df = ensure_phase2_columns(df)
    st.session_state['df'] = df
else:
    df = ensure_phase2_columns(st.session_state['df'])
    st.session_state['df'] = df

# --- Sidebar ---
st.sidebar.title("📊 Survey Data Dashboard")
st.sidebar.markdown("Data entry and visualization")

# Filters
filters = {}
# Every sidebar multiselect, described as data: each spec is
# (column, label, coerce_int). Groups render with a sidebar divider between
# them, matching the original layout. coerce_int=True maps the phase-2 ind_*
# values to int before sorting. Labels that the old code derived from the
# column name (the nvl_* skills and des_* hierarchy groups) are spelled out
# here so the rendered text stays byte-identical.
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
    [
        ('nvl_excel', "Filter by Excel", False),
        ('nvl_python', "Filter by Python", False),
        ('nvl_sas', "Filter by Sas", False),
        ('nvl_sql', "Filter by Sql", False),
        ('nvl_vba', "Filter by Vba", False),
    ],
    [
        ('des_red', "Filter by Des Red", False),
        ('des_dt', "Filter by Des Dt", False),
        ('des_dg', "Filter by Des Dg", False),
        ('des_dan', "Filter by Des Dan", False),
        ('des_centro_ges', "Filter by Des Centro Ges", False),
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