import streamlit as st
import pandas as pd

from excel_io import save_dataframe_to_excel
from filters import apply_filters
from fuzzy_search import fuzzy_filter_by_name


# Field configuration
INDICATOR_FIELDS = ['ind_select', 'ind_review', 'ind_1to1', 'ind_share', 'ind_self']
DROPDOWN_FIELDS = ['use_cases', 'place', 'company']
REQUIRED_FIELDS = ['name', 'email', 'phone', 'company', 'place', 'use_cases']


def get_field_config(df):
    """Build field configuration from dataframe."""
    all_fields = [col for col in df.columns if col != 'id']
    regular_fields = [f for f in all_fields if f not in INDICATOR_FIELDS + ['url_1to1']]
    dropdown_fields = DROPDOWN_FIELDS + [f for f in all_fields if f.startswith('nvl')]
    required_fields = [f for f in all_fields if f not in INDICATOR_FIELDS + ['txt_review', 'url_1to1'] and df[f].dtype != 'datetime64[ns]']
    return {
        'all': all_fields,
        'regular': regular_fields,
        'indicators': [f for f in INDICATOR_FIELDS if f in all_fields],
        'dropdown': dropdown_fields,
        'required': required_fields
    }


def validate_field(field_name, value, dtype, is_required=False):
    """Validate a single field value."""
    if is_required and (not value or (isinstance(value, str) and value.strip() == "")):
        return f"Field '{field_name}' is required and cannot be empty."
    if value and not isinstance(value, bool):
        try:
            dtype.type(value)
        except ValueError as e:
            return f"Field '{field_name}': Invalid value '{value}' for type {dtype}: {str(e)}"
    return None


def render_form_field(field, value, key_prefix, df, field_config):
    """Render a single form field based on its type."""
    if field in field_config['indicators']:
        checked = bool(value == 1 or value == '1')
        return st.checkbox(field, value=checked, key=f"{key_prefix}_{field}")
    elif df[field].dtype == 'datetime64[ns]':
        date_value = pd.to_datetime(value).date() if pd.notna(value) else None
        return st.date_input(field, value=date_value, key=f"{key_prefix}_{field}")
    elif field in field_config['dropdown']:
        options = df[field].dropna().unique().tolist()
        current = value if pd.notna(value) else (options[0] if options else "")
        return st.selectbox(field, options, index=options.index(current) if current in options else 0, key=f"{key_prefix}_{field}")
    else:
        current_str = str(value) if pd.notna(value) else ""
        return st.text_input(field, value=current_str, key=f"{key_prefix}_{field}")


def run(df, filters, config):
    """Main data entry interface. Returns modified dataframe."""
    field_config = get_field_config(df)
    
    # Clean up state when switching contexts
    if 'last_tab' not in st.session_state:
        st.session_state['last_tab'] = 'data_entry'
    if st.session_state.get('last_tab') != 'data_entry':
        st.session_state.pop('confirm_delete', None)
        st.session_state.pop('adding_new', None)
        st.session_state['last_tab'] = 'data_entry'
    
    # Apply filters. include_na=True keeps blank/new records (empty filter
    # column) visible so they can be filled in on this editing tab.
    filtered_df = apply_filters(df, filters, include_na=True)

    # Search bar and add button
    col_search, col_add = st.columns([3, 1])
    with col_search:
        search_term = st.text_input("Search by name (fuzzy)", "", key="data_entry_search")
    with col_add:
        st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
        if st.button("Add Manual Record", type="primary", key="data_entry_add_manual"):
            st.session_state['adding_new'] = True
            st.session_state.pop('selected_id', None)
            st.session_state.pop('confirm_delete', None)

    # Fuzzy search
    if search_term:
        filtered_df = fuzzy_filter_by_name(filtered_df, search_term)

    # Sort by name if not searching
    if not search_term:
        filtered_df = filtered_df.sort_values(by='name')

    # Display dataset
    st.subheader(f"Filtered Dataset ({len(filtered_df)} records)")
    display_df = filtered_df[['name'] + [col for col in filtered_df.columns if col != 'name']].sort_values('name')
    
    # Fix Arrow serialization issue: ensure numeric columns with mixed types are properly converted
    for col in display_df.columns:
        if col in ['pk_empl', 'fk_centro', 'cod_dan', 'cod_dg', 'cod_dt', 'cod_red']:
            # Convert to nullable Int64 to handle mixed types/NaN
            display_df[col] = pd.to_numeric(display_df[col], errors='coerce').astype('Int64')
    
    column_config = {'name': st.column_config.Column(pinned=True)}
    event = st.dataframe(display_df, column_config=column_config, height=178, on_select="rerun", selection_mode="single-row", key="data_entry_dataset")
    
    # Handle row selection
    if event.selection.rows:
        selected_row_idx = event.selection.rows[0]
        clicked_row = display_df.iloc[selected_row_idx]
        selected_id = clicked_row['id']
        st.session_state['selected_id'] = selected_id
        # Keep the keyed edit selectbox in sync with the clicked row.
        st.session_state['data_entry_edit_select'] = f"{clicked_row['name']} (ID: {selected_id})"
        st.session_state.pop('adding_new', None)

    # Edit existing record
    if not st.session_state.get('adding_new') and not filtered_df.empty:
        df = render_edit_section(df, filtered_df, config, field_config, search_term)
    elif not st.session_state.get('adding_new'):
        st.subheader("Edit Record")
        st.write("No records to edit.")

    # Add new record
    if st.session_state.get('adding_new'):
        df = render_add_section(df, config, field_config)

    # Display save status
    if st.session_state.get('last_saved', False):
        st.success("Changes saved successfully!")
        st.session_state['last_saved'] = False

    return df


