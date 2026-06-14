import streamlit as st
import pandas as pd
import logging

from excel_io import atomic_write_sheet, load_full_sheet
from sync_rules import apply_binary_checks, apply_replicate_rules

logger = logging.getLogger(__name__)


def run(df, filters, config):
    """
    Data Sync Module: Syncs new records from source Excel to main Excel.
    
    Process:
    1. Read source Excel using source_path and source_path_spec
    2. Compare IDs to find new records (in source but not in main Excel)
    3. Display preview and ask for confirmation
    4. On confirmation: insert new records, apply replicate rules, convert binary_check fields
       - binary_check: Convert 'Sí' → 1, absent/other → 0
       - replicate: Copy values to both origin and destination columns
    """
    st.header("📥 Data Sync")
    st.markdown("Sync new records from source Excel to main Excel")
    
    # Extract config
    source_path = config.get('source_path')
    source_spec = config.get('source_path_spec', {})
    if not source_path:
        st.error("⚠️ No source_path configured in config.json")
        return
    
    # Get source columns from config (now numeric indexes)
    source_columns = source_spec.get('columns', [])
    
    if not source_columns:
        st.error("⚠️ No columns specified in source_path_spec.columns")
        return
    
    # Get ID column from config (now numeric index)
    id_column = source_spec.get('id', 0)
    
    # Get sheet name from config
    source_sheet = source_spec.get('sheet_name', 'Sheet1')
    
    st.info(f"ℹ️ **Source**: `{source_path}`")
    st.info(f"ℹ️ **Columns to sync**: {', '.join(map(str, source_columns))}")
    st.info(f"ℹ️ **ID column**: {id_column}")
    
    # Button to load and compare
    if st.button("🔍 Load and Compare Data"):
        with st.spinner("Loading source data..."):
            try:
                # Read source Excel - use numeric column indexes directly
                df_source = pd.read_excel(
                    source_path, 
                    sheet_name=source_sheet, 
                    header=None, 
                    usecols=source_columns, 
                    skiprows=1, 
                    engine='openpyxl'
                )
                df_source.columns = [str(i) for i in source_columns[:len(df_source.columns)]]
                
                st.success(f"✅ Loaded {len(df_source)} records from source")
                
            except FileNotFoundError:
                st.error(f"❌ Source file not found: {source_path}")
                return
            except Exception as e:
                st.error(f"❌ Error loading source file: {e}")
                logger.error(f"Error loading source: {e}")
                return
        
        # Compare IDs
        source_ids = set(df_source[str(id_column)].dropna().astype(str))
        existing_ids = set(df['id'].dropna().astype(str))
        new_ids = source_ids - existing_ids
        
        if not new_ids:
            st.success("✅ No new records to sync. All source records already exist in main Excel.")
            return
        
        # Filter new records
        df_new = df_source[df_source[str(id_column)].astype(str).isin(new_ids)].copy()
        
        # Store in session state for confirmation
        st.session_state['df_new'] = df_new
        st.session_state['new_ids'] = new_ids
        st.session_state['source_columns'] = source_columns
        
        st.success(f"🔍 Found **{len(df_new)}** new records to sync")
    
    # Display preview and confirmation
    if 'df_new' in st.session_state:
        df_new = st.session_state['df_new']
        new_ids = st.session_state['new_ids']
        source_columns = st.session_state['source_columns']
        
        st.subheader(f"📋 Preview: {len(df_new)} New Records")
        st.markdown("**These records will be added to the main Excel:**")
        
        # Show preview table
        st.dataframe(df_new, height=300)
        
        # Show summary
        st.markdown("### Summary of Changes")
        st.markdown(f"- **Records to add**: {len(df_new)}")
        st.markdown(f"- **IDs**: {', '.join(sorted(new_ids))}")
        st.markdown(f"- **Columns to insert**: {', '.join(map(str, source_columns))}")
        
        # Show replicate rules
        replicate_rules = source_spec.get('replicate', [])
        if replicate_rules:
            st.markdown("### Replication Rules")
            for rule in replicate_rules:
                origin = rule.get('origin')
                destination = rule.get('destination')
                column_id = rule.get('column_id')
                st.markdown(f"- Copy column **{origin}** → **{destination}** (`{column_id}`)")
        
        # Show binary_check rules
        binary_check_rules = source_spec.get('binary_check', [])
        if binary_check_rules:
            st.markdown("### Binary Check Conversions")
            st.markdown("Convert 'Sí' to 1, otherwise 0:")
            for rule in binary_check_rules:
                source_col = rule.get('column')
                dest_col = rule.get('destination')
                st.markdown(f"- Column **{source_col}** → **{dest_col}** (Sí=1, other=0)")
        
        # Confirmation
        st.warning("⚠️ **This action will modify the main Excel file. Please confirm to proceed.**")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("✅ Confirm & Sync", type="primary"):
                with st.spinner("Syncing data..."):
                    success = sync_data(df, df_new, config, source_columns)
                    if success:
                        st.success(f"✅ Successfully synced {len(df_new)} new records!")
                        # Clear session state
                        del st.session_state['df_new']
                        del st.session_state['new_ids']
                        del st.session_state['source_columns']
                        st.balloons()
                        st.rerun()
        with col2:
            if st.button("❌ Cancel"):
                # Clear session state
                del st.session_state['df_new']
                del st.session_state['new_ids']
                del st.session_state['source_columns']
                st.info("Sync cancelled")
                st.rerun()


