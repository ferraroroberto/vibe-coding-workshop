import streamlit as st
import pandas as pd
import logging
import tempfile
import os

logger = logging.getLogger(__name__)


def run(df, filters, config):
    """
    Selection Management Module: Bulk review and manage Phase 2 candidate selections.
    
    Features:
    1. Review all Phase 2 candidates (ind_confirm = 1)
    2. Mark selected/waitlist in bulk
    3. Team balance overview across all hierarchy levels
    4. Final decision management
    """
    st.header("🎯 Selection Management")
    st.markdown("Manage Phase 2 candidate selections and waitlist")
    
    # Apply filters
    filtered_df = df.copy()
    for col, selected in filters.items():
        if selected and col in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[col].isin(selected) | filtered_df[col].isna()]
    
    # Ensure ind_confirm is numeric with no NULLs
    if 'ind_confirm' in filtered_df.columns:
        filtered_df['ind_confirm'] = pd.to_numeric(filtered_df['ind_confirm'], errors='coerce').fillna(0).astype(int)
    
    # Phase 2 candidates only (ind_confirm = 1)
    candidates_df = filtered_df[filtered_df['ind_confirm'] == 1].copy()
    
    if candidates_df.empty:
        st.warning("⚠️ No Phase 2 candidates found (records with ind_confirm = 1)")
        st.info("ℹ️ Use the 'Phase 2 Sync' tab to import Phase 2 form data first.")
        return df
    
    # Summary metrics
    st.markdown("### 📊 Selection Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Candidates", len(candidates_df))
    with col2:
        selected_count = (candidates_df['ind_session'] == 1).sum()
        st.metric("Selected", selected_count)
    with col3:
        waitlist_count = (candidates_df['ind_waitlist'] == 1).sum()
        st.metric("Waitlist", waitlist_count)
    with col4:
        pending_count = len(candidates_df) - selected_count - waitlist_count
        st.metric("Pending", pending_count)
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 Candidate List", "⚖️ Team Balance", "📈 Quick Actions"])
    
    with tab1:
        df = render_candidate_list(df, candidates_df, config)
    
    with tab2:
        render_team_balance_overview(candidates_df, config)
    
    with tab3:
        df = render_quick_actions(df, candidates_df, config)
    
    return df


def render_candidate_list(df, candidates_df, config):
    """Render the main candidate list with inline selection controls."""
    st.subheader("📋 All Phase 2 Candidates")
    
    # Group by selector
    group_options = {
        'none': 'No grouping',
        'des_dan': 'N+1 (DAN)',
        'des_dg': 'N+2 (DG)',
        'des_dt': 'N+3 (DT)',
        'des_centro_ges': 'Work Center'
    }
    
    available_options = {k: v for k, v in group_options.items() if k == 'none' or k in candidates_df.columns}
    
    selected_grouping = st.selectbox(
        "Group by",
        options=list(available_options.keys()),
        format_func=lambda x: available_options[x],
        key="sm_group_by"
    )
    
    # Status filter
    status_filter = st.multiselect(
        "Filter by Status",
        options=['Selected', 'Waitlist', 'Pending'],
        default=['Selected', 'Waitlist', 'Pending'],
        key="sm_status_filter"
    )
    
    # Apply status filter
    def get_status_value(row):
        if row.get('ind_session', 0) == 1:
            return 'Selected'
        elif row.get('ind_waitlist', 0) == 1:
            return 'Waitlist'
        return 'Pending'
    
    candidates_df = candidates_df.copy()
    candidates_df['_status'] = candidates_df.apply(get_status_value, axis=1)
    filtered_candidates = candidates_df[candidates_df['_status'].isin(status_filter)]
    
    if filtered_candidates.empty:
        st.info("No candidates match the selected filters")
        return df
    
    # Display with or without grouping
    if selected_grouping == 'none':
        df = render_candidate_table(df, filtered_candidates, config)
    else:
        groups = filtered_candidates.groupby(selected_grouping)
        for group_name, group_df in groups:
            group_display = str(group_name) if pd.notna(group_name) else 'Unknown'
            with st.expander(f"📁 {group_display} ({len(group_df)} candidates)", expanded=False):
                # Group summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Selected", (group_df['ind_session'] == 1).sum())
                with col2:
                    st.metric("Waitlist", (group_df['ind_waitlist'] == 1).sum())
                with col3:
                    pending = len(group_df) - (group_df['ind_session'] == 1).sum() - (group_df['ind_waitlist'] == 1).sum()
                    st.metric("Pending", pending)
                
                df = render_candidate_table(df, group_df, config, group_key=str(group_name))
    
    return df


