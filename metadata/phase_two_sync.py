import streamlit as st
import pandas as pd
import logging
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from excel_io import atomic_write_sheet, find_id_column_name, load_full_sheet
from sync_rules import apply_binary_checks, apply_replicate_rules

logger = logging.getLogger(__name__)


def run(df, filters, config):
    """
    Phase 2 Sync Module: Syncs Phase 2 form data to existing records in master dataset.
    
    Process:
    1. Read Phase 2 Excel using phase_two_path and phase_two_spec
    2. Match by name (fuzzy) - only update existing records from Phase 1
    3. Show validation results (matched/unmatched)
    4. Apply replicate rules and binary_check rules from config
    5. Preview and confirm merge
    """
    st.header("📥 Phase 2 Sync")
    st.markdown("Sync Phase 2 form data to existing Phase 1 records")
    
    # Extract config
    phase_two_path = config.get('phase_two_path')
    phase_two_spec = config.get('phase_two_spec', {})
    if not phase_two_path:
        st.error("⚠️ No phase_two_path configured in config.json")
        return df
    
    if not phase_two_spec:
        st.error("⚠️ No phase_two_spec configured in config.json")
        return df
    
    # Get source columns from config
    source_columns = phase_two_spec.get('columns', [])
    if not source_columns:
        st.error("⚠️ No columns specified in phase_two_spec.columns")
        return df
    
    # Get name column for matching
    name_column = phase_two_spec.get('name', 4)
    source_sheet = phase_two_spec.get('sheet_name', 'Sheet1')
    
    st.info(f"ℹ️ **Phase 2 Source**: `{phase_two_path}`")
    st.info(f"ℹ️ **Columns to sync**: {', '.join(map(str, source_columns))}")
    st.info(f"ℹ️ **Name column for matching**: {name_column}")
    
    # Show current Phase 2 status
    st.markdown("### 📊 Current Phase 2 Status")
    phase2_cols = ['ind_confirm', 'ide_python', 'ide_sql', 'txt_usecase_data', 
                   'txt_usecase_visual', 'txt_usecase_automate']
    
    # Count records that have at least one Phase 2 field populated
    has_phase2_mask = pd.Series([False] * len(df), index=df.index)
    for col in phase2_cols:
        if col in df.columns:
            if col.startswith('ind_'):
                has_phase2_mask |= (df[col] == 1)
            else:
                has_phase2_mask |= (df[col].notna() & (df[col] != ''))
    
    has_phase2_data = has_phase2_mask.sum()
    
    st.markdown(f"**Records with Phase 2 data**: {has_phase2_data}")
    
    # Button to load and compare
    if st.button("🔍 Load Phase 2 Data"):
        with st.spinner("Loading Phase 2 data..."):
            try:
                # First, get total rows in Excel
                total_df = pd.read_excel(phase_two_path, sheet_name=source_sheet, header=0, engine='openpyxl')
                total_rows = len(total_df)
                st.info(f"ℹ️ **Total rows in Excel (excluding header)**: {total_rows}")
                
                # Read Phase 2 Excel with specified columns
                df_phase2 = pd.read_excel(
                    phase_two_path,
                    sheet_name=source_sheet,
                    header=None,
                    usecols=source_columns,
                    skiprows=1,
                    engine='openpyxl'
                )
                df_phase2.columns = [str(i) for i in source_columns[:len(df_phase2.columns)]]
                
                loaded_rows = len(df_phase2)
                st.success(f"✅ Loaded {loaded_rows} records from Phase 2 source (columns {source_columns})")
                
                # Load full data to identify rows with no data in source columns
                full_phase2 = pd.read_excel(
                    phase_two_path,
                    sheet_name=source_sheet,
                    header=None,
                    skiprows=1,
                    engine='openpyxl'
                )
                # Find rows where all source_columns are empty
                empty_mask = full_phase2[source_columns].isna().all(axis=1) | (full_phase2[source_columns].astype(str) == '').all(axis=1)
                empty_rows = full_phase2[empty_mask]
                
                if not empty_rows.empty:
                    st.warning(f"⚠️ Found {len(empty_rows)} rows in Phase 2 file with no data in the specified columns (these were not loaded)")
                
                # Check for duplicates by name and handle them
                name_col = str(name_column)
                id_col = str(phase_two_spec.get('id', 0))
                if name_col in df_phase2.columns and id_col in df_phase2.columns:
                    duplicates = df_phase2[df_phase2.duplicated(subset=[name_col], keep=False)]
                    if not duplicates.empty:
                        st.warning(f"⚠️ Found {len(duplicates)} duplicate records by name. Keeping the one with largest ID for each name.")
                        # Sort by name then by ID descending, drop duplicates keeping last (largest ID)
                        df_phase2 = df_phase2.sort_values(by=[name_col, id_col], ascending=[True, False]).drop_duplicates(subset=[name_col], keep='first')
                        st.info(f"📊 After deduplication: {len(df_phase2)} records")
                
            except FileNotFoundError:
                st.error(f"❌ Phase 2 file not found: {phase_two_path}")
                return df
            except Exception as e:
                st.error(f"❌ Error loading Phase 2 file: {e}")
                logger.error(f"Error loading Phase 2 source: {e}")
                return df
        
        # Match Phase 2 records to existing Phase 1 records by name
        with st.spinner("Matching names..."):
            matched_records, unmatched_records = match_phase2_to_phase1(
                df, df_phase2, str(name_column)
            )
        
        if len(matched_records) == 0:
            st.warning("⚠️ No matching records found. Phase 2 names must match existing Phase 1 records.")
            if len(unmatched_records) > 0:
                st.error(f"❌ {len(unmatched_records)} records could not be matched:")
                st.dataframe(unmatched_records[[str(name_column)]], height=200)
            return df
        
        # Store in session state
        st.session_state['phase2_matched'] = matched_records
        st.session_state['phase2_unmatched'] = unmatched_records
        st.session_state['phase2_source_columns'] = source_columns
        st.session_state['df_phase2'] = df_phase2
        st.session_state['phase2_empty'] = empty_rows
        
        st.success(f"🔍 Matched **{len(matched_records)}** records")
        if len(unmatched_records) > 0:
            st.warning(f"⚠️ **{len(unmatched_records)}** records could not be matched")
    
    # Display preview and confirmation
    if 'phase2_matched' in st.session_state:
        matched_records = st.session_state['phase2_matched']
        unmatched_records = st.session_state['phase2_unmatched']
        source_columns = st.session_state['phase2_source_columns']
        df_phase2 = st.session_state['df_phase2']
        empty_rows = st.session_state.get('phase2_empty', pd.DataFrame())
        
        # Show empty rows first
        if not empty_rows.empty:
            st.subheader(f"📋 Empty Rows: {len(empty_rows)} Records with No Data")
            st.markdown("**These Phase 2 records have no data in the specified columns and were not loaded:**")
            # Show first 5 columns for context
            display_empty = empty_rows.iloc[:, :5].copy()
            display_empty.columns = [f'Col {i}' for i in range(len(display_empty.columns))]
            st.dataframe(display_empty, height=150)
        
        st.subheader(f"📋 Preview: {len(matched_records)} Matched Records")
        
        # Show matched records
        st.markdown("**These records will be updated with Phase 2 data:**")
        display_matched = matched_records[['master_id', 'master_name', 'phase2_name', 'match_score']].copy()
        display_matched.columns = ['ID', 'Master Name', 'Phase 2 Name', 'Match Score (%)']
        st.dataframe(display_matched, height=300)
        
        # Show unmatched records
        if len(unmatched_records) > 0:
            st.markdown("**⚠️ These Phase 2 records could NOT be matched (will be skipped):**")
            st.dataframe(unmatched_records[[str(phase_two_spec.get('name', 4))]], height=150)
        
        # Show replicate rules
        replicate_rules = phase_two_spec.get('replicate', [])
        if replicate_rules:
            st.markdown("### Replication Rules")
            for rule in replicate_rules:
                origin = rule.get('origin')
                destination = rule.get('destination')
                column_id = rule.get('column_id')
                st.markdown(f"- Column **{origin}** → Master column **{destination}** (`{column_id}`)")
        
        # Show binary_check rules
        binary_check_rules = phase_two_spec.get('binary_check', [])
        if binary_check_rules:
            st.markdown("### Binary Check Conversions")
            st.markdown("Convert 'Sí' to 1, otherwise 0:")
            for rule in binary_check_rules:
                source_col = rule.get('column')
                dest_col = rule.get('destination')
                column_id = rule.get('column_id', '')
                st.markdown(f"- Column **{source_col}** → **{dest_col}** (`{column_id}`) (Sí=1, other=0)")
        
        # Confirmation
        st.warning("⚠️ **This action will update the master dataset with Phase 2 data. Please confirm to proceed.**")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("✅ Confirm & Sync", type="primary", key="phase2_confirm"):
                with st.spinner("Syncing Phase 2 data..."):
                    df_updated = sync_phase2_data(
                        df, matched_records, df_phase2, config
                    )
                    if df_updated is not None:
                        st.success(f"✅ Successfully synced {len(matched_records)} Phase 2 records!")
                        # Clear session state
                        clear_phase2_session_state()
                        st.session_state['df'] = df_updated
                        st.balloons()
                        st.rerun()
        with col2:
            if st.button("❌ Cancel", key="phase2_cancel"):
                clear_phase2_session_state()
                st.info("Phase 2 sync cancelled")
                st.rerun()
    
    return df


