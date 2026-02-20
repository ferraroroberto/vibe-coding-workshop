import streamlit as st
import pandas as pd
import logging
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

logger = logging.getLogger(__name__)


# Phase 2 specific fields
PHASE2_INDICATOR_FIELDS = ['ind_confirm', 'ind_session', 'ind_waitlist', 'ind_facilitate', 'ind_review_phasetwo']
PHASE2_TEXT_FIELDS = ['ide_python', 'ide_sql', 'txt_usecase_data', 'txt_usecase_visual', 'txt_usecase_automate']
PHASE1_INDICATOR_FIELDS = ['ind_select', 'ind_review', 'ind_1to1', 'ind_share', 'ind_self']


def run(df, filters, config):
    """
    Phase 2 Entry Module: Edit Phase 2 records with team balance view.
    
    Features:
    1. Show all Phase 1 + Phase 2 fields for a person
    2. Edit ind_session, ind_waitlist flags
    3. Team balance view (count people from same team/center)
    4. Selection decision table (same team with ind_confirm = 1)
    """
    st.header("📝 Phase 2 Record Entry")
    st.markdown("View and edit Phase 2 records with team context")
    
    # Clean up state when switching contexts
    if 'last_tab' not in st.session_state:
        st.session_state['last_tab'] = 'phase_two_entry'
    if st.session_state.get('last_tab') != 'phase_two_entry':
        st.session_state.pop('phase2_selected_id', None)
        st.session_state['last_tab'] = 'phase_two_entry'
    
    # Apply filters
    filtered_df = df.copy()
    for col, selected in filters.items():
        if selected and col in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[col].isin(selected) | filtered_df[col].isna()]
    
    # Search bar
    search_term = st.text_input("Search by name (fuzzy)", "", key="phase2_search")
    
    # Fuzzy search
    if search_term:
        names = filtered_df['name'].dropna().tolist()
        matches = process.extract(search_term, names, scorer=fuzz.partial_ratio, limit=None)
        good_matches = [(match[0], match[1]) for match in matches if match[1] >= 70]
        if good_matches:
            good_matches.sort(key=lambda x: x[1], reverse=True)
            matched_names = [name for name, score in good_matches]
            filtered_df = filtered_df[filtered_df['name'].isin(matched_names)]
            name_to_order = {name: i for i, (name, _) in enumerate(good_matches)}
            filtered_df = filtered_df.assign(match_order=filtered_df['name'].map(name_to_order)).sort_values('match_order').drop('match_order', axis=1)
    else:
        filtered_df = filtered_df.sort_values(by='name')
    
    # Display dataset
    st.subheader(f"Phase 2 Records ({len(filtered_df)} records)")
    
    # Select columns to display
    display_cols = ['name', 'company', 'place', 'des_dan', 'des_dg', 'ind_confirm', 
                    'ind_session', 'ind_waitlist']
    available_cols = [col for col in display_cols if col in filtered_df.columns]
    display_df = filtered_df[available_cols].copy()
    
    # Fix Arrow serialization
    for col in display_df.columns:
        if col.startswith('ind_'):
            display_df[col] = pd.to_numeric(display_df[col], errors='coerce').fillna(0).astype('Int64')
    
    column_config = {'name': st.column_config.Column(pinned=True)}
    event = st.dataframe(display_df, column_config=column_config, height=200, 
                         on_select="rerun", selection_mode="single-row", key="phase2_table")
    
    # Handle row selection
    if event.selection.rows:
        selected_row_idx = event.selection.rows[0]
        selected_id = filtered_df.iloc[selected_row_idx]['id']
        st.session_state['phase2_selected_id'] = selected_id
    
    # Edit selected record
    if 'phase2_selected_id' in st.session_state and not filtered_df.empty:
        selected_id = st.session_state['phase2_selected_id']
        
        if selected_id in df['id'].values:
            selected_row = df[df['id'] == selected_id].iloc[0]
            
            st.markdown("---")
            df = render_phase2_edit_form(df, selected_row, config)
            
            st.markdown("---")
            render_team_balance(df, selected_row, config)
            
            st.markdown("---")
            render_selection_decision_table(df, selected_row, config)
    elif filtered_df.empty:
        st.info("ℹ️ No Phase 2 records found. Make sure records have ind_confirm = 1 after Phase 2 sync.")
    
    return df