def render_candidate_table(df, candidates_df, config, group_key=""):
    """Render a table of candidates with selection controls."""
    # Prepare display columns
    display_cols = ['name', 'company', 'des_dan', 'nvl_python', '_status']
    available_cols = [col for col in display_cols if col in candidates_df.columns or col == '_status']
    
    table_df = candidates_df[available_cols].copy()
    
    # Rename status column for display
    table_df = table_df.rename(columns={'_status': 'Status'})
    
    st.dataframe(table_df, hide_index=True, width='stretch', key=f"candidates_table_{group_key}")
    
    # Quick selection buttons for this group
    st.markdown("**Quick actions for this group:**")
    col1, col2, col3, col4 = st.columns(4)
    
    pending_ids = candidates_df[candidates_df['_status'] == 'Pending']['id'].tolist()
    
    with col1:
        if st.button(f"Select All Pending ({len(pending_ids)})", key=f"select_all_{group_key}", disabled=len(pending_ids) == 0):
            df = bulk_update_status(df, pending_ids, 'ind_session', 1, config)
            st.session_state['df'] = df
            st.success(f"✅ Selected {len(pending_ids)} candidates")
            st.rerun()
    
    with col2:
        if st.button(f"Waitlist All Pending", key=f"waitlist_all_{group_key}", disabled=len(pending_ids) == 0):
            df = bulk_update_status(df, pending_ids, 'ind_waitlist', 1, config)
            st.session_state['df'] = df
            st.success(f"⏳ Added {len(pending_ids)} to waitlist")
            st.rerun()
    
    with col3:
        selected_ids = candidates_df[candidates_df['_status'] == 'Selected']['id'].tolist()
        if st.button(f"Clear Selected ({len(selected_ids)})", key=f"clear_selected_{group_key}", disabled=len(selected_ids) == 0):
            df = bulk_update_status(df, selected_ids, 'ind_session', 0, config)
            st.session_state['df'] = df
            st.success(f"Cleared {len(selected_ids)} selections")
            st.rerun()
    
    with col4:
        waitlist_ids = candidates_df[candidates_df['_status'] == 'Waitlist']['id'].tolist()
        if st.button(f"Clear Waitlist ({len(waitlist_ids)})", key=f"clear_waitlist_{group_key}", disabled=len(waitlist_ids) == 0):
            df = bulk_update_status(df, waitlist_ids, 'ind_waitlist', 0, config)
            st.session_state['df'] = df
            st.success(f"Cleared {len(waitlist_ids)} from waitlist")
            st.rerun()
    
    return df


def render_team_balance_overview(candidates_df, config):
    """Render team balance overview across all hierarchy levels."""
    st.subheader("⚖️ Team Balance Overview")
    st.markdown("Selection distribution across organizational hierarchy")
    
    hierarchy_levels = [
        ('des_dt', 'N+3 (DT)'),
        ('des_dg', 'N+2 (DG)'),
        ('des_dan', 'N+1 (DAN)'),
        ('des_centro_ges', 'Work Center')
    ]
    
    for col_name, display_name in hierarchy_levels:
        if col_name not in candidates_df.columns:
            continue
        
        st.markdown(f"### {display_name}")
        
        # Group by this hierarchy level
        grouped = candidates_df.groupby(col_name).agg({
            'id': 'count',
            'ind_session': lambda x: (x == 1).sum(),
            'ind_waitlist': lambda x: (x == 1).sum()
        }).reset_index()
        
        grouped.columns = [display_name, 'Total', 'Selected', 'Waitlist']
        grouped['Pending'] = grouped['Total'] - grouped['Selected'] - grouped['Waitlist']
        grouped['Selection Rate'] = (grouped['Selected'] / grouped['Total'] * 100).round(1)

        # Order columns: [display_name, 'Total', 'Selected', 'Selection Rate', 'Waitlist', 'Pending']
        cols = [display_name, 'Total', 'Selected', 'Selection Rate', 'Waitlist', 'Pending']
        grouped = grouped[cols]

        # Sort by total descending
        grouped = grouped.sort_values('Total', ascending=False)

        # Use Styler to format as percentage and align right (numeric type for alignment)
        styled_df = grouped.style.format({'Selection Rate': '{:.1f}%'}).set_properties(subset=['Selection Rate'], **{'text-align': 'right'})
        st.dataframe(styled_df, hide_index=True, width='stretch')
        st.markdown("---")