def match_phase2_to_phase1(df_master, df_phase2, name_column):
    """
    Match Phase 2 records to Phase 1 records using fuzzy name matching.
    
    Args:
        df_master: Master dataframe (Phase 1 records)
        df_phase2: Phase 2 dataframe
        name_column: Column name containing names in Phase 2 data
    
    Returns:
        matched_records: DataFrame with matched records (master_id, master_name, phase2_name, phase2_idx, match_score)
        unmatched_records: DataFrame with unmatched Phase 2 records
    """
    master_names = df_master['name'].dropna().tolist()
    master_ids = df_master['id'].tolist()
    name_to_id = dict(zip(master_names, master_ids))
    
    matched = []
    unmatched = []
    
    for idx, row in df_phase2.iterrows():
        phase2_name = row.get(name_column)
        if pd.isna(phase2_name) or str(phase2_name).strip() == '':
            unmatched.append(row)
            continue
        
        phase2_name = str(phase2_name).strip()
        
        # Fuzzy match
        match_result = process.extractOne(phase2_name, master_names, scorer=fuzz.ratio)
        
        if match_result and match_result[1] >= 85:  # 85% threshold for matching
            best_match_name = match_result[0]
            match_score = match_result[1]
            master_id = name_to_id[best_match_name]
            
            matched.append({
                'master_id': master_id,
                'master_name': best_match_name,
                'phase2_name': phase2_name,
                'phase2_idx': idx,
                'match_score': match_score
            })
        else:
            unmatched.append(row)
    
    matched_df = pd.DataFrame(matched) if matched else pd.DataFrame()
    unmatched_df = pd.DataFrame(unmatched) if unmatched else pd.DataFrame()
    
    return matched_df, unmatched_df