def render_edit_section(df, filtered_df, config, field_config, search_term):
    """Render the edit record section."""
    st.subheader("Edit Record")
    
    # Select record
    record_options = [f"{row['name']} (ID: {row['id']})" for idx, row in filtered_df.iterrows()]
    selected_id = st.session_state.get('selected_id', None)
    if selected_id and selected_id in filtered_df['id'].values:
        default_index = next(i for i, row in enumerate(filtered_df.itertuples()) if row.id == selected_id)
    else:
        default_index = 0 if search_term else None
    
    # Drop a stale selection that no longer matches the current options so the
    # keyed selectbox falls back to default_index instead of raising.
    if st.session_state.get('data_entry_edit_select') not in record_options:
        st.session_state.pop('data_entry_edit_select', None)
    select_kwargs = {'key': 'data_entry_edit_select'}
    if 'data_entry_edit_select' not in st.session_state:
        select_kwargs['index'] = default_index
    selected_record = st.selectbox("Select a record to edit", record_options, **select_kwargs)
    if not selected_record:
        return df
    
    selected_idx = record_options.index(selected_record)
    selected_row = filtered_df.iloc[selected_idx]
    selected_id = selected_row['id']

    # Render form fields in two columns
    col1, col2 = st.columns(2)
    for i, field in enumerate(field_config['regular']):
        col = col1 if i % 2 == 0 else col2
        with col:
            render_form_field(field, selected_row[field], selected_id, df, field_config)
    
    # Indicators in one line
    st.write("Indicators:")
    ind_cols = st.columns(len(field_config['indicators']))
    for i, field in enumerate(field_config['indicators']):
        with ind_cols[i]:
            checked = bool(selected_row[field] == 1 or selected_row[field] == '1')
            st.checkbox(field, value=checked, key=f"{selected_id}_{field}")
    
    # URL field in full line, clickable
    if 'url_1to1' in df.columns:
        url_value = str(selected_row['url_1to1']) if pd.notna(selected_row['url_1to1']) else ""
        st.text_input("url_1to1", value=url_value, key=f"{selected_id}_url_1to1")
        if url_value:
            st.markdown(f"[open link]({url_value})")

    # Delete record button
    if st.button("Delete Record", type="secondary", key="data_entry_delete"):
        st.session_state['confirm_delete'] = True
    
    if st.session_state.get('confirm_delete'):
        st.error("Are you sure you want to delete this record?")
        col_conf, col_cancel = st.columns(2)
        with col_conf:
            if st.button("Confirm Delete", key="data_entry_confirm_delete"):
                idx = df[df['id'] == selected_id].index[0]
                df = df.drop(idx).reset_index(drop=True)
                save_dataframe_to_excel(df, config)
                st.session_state['df'] = df
                st.session_state.pop('confirm_delete', None)
                st.session_state.pop('selected_id', None)
                st.session_state['last_saved'] = True
                st.rerun()
        with col_cancel:
            if st.button("Cancel", key="data_entry_cancel_delete"):
                st.session_state.pop('confirm_delete', None)

    # Check for changes and save
    if not st.session_state.get('confirm_delete'):
        has_changes = check_changes(selected_row, selected_id, field_config)
        if has_changes:
            if st.button("Save Changes", key="data_entry_save_changes"):
                df = save_record_changes(df, selected_row, selected_id, field_config, config)
                st.session_state['df'] = df
                st.rerun()
    
    return df