def render_quick_actions(df, candidates_df, config):
    """Render quick bulk actions panel."""
    st.subheader("📈 Quick Actions")
    st.markdown("Bulk operations for managing selections")
    
    # Statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Current Status")
        total = len(candidates_df)
        selected = (candidates_df['ind_session'] == 1).sum()
        waitlist = (candidates_df['ind_waitlist'] == 1).sum()
        pending = total - selected - waitlist
        
        st.write(f"- **Total candidates**: {total}")
        st.write(f"- **Selected**: {selected} ({selected/total*100:.1f}%)")
        st.write(f"- **Waitlist**: {waitlist} ({waitlist/total*100:.1f}%)")
        st.write(f"- **Pending**: {pending} ({pending/total*100:.1f}%)")
    
    with col2:
        st.markdown("### Target Settings")
        target_selected = st.number_input("Target number selected", min_value=0, max_value=total, value=min(20, total), key="target_selected")
        target_waitlist = st.number_input("Target waitlist size", min_value=0, max_value=total, value=min(10, total), key="target_waitlist")
        
        remaining_selected = target_selected - selected
        remaining_waitlist = target_waitlist - waitlist
        
        if remaining_selected > 0:
            st.info(f"ℹ️ Need to select {remaining_selected} more candidates")
        elif remaining_selected < 0:
            st.warning(f"⚠️ Over target by {-remaining_selected} selections")
        else:
            st.success("✅ Selection target met!")
        
        if remaining_waitlist > 0:
            st.info(f"ℹ️ Need {remaining_waitlist} more for waitlist")
    
    st.markdown("---")
    
    # Danger zone
    st.markdown("### ⚠️ Bulk Operations")
    st.warning("These actions affect all filtered candidates. Use with caution!")
    
    col1, col2, col3 = st.columns(3)
    
    all_ids = candidates_df['id'].tolist()
    
    with col1:
        if st.button("🔄 Reset All to Pending", type="secondary", key="reset_all"):
            # Clear both ind_session and ind_waitlist
            df = bulk_update_status(df, all_ids, 'ind_session', 0, config)
            df = bulk_update_status(df, all_ids, 'ind_waitlist', 0, config, save=True)
            st.session_state['df'] = df
            st.success(f"Reset {len(all_ids)} candidates to pending")
            st.rerun()
    
    with col2:
        pending_ids = candidates_df[(candidates_df['ind_session'] != 1) & (candidates_df['ind_waitlist'] != 1)]['id'].tolist()
        if st.button(f"✅ Select All Pending ({len(pending_ids)})", type="primary", key="select_all_pending", disabled=len(pending_ids) == 0):
            df = bulk_update_status(df, pending_ids, 'ind_session', 1, config)
            st.session_state['df'] = df
            st.success(f"Selected {len(pending_ids)} candidates")
            st.rerun()
    
    with col3:
        if st.button("📋 Export Selection Report", key="export_report"):
            export_selection_report(candidates_df)
    
    return df


def bulk_update_status(df, ids, column, value, config, save=True):
    """Bulk update a status column for multiple records."""
    # Update df
    mask = df['id'].isin(ids)
    df.loc[mask, column] = value
    
    if not save:
        return df
    
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
    
    # Find target column
    if column not in column_id_to_index:
        logger.warning(f"Column {column} not found in config")
        return df
    
    target_col_idx = column_id_to_index[column]
    target_col_name = full_df.columns[target_col_idx]
    
    # Update rows
    mask = full_df[id_column_name].isin(ids)
    full_df.loc[mask, target_col_name] = value
    
    # Write atomically
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx', dir=os.path.dirname(excel_path)) as tmp_file:
        tmp_path = tmp_file.name
        with pd.ExcelWriter(tmp_path, engine='openpyxl') as writer:
            full_df.to_excel(writer, sheet_name=sheet, index=False)
    os.replace(tmp_path, excel_path)
    
    logger.info(f"✅ Bulk updated {len(ids)} records: {column} = {value}")
    return df


def export_selection_report(candidates_df):
    """Export selection report to Excel."""
    import io
    
    # Prepare report data
    report_df = candidates_df.copy()
    
    # Add status column
    def get_status(row):
        if row.get('ind_session', 0) == 1:
            return "Selected"
        elif row.get('ind_waitlist', 0) == 1:
            return "Waitlist"
        return "Pending"
    
    report_df['selection_status'] = report_df.apply(get_status, axis=1)
    
    # Select columns for report
    report_cols = ['name', 'email', 'company', 'place', 'des_dan', 'des_dg', 'des_dt',
                   'nvl_python', 'ind_confirm', 'ind_session', 'ind_waitlist', 'selection_status']
    available_cols = [col for col in report_cols if col in report_df.columns]
    report_df = report_df[available_cols]
    
    # Create summary
    summary_data = {
        'Metric': ['Total Candidates', 'Selected', 'Waitlist', 'Pending'],
        'Count': [
            len(candidates_df),
            (candidates_df['ind_session'] == 1).sum(),
            (candidates_df['ind_waitlist'] == 1).sum(),
            len(candidates_df) - (candidates_df['ind_session'] == 1).sum() - (candidates_df['ind_waitlist'] == 1).sum()
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    
    # Write to Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        report_df.to_excel(writer, sheet_name='Candidates', index=False)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    output.seek(0)
    
    st.download_button(
        label="📥 Download Report",
        data=output,
        file_name="selection_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