def sync_phase2_data(df_master, matched_records, df_phase2, config):
    """
    Sync Phase 2 data to master dataset.
    
    Args:
        df_master: Master dataframe
        matched_records: DataFrame with match info (master_id, phase2_idx)
        df_phase2: Phase 2 source dataframe
        config: Configuration dict
    
    Returns:
        Updated master dataframe
    """
    try:
        excel_spec = config['excel_interpreter_spec']
        phase_two_spec = config['phase_two_spec']

        # Load full Excel with header
        full_df = load_full_sheet(config)

        # Find the ID column in full_df
        id_column_name = find_id_column_name(full_df, config)

        # Get rules from Phase 2 spec
        replicate_rules = phase_two_spec.get('replicate', [])
        binary_check_rules = phase_two_spec.get('binary_check', [])
        missing_field_value = phase_two_spec.get('missing_field_value', 'sin respuesta')
        missing_fields = phase_two_spec.get('missing_fields', [])

        # Process each matched record
        for _, match in matched_records.iterrows():
            master_id = match['master_id']
            phase2_idx = match['phase2_idx']

            # Get Phase 2 row
            phase2_row = df_phase2.iloc[phase2_idx]

            # Find the row in full_df
            full_df_mask = full_df[id_column_name] == master_id
            if not full_df_mask.any():
                logger.warning(f"⚠️ Could not find master_id {master_id} in Excel")
                continue

            full_df_idx = full_df[full_df_mask].index[0]

            # Also update df_master
            master_mask = df_master['id'] == master_id
            if not master_mask.any():
                continue
            master_idx = df_master[master_mask].index[0]

            def get_source(key):
                return phase2_row[key] if key in phase2_row.index else None

            def set_excel(col_idx, value):
                if col_idx < len(full_df.columns):
                    full_df.at[full_df_idx, full_df.columns[col_idx]] = value

            def set_master(column_id, value):
                if column_id in df_master.columns:
                    df_master.at[master_idx, column_id] = value

            apply_replicate_rules(
                replicate_rules,
                get_source,
                set_excel,
                missing_field_value=missing_field_value,
                missing_fields=missing_fields,
                set_master=set_master,
            )

            apply_binary_checks(
                binary_check_rules,
                get_source,
                set_excel,
                set_master=set_master,
            )

        atomic_write_sheet(full_df, config)

        # Set all 'ind_' columns to zero where null/NaN
        ind_cols = [col for col in df_master.columns if col.startswith('ind_')]
        if ind_cols:
            df_master[ind_cols] = df_master[ind_cols].fillna(0)
        logger.info(f"✅ Synced {len(matched_records)} Phase 2 records successfully")
        return df_master
        
    except Exception as e:
        st.error(f"❌ Error syncing Phase 2 data: {e}")
        logger.error(f"Error syncing Phase 2 data: {e}")
        import traceback
        st.code(traceback.format_exc())
        return None


def clear_phase2_session_state():
    """Clear Phase 2 sync session state."""
    keys_to_remove = ['phase2_matched', 'phase2_unmatched', 'phase2_source_columns', 'df_phase2', 'phase2_empty']
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]