def render_phase2_edit_form(df, selected_row, config):
    """Render the Phase 2 edit form with all fields."""
    st.subheader(f"📋 Edit: {selected_row['name']}")
    
    selected_id = selected_row['id']
    
    # Phase 1 Info (read-only display)
    with st.expander("📄 Phase 1 Information", expanded=False):
        col1, col2 = st.columns(2)
        phase1_fields = ['email', 'company', 'place', 'use_cases', 'role',
                         'nvl_excel', 'nvl_python', 'nvl_rstudio', 'nvl_sas', 'nvl_sql', 'nvl_vba',
                         'txt_success', 'des_centro_ges', 'des_dan', 'des_dg', 'des_dt', 'des_red']
        
        for i, field in enumerate(phase1_fields):
            if field in df.columns:
                col = col1 if i % 2 == 0 else col2
                with col:
                    value = selected_row.get(field, '')
                    value_str = str(value) if pd.notna(value) else ''
                    st.text_input(field, value=value_str, disabled=True, key=f"p1_{selected_id}_{field}")
    
    # Phase 1 Indicators (editable)
    st.markdown("### Phase 1 Indicators")
    ind_cols = st.columns(len(PHASE1_INDICATOR_FIELDS))
    for i, field in enumerate(PHASE1_INDICATOR_FIELDS):
        if field in df.columns:
            with ind_cols[i]:
                checked = bool(selected_row[field] == 1 or selected_row[field] == '1')
                st.checkbox(field, value=checked, key=f"p2edit_{selected_id}_{field}")
    
    # Phase 2 Fields (editable)
    st.markdown("### Phase 2 Information")
    
    for field in PHASE2_TEXT_FIELDS:
        if field in df.columns:
            value = selected_row.get(field, '')
            value_str = str(value) if pd.notna(value) else ''
            st.text_area(field, value=value_str, key=f"p2edit_{selected_id}_{field}", height=80)
    
    # Phase 2 Indicators (editable)
    st.markdown("### Phase 2 Indicators & Selection")
    ind_cols = st.columns(len(PHASE2_INDICATOR_FIELDS))
    for i, field in enumerate(PHASE2_INDICATOR_FIELDS):
        if field in df.columns:
            with ind_cols[i]:
                checked = bool(selected_row[field] == 1 or selected_row[field] == '1')
                st.checkbox(field, value=checked, key=f"p2edit_{selected_id}_{field}")

    # separator field
    st.markdown("---")
    
    # txt_review field (editable, just above url_1to1)
    if 'txt_review' in df.columns:
        txt_review_value = str(selected_row['txt_review']) if pd.notna(selected_row['txt_review']) else ""
        st.text_area("txt_review", value=txt_review_value, key=f"p2edit_{selected_id}_txt_review", height=80)

    

    # URL field
    if 'url_1to1' in df.columns:
        url_value = str(selected_row['url_1to1']) if pd.notna(selected_row['url_1to1']) else ""
        st.text_input("url_1to1", value=url_value, key=f"p2edit_{selected_id}_url_1to1")
        if url_value:
            st.markdown(f"[Open link]({url_value})")
    
    # Check for changes and save
    has_changes = check_phase2_changes(selected_row, selected_id, df)
    if has_changes:
        if st.button("💾 Save Changes", type="primary", key="p2_save"):
            df = save_phase2_changes(df, selected_row, selected_id, config)
            st.session_state['df'] = df
            st.success("✅ Changes saved!")
            st.rerun()
    
    return df