def sync_data(df_main, df_new, config, source_columns):
    """
    Sync new records to main Excel:
    1. Map source columns to main Excel columns
    2. Apply replicate rules (copy to both origin and destination)
    3. Apply binary_check rules (convert 'Sí' → 1, other → 0)
    4. Append to Excel file
    """
    try:
        excel_spec = config['excel_interpreter_spec']
        source_spec = config['source_path_spec']

        # Load full Excel with header
        full_df = load_full_sheet(config)

        # Create column mapping: column_index -> column_id
        column_id_map = {str(col['column']): col['column_id'] for col in excel_spec['columns'] if col['column_id'] != 'skip'}

        # Prepare new rows to append
        new_rows = []

        for _, source_row in df_new.iterrows():
            # Create empty row with all Excel columns
            new_excel_row = pd.Series([None] * len(full_df.columns), index=full_df.columns)

            def set_excel(col_idx, value):
                if col_idx < len(full_df.columns):
                    new_excel_row[full_df.columns[col_idx]] = value

            def get_source(key):
                return source_row[key] if key in source_row else None

            # Map source columns to Excel columns
            for source_col in source_columns:
                source_col_str = str(source_col)
                if source_col_str in column_id_map and source_col_str in source_row:
                    set_excel(source_col, source_row[source_col_str])

            # Apply replicate rules (copy to both origin and destination)
            apply_replicate_rules(
                source_spec.get('replicate', []),
                get_source,
                set_excel,
                missing_field_value=source_spec.get('missing_field_value', 'sin respuesta'),
                missing_fields=source_spec.get('missing_fields', []),
                also_write_origin=True,
            )

            # Apply binary_check rules (save original value + convert 'Sí' → 1, other → 0)
            apply_binary_checks(
                source_spec.get('binary_check', []),
                get_source,
                set_excel,
                keep_original=True,
            )

            # Set ind_review, ind_select, ind_1to1 to 0 by default
            default_indicators = ['ind_review', 'ind_select', 'ind_1to1']
            for col_spec in excel_spec['columns']:
                if col_spec['column_id'] in default_indicators:
                    set_excel(col_spec['column'], 0)

            new_rows.append(new_excel_row)

        # Append new rows to full_df
        full_df = pd.concat([full_df, pd.DataFrame(new_rows)], ignore_index=True)

        atomic_write_sheet(full_df, config)

        logger.info(f"✅ Synced {len(df_new)} records successfully")
        return True
        
    except Exception as e:
        st.error(f"❌ Error syncing data: {e}")
        logger.error(f"Error syncing data: {e}")
        return False
