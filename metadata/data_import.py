import streamlit as st
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)


def run(df, filters, config):
    """
    Data Import Module: Enriches base table with employee and work center data.
    
    Process:
    1. Load employee and work center data from CSV files
    2. Match base table NAME field with concatenated employee names
    3. Join with work center data using PK_EMPL
    4. Fill missing values with defaults (-1 for numeric, "not found" for text)
    5. Display preview and ask for confirmation
    6. On confirmation: update and save the enriched data
    """
    st.header("📦 Data Import")
    st.markdown("Enrich base data with employee and work center information")
    
    # Extract config
    emp_config = config.get('source_path_employees', {})
    wc_config = config.get('source_path_workcenters', {})
    excel_path = config.get('excel_path')
    excel_spec = config.get('excel_interpreter_spec', {})
    
    if not emp_config or not wc_config:
        st.error("⚠️ Employee or work center configuration missing in config.json")
        return
    
    # Build file paths
    emp_path = os.path.join(emp_config.get('path', ''), emp_config.get('file', ''))
    wc_path = os.path.join(wc_config.get('path', ''), wc_config.get('file', ''))
    
    st.info(f"ℹ️ **Employee Source**: `{emp_path}`")
    st.info(f"ℹ️ **Work Center Source**: `{wc_path}`")
    
    # Count current null values in columns 27-37
    target_columns = ['pk_empl', 'fk_centro', 'des_centro_ges', 'cod_dan', 'des_dan', 
                      'cod_dg', 'des_dg', 'cod_dt', 'des_dt', 'cod_red', 'des_red']
    
    null_counts = {}
    for col in target_columns:
        if col in df.columns:
            null_counts[col] = df[col].isna().sum()
    
    total_nulls = sum(null_counts.values())
    
    st.markdown("### 📊 Current Data Status")
    st.markdown(f"**Total null values in target columns (27-37)**: {total_nulls}")
    
    if total_nulls > 0:
        st.markdown("**Null counts by column:**")
        for col, count in null_counts.items():
            if count > 0:
                st.markdown(f"- `{col}`: {count} null values")
    else:
        st.success("✅ No null values found. All records already enriched.")
    
    # Button to load and process
    if st.button("🔍 Load and Enrich Data"):
        with st.spinner("Loading employee and work center data..."):
            try:
                # Load employee data (semicolon separator)
                df_emp = pd.read_csv(emp_path, sep=';', encoding='utf-8')
                emp_keep_cols = emp_config.get('keep', [])
                df_emp = df_emp[emp_keep_cols]
                
                st.success(f"✅ Loaded {len(df_emp)} employee records")
                
                # Load work center data (comma separator)
                df_wc = pd.read_csv(wc_path, sep=',', encoding='utf-8')
                wc_keep_cols = wc_config.get('keep', [])
                df_wc = df_wc[wc_keep_cols]
                
                st.success(f"✅ Loaded {len(df_wc)} work center records")
                
            except FileNotFoundError as e:
                st.error(f"❌ File not found: {e}")
                return
            except Exception as e:
                st.error(f"❌ Error loading files: {e}")
                logger.error(f"Error loading source files: {e}")
                return
        
        with st.spinner("Processing data enrichment..."):
            try:
                # Create concatenated name in employee table
                df_emp['full_name'] = df_emp.apply(
                    lambda row: concatenate_name(
                        row.get('NOMBRE_EMPLEADO'),
                        row.get('APELLIDO1_EMPLEADO'),
                        row.get('APELLIDO2_EMPLEADO')
                    ),
                    axis=1
                )
                
                # Create a copy of base df for enrichment
                df_enriched = df.copy().reset_index(drop=True)
                
                # Store original row count
                original_row_count = len(df_enriched)
                
                # Match base table with employee data on NAME field
                df_enriched = df_enriched.merge(
                    df_emp[['full_name', 'PK_EMPL', 'FK_CENTRO']],
                    left_on='name',
                    right_on='full_name',
                    how='left',
                    suffixes=('', '_emp')
                ).reset_index(drop=True)
                
                # Check for duplicates after first merge
                duplicates_emp = []
                if len(df_enriched) > original_row_count:
                    # Find duplicate IDs
                    duplicate_ids = df_enriched[df_enriched.duplicated(subset=['id'], keep=False)]['id'].unique()
                    duplicates_emp = df_enriched[df_enriched['id'].isin(duplicate_ids)][['id', 'name', 'PK_EMPL', 'FK_CENTRO']].sort_values('id')
                    
                    # For duplicates, prioritize records with valid FK_CENTRO (not null and not -1)
                    def select_best_match(group):
                        # First, try to get rows with valid FK_CENTRO
                        valid_fk = group[group['FK_CENTRO'].notna() & (group['FK_CENTRO'] != -1)]
                        if len(valid_fk) > 0:
                            return valid_fk.iloc[0]
                        # Otherwise, return first row
                        return group.iloc[0]
                    
                    # Group by ID and select best match for each
                    df_enriched = df_enriched.groupby('id', as_index=False).apply(select_best_match).reset_index(drop=True)
                
                # Join with work center data
                df_enriched = df_enriched.merge(
                    df_wc,
                    left_on='FK_CENTRO',
                    right_on='PK_CENTRO',
                    how='left',
                    suffixes=('', '_wc')
                ).reset_index(drop=True)
                
                # Check for duplicates after second merge
                duplicates_wc = []
                if len(df_enriched) > original_row_count:
                    duplicate_ids = df_enriched[df_enriched.duplicated(subset=['id'], keep=False)]['id'].unique()
                    duplicates_wc = df_enriched[df_enriched['id'].isin(duplicate_ids)][['id', 'name', 'FK_CENTRO', 'PK_CENTRO']].sort_values('id')
                    
                    # For duplicates, prioritize records with non-null work center data
                    def select_best_wc_match(group):
                        # Try to get rows with non-null DES_CENTRO_GES
                        valid_wc = group[group['DES_CENTRO_GES'].notna()]
                        if len(valid_wc) > 0:
                            return valid_wc.iloc[0]
                        return group.iloc[0]
                    
                    df_enriched = df_enriched.groupby('id', as_index=False).apply(select_best_wc_match).reset_index(drop=True)
                
                # Store duplicate info in session state
                if len(duplicates_emp) > 0:
                    st.session_state['duplicates_emp'] = duplicates_emp
                if len(duplicates_wc) > 0:
                    st.session_state['duplicates_wc'] = duplicates_wc
                
                # Update target columns in base df with enriched data
                # Columns 27-37 mapping
                column_mapping = {
                    'PK_EMPL': 'pk_empl',
                    'FK_CENTRO': 'fk_centro',
                    'DES_CENTRO_GES': 'des_centro_ges',
                    'COD_DAN': 'cod_dan',
                    'DES_DAN': 'des_dan',
                    'COD_DG': 'cod_dg',
                    'DES_DG': 'des_dg',
                    'COD_DT': 'cod_dt',
                    'DES_DT': 'des_dt',
                    'COD_RED': 'cod_red',
                    'DES_RED': 'des_red'
                }
                
                # Count unique records that have at least one null in target columns
                target_cols_list = list(column_mapping.values())
                existing_target_cols = [col for col in target_cols_list if col in df.columns]
                if existing_target_cols:
                    records_updated = df[existing_target_cols].isna().any(axis=1).sum()
                else:
                    records_updated = len(df)
                
                # Map source columns to target columns - populate or update
                for source_col, target_col in column_mapping.items():
                    if source_col in df_enriched.columns:
                        # If target column exists and has nulls, fill from source
                        if target_col in df_enriched.columns:
                            # Fill nulls in target with values from source
                            mask = df_enriched[target_col].isna()
                            df_enriched.loc[mask, target_col] = df_enriched.loc[mask, source_col]
                        else:
                            # Create target column from source
                            df_enriched[target_col] = df_enriched[source_col]
                
                # Apply default values for remaining nulls
                numeric_cols = ['pk_empl', 'fk_centro', 'cod_dan', 'cod_dg', 'cod_dt', 'cod_red']
                text_cols = ['des_centro_ges', 'des_dan', 'des_dg', 'des_dt', 'des_red']
                
                for col in numeric_cols:
                    if col in df_enriched.columns:
                        df_enriched[col] = df_enriched[col].fillna(-1).astype(int)
                
                for col in text_cols:
                    if col in df_enriched.columns:
                        df_enriched[col] = df_enriched[col].fillna("not found")
                
                # Store in session state
                st.session_state['df_enriched'] = df_enriched
                st.session_state['records_updated'] = records_updated
                st.session_state['total_records'] = len(df_enriched)
                
                st.success(f"✅ Data enrichment completed!")
                
            except Exception as e:
                st.error(f"❌ Error during enrichment: {str(e)}")
                logger.error(f"Error during enrichment: {e}", exc_info=True)
                import traceback
                st.code(traceback.format_exc())
                return
    
    # Display preview and confirmation
    if 'df_enriched' in st.session_state:
        df_enriched = st.session_state['df_enriched']
        records_updated = st.session_state['records_updated']
        total_records = st.session_state['total_records']
        
        st.subheader("📋 Enrichment Summary")
        st.markdown(f"**Total records**: {total_records}")
        st.markdown(f"**Records updated**: {records_updated}")
        
        # Show sample of enriched data (name + all target columns 27-37)
        display_cols = ['name', 'pk_empl', 'fk_centro', 'des_centro_ges', 'cod_dan', 'des_dan', 
                        'cod_dg', 'des_dg', 'cod_dt', 'des_dt', 'cod_red', 'des_red']
        available_display_cols = [col for col in display_cols if col in df_enriched.columns]
        
        st.markdown("### Sample of Enriched Data (First 10 rows)")
        st.dataframe(df_enriched[available_display_cols].head(10), height=300)
        
        # Show duplicate warnings if any
        if 'duplicates_emp' in st.session_state:
            duplicates_emp = st.session_state['duplicates_emp']
            st.warning(f"⚠️ Found {len(duplicates_emp.groupby('id'))} records with duplicate employee matches (using match with valid work center)")
            st.dataframe(duplicates_emp, height=200)
        
        if 'duplicates_wc' in st.session_state:
            duplicates_wc = st.session_state['duplicates_wc']
            st.warning(f"⚠️ Found {len(duplicates_wc.groupby('id'))} records with duplicate work center matches (using match with valid data)")
            st.dataframe(duplicates_wc, height=200)
        
        # Count remaining nulls after enrichment
        remaining_nulls = 0
        for col in target_columns:
            if col in df_enriched.columns:
                remaining_nulls += df_enriched[col].isna().sum()
        
        if remaining_nulls == 0:
            st.success("✅ No null values remaining after enrichment!")
        else:
            st.warning(f"⚠️ {remaining_nulls} null values remaining (will be filled with defaults)")
        
        # Confirmation
        st.warning("⚠️ **This action will modify the main Excel file. Please confirm to proceed.**")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("✅ Confirm & Save", type="primary"):
                with st.spinner("Saving enriched data..."):
                    success = save_enriched_data(df_enriched, config)
                    if success:
                        st.success(f"✅ Successfully updated {records_updated} records!")
                        # Update session state
                        st.session_state['df'] = df_enriched
                        # Clear enrichment session state
                        del st.session_state['df_enriched']
                        del st.session_state['records_updated']
                        del st.session_state['total_records']
                        if 'duplicates_emp' in st.session_state:
                            del st.session_state['duplicates_emp']
                        if 'duplicates_wc' in st.session_state:
                            del st.session_state['duplicates_wc']
                        st.balloons()
                        st.rerun()
        with col2:
            if st.button("❌ Cancel"):
                # Clear session state
                del st.session_state['df_enriched']
                del st.session_state['records_updated']
                del st.session_state['total_records']
                if 'duplicates_emp' in st.session_state:
                    del st.session_state['duplicates_emp']
                if 'duplicates_wc' in st.session_state:
                    del st.session_state['duplicates_wc']
                st.info("Enrichment cancelled")
                st.rerun()