def check_phase2_changes(selected_row, selected_id, df):
    """Check if any Phase 2 field has been modified."""
    all_fields = PHASE1_INDICATOR_FIELDS + PHASE2_TEXT_FIELDS + PHASE2_INDICATOR_FIELDS + ['txt_review', 'url_1to1']
    
    for field in all_fields:
        if field not in df.columns:
            continue
        key = f"p2edit_{selected_id}_{field}"
        if key in st.session_state:
            current_value = st.session_state[key]
            original_value = selected_row.get(field)
            
            if field in PHASE1_INDICATOR_FIELDS + PHASE2_INDICATOR_FIELDS:
                original_bool = bool(original_value == 1 or original_value == '1')
                if current_value != original_bool:
                    return True
            else:
                original_str = str(original_value) if pd.notna(original_value) else ""
                if current_value != original_str:
                    return True
    return False


def save_phase2_changes(df, selected_row, selected_id, config):
    """Save Phase 2 changes to dataframe and Excel."""
    import tempfile
    import os
    
    all_fields = PHASE1_INDICATOR_FIELDS + PHASE2_TEXT_FIELDS + PHASE2_INDICATOR_FIELDS + ['txt_review', 'url_1to1']
    idx = df[df['id'] == selected_id].index[0]
    
    # Update df
    for field in all_fields:
        if field not in df.columns:
            continue
        key = f"p2edit_{selected_id}_{field}"
        if key in st.session_state:
            new_value = st.session_state[key]
            if field in PHASE1_INDICATOR_FIELDS + PHASE2_INDICATOR_FIELDS:
                new_value = int(1 if new_value else 0)
            df.at[idx, field] = new_value
    
    # Save to Excel
    excel_path = config['excel_path']
    sheet = config['excel_interpreter_spec']['sheet_name']
    excel_spec = config['excel_interpreter_spec']
    
    # Load full Excel
    full_df = pd.read_excel(excel_path, sheet_name=sheet, header=0, engine='openpyxl')
    
    # Get column mapping
    column_id_to_index = {col['column_id']: col['column'] for col in excel_spec['columns'] if col['column_id'] != 'skip'}
    
    # Find ID column
    id_column_idx = column_id_to_index.get('id', 0)
    id_column_name = full_df.columns[id_column_idx]
    
    # Find row in full_df
    full_df_mask = full_df[id_column_name] == selected_id
    if full_df_mask.any():
        full_df_idx = full_df[full_df_mask].index[0]
        
        # Update columns
        for field in all_fields:
            if field in column_id_to_index and field in df.columns:
                col_idx = column_id_to_index[field]
                if col_idx < len(full_df.columns):
                    full_df.at[full_df_idx, full_df.columns[col_idx]] = df.at[idx, field]
        
        # Write atomically
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx', dir=os.path.dirname(excel_path)) as tmp_file:
            tmp_path = tmp_file.name
            with pd.ExcelWriter(tmp_path, engine='openpyxl') as writer:
                full_df.to_excel(writer, sheet_name=sheet, index=False)
        os.replace(tmp_path, excel_path)
    
    return df


def render_team_balance(df, selected_row, config):
    """Render team balance view showing selection counts at different hierarchy levels."""
    st.subheader("⚖️ Team Balance")
    st.markdown("Count of people from the same organizational unit with `ind_confirm = 1`")
    
    # Get hierarchy levels
    hierarchy_levels = [
        ('des_centro_ges', 'Work Center'),
        ('des_dan', 'N+1 (DAN)'),
        ('des_dg', 'N+2 (DG)'),
        ('des_dt', 'N+3 (DT)'),
        ('des_red', 'Network')
    ]
    
    # Filter to ind_confirm = 1 (ensure no NULLs)
    df_clean = df.copy()
    if 'ind_confirm' in df_clean.columns:
        df_clean['ind_confirm'] = pd.to_numeric(df_clean['ind_confirm'], errors='coerce').fillna(0).astype(int)
    confirmed_df = df_clean[df_clean['ind_confirm'] == 1].copy()
    
    col1, col2, col3 = st.columns(3)
    
    for i, (col_name, display_name) in enumerate(hierarchy_levels):
        if col_name not in df.columns:
            continue
        
        current_value = selected_row.get(col_name)
        if pd.isna(current_value) or str(current_value).strip() == '':
            continue
        
        # Count people in same group
        same_group = confirmed_df[confirmed_df[col_name] == current_value]
        total_in_group = len(same_group)
        selected_in_group = (same_group['ind_session'] == 1).sum()
        waitlist_in_group = (same_group['ind_waitlist'] == 1).sum()
        
        col = [col1, col2, col3][i % 3]
        with col:
            st.metric(
                label=f"{display_name}",
                value=f"{selected_in_group}/{total_in_group}",
                delta=f"{waitlist_in_group} waitlist" if waitlist_in_group > 0 else None,
                help=f"Selected/Total confirmed in '{current_value}'"
            )