def render_add_section(df, config, field_config):
    """Render the add new record section."""
    st.subheader("Add New Record")
    
    with st.form("add_record_form"):
        col1, col2 = st.columns(2)
        inputs = {}
        
        # Render all fields
        for i, field in enumerate(field_config['all']):
            col = col1 if i % 2 == 0 else col2
            with col:
                if field in field_config['indicators']:
                    inputs[field] = st.checkbox(field, key=f"add_{field}")
                elif df[field].dtype == 'datetime64[ns]':
                    inputs[field] = st.date_input(field, key=f"add_{field}")
                elif field in field_config['dropdown']:
                    options = df[field].dropna().unique().tolist()
                    inputs[field] = st.selectbox(field, options, key=f"add_{field}")
                else:
                    inputs[field] = st.text_input(field, key=f"add_{field}")
        
        col_submit, col_cancel = st.columns(2)
        with col_submit:
            submitted = st.form_submit_button("Add Record", type="primary", key="data_entry_add_submit")
        with col_cancel:
            cancelled = st.form_submit_button("Cancel", type="secondary", key="data_entry_add_cancel")
        
        if cancelled:
            st.session_state.pop('adding_new', None)
            st.rerun()
        
        if submitted:
            # Validate all fields
            validation_errors = []
            for field in field_config['all']:
                if field not in field_config['indicators']:
                    is_required = field in field_config['required']
                    error = validate_field(field, inputs[field], df[field].dtype, is_required)
                    if error:
                        validation_errors.append(error)
            
            if validation_errors:
                for error in validation_errors:
                    st.error(error)
            else:
                # Create new record
                new_id = df['id'].max() + 1 if not df.empty else 1
                new_row = {'id': new_id}
                for field in field_config['all']:
                    if field in field_config['indicators']:
                        new_row[field] = 1 if inputs[field] else 0
                    elif df[field].dtype == 'datetime64[ns]':
                        # Convert date to pandas datetime
                        new_row[field] = pd.to_datetime(inputs[field]) if inputs[field] else pd.NaT
                    else:
                        new_row[field] = inputs[field]
                
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_dataframe_to_excel(df, config)
                st.session_state['df'] = df
                st.session_state.pop('adding_new', None)
                st.session_state['last_saved'] = True
                st.success("New record added!")
                st.rerun()
    
    return df


def check_changes(selected_row, selected_id, field_config):
    """Check if any field has been modified."""
    all_fields = field_config['all'] + (['url_1to1'] if 'url_1to1' not in field_config['all'] else [])
    for field in all_fields:
        key = f"{selected_id}_{field}"
        if key in st.session_state:
            current_session_value = st.session_state[key]
            original_value = selected_row[field]
            if field in field_config['indicators']:
                original_bool = bool(original_value == 1 or original_value == '1')
                if current_session_value != original_bool:
                    return True
            else:
                original_str = str(original_value) if pd.notna(original_value) else ""
                if current_session_value != original_str:
                    return True
    return False


def save_record_changes(df, selected_row, selected_id, field_config, config):
    """Save changes for a single record."""
    all_fields = field_config['all'] + (['url_1to1'] if 'url_1to1' not in field_config['all'] else [])
    validation_errors = []
    
    # Validate all values before updating
    for field in all_fields:
        key = f"{selected_id}_{field}"
        if key in st.session_state:
            new_value = st.session_state[key]
            if field not in field_config['indicators']:
                error = validate_field(field, new_value, df[field].dtype)
                if error:
                    validation_errors.append(error)
    
    if validation_errors:
        for error in validation_errors:
            st.error(error)
        return df
    
    # Update df with all current values
    idx = df[df['id'] == selected_id].index[0]
    for field in all_fields:
        key = f"{selected_id}_{field}"
        if key in st.session_state:
            new_value = st.session_state[key]
            if field in field_config['indicators']:
                new_value = int(1 if new_value else 0)
            elif df[field].dtype == 'datetime64[ns]':
                # Convert date to pandas datetime
                new_value = pd.to_datetime(new_value) if new_value else pd.NaT
            df.at[idx, field] = new_value
    
    save_dataframe_to_excel(df, config)
    st.session_state['last_saved'] = True
    return df