def concatenate_name(first_name, last_name1, last_name2):
    """
    Concatenate employee names with single spaces, avoiding double spaces.
    Trim trailing spaces if second last name is missing.
    """
    parts = []
    
    if pd.notna(first_name) and str(first_name).strip():
        parts.append(str(first_name).strip())
    
    if pd.notna(last_name1) and str(last_name1).strip():
        parts.append(str(last_name1).strip())
    
    if pd.notna(last_name2) and str(last_name2).strip():
        parts.append(str(last_name2).strip())
    
    return ' '.join(parts)


def save_enriched_data(df_enriched, config):
    """
    Save enriched data back to Excel file.
    Uses atomic write pattern (temp file + replace).
    """
    import tempfile
    import os
    
    try:
        excel_path = config['excel_path']
        sheet = config['excel_interpreter_spec']['sheet_name']
        excel_spec = config['excel_interpreter_spec']
        
        # Load full Excel with header
        full_df = pd.read_excel(excel_path, sheet_name=sheet, header=0, engine='openpyxl')
        
        # Get column mapping from config (column_id -> column index)
        column_id_to_index = {col['column_id']: col['column'] for col in excel_spec['columns'] if col['column_id'] != 'skip'}
        
        # Get list of column_ids that we should update
        expected_column_ids = list(column_id_to_index.keys())
        
        # Only update columns that exist in both df_enriched and the config
        for col_id in expected_column_ids:
            if col_id in df_enriched.columns:
                col_index = column_id_to_index[col_id]
                if col_index < len(full_df.columns):
                    # Ensure same length
                    if len(df_enriched) == len(full_df):
                        full_df.iloc[:, col_index] = df_enriched[col_id].values
                    else:
                        st.error(f"⚠️ Row count mismatch: enriched={len(df_enriched)}, original={len(full_df)}")
                        return False
        
        # Write to temporary file first (atomic write)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx', dir=os.path.dirname(excel_path)) as tmp_file:
            tmp_path = tmp_file.name
            with pd.ExcelWriter(tmp_path, engine='openpyxl') as writer:
                full_df.to_excel(writer, sheet_name=sheet, index=False)
        
        # Atomically replace the original file
        os.replace(tmp_path, excel_path)
        
        logger.info(f"✅ Saved enriched data successfully")
        return True
        
    except Exception as e:
        st.error(f"❌ Error saving data: {e}")
        logger.error(f"Error saving enriched data: {e}")
        import traceback
        st.code(traceback.format_exc())
        return False