def render_selection_decision_table(df, selected_row, config):
    """Render selection decision table showing colleagues with ind_confirm = 1."""
    st.subheader("📊 Selection Decision Table")
    
    # Hierarchy selector
    hierarchy_options = {
        'des_centro_ges': 'Work Center',
        'des_dan': 'N+1 (DAN)',
        'des_dg': 'N+2 (DG)',
        'des_dt': 'N+3 (DT)'
    }
    
    available_options = {k: v for k, v in hierarchy_options.items() if k in df.columns}
    
    if not available_options:
        st.warning("No hierarchy columns available")
        return
    
    selected_hierarchy = st.selectbox(
        "Group by hierarchy level",
        options=list(available_options.keys()),
        format_func=lambda x: available_options[x],
        key="p2_hierarchy_select"
    )
    
    current_value = selected_row.get(selected_hierarchy)
    if pd.isna(current_value) or str(current_value).strip() == '':
        st.info(f"No {available_options[selected_hierarchy]} defined for this person")
        return
    
    st.markdown(f"**Showing colleagues in:** `{current_value}`")
    
    # Filter to same group with ind_confirm = 1 (ensure no NULLs)
    df_clean = df.copy()
    if 'ind_confirm' in df_clean.columns:
        df_clean['ind_confirm'] = pd.to_numeric(df_clean['ind_confirm'], errors='coerce').fillna(0).astype(int)
    confirmed_df = df_clean[(df_clean['ind_confirm'] == 1) & (df_clean[selected_hierarchy] == current_value)].copy()
    
    if confirmed_df.empty:
        st.info("No confirmed colleagues in this group")
        return
    
    # Prepare display
    display_cols = ['name', 'des_dan', 'ind_session', 'ind_waitlist']
    available_cols = [col for col in display_cols if col in confirmed_df.columns]
    
    table_df = confirmed_df[available_cols].copy()
    
    # Fix types for display
    for col in ['ind_session', 'ind_waitlist']:
        if col in table_df.columns:
            table_df[col] = pd.to_numeric(table_df[col], errors='coerce').fillna(0).astype('Int64')
    
    # Add status column
    def get_status(row):
        if row.get('ind_session', 0) == 1:
            return "✅ Selected"
        elif row.get('ind_waitlist', 0) == 1:
            return "⏳ Waitlist"
        else:
            return "❓ Pending"
    
    table_df['Status'] = table_df.apply(get_status, axis=1)
    
    # Reorder columns
    final_cols = ['name', 'Status'] + [c for c in available_cols if c not in ['name', 'ind_session', 'ind_waitlist']]
    table_df = table_df[final_cols]
    
    # Sort by status then name
    status_order = {'✅ Selected': 0, '⏳ Waitlist': 1, '❓ Pending': 2}
    table_df['_sort'] = table_df['Status'].map(status_order)
    table_df = table_df.sort_values(['_sort', 'name']).drop('_sort', axis=1)
    
    st.dataframe(table_df, hide_index=True, width='stretch')
    
    # Summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Selected", (confirmed_df['ind_session'] == 1).sum())
    with col2:
        st.metric("Waitlist", (confirmed_df['ind_waitlist'] == 1).sum())
    with col3:
        st.metric("Pending", len(confirmed_df) - (confirmed_df['ind_session'] == 1).sum() - (confirmed_df['ind_waitlist'] == 1).sum())
