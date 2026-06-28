import streamlit as st
import pandas as pd
import json
import plotly.express as px
from collections import Counter

from charts import build_breakdown_pie, collapse_to_other, grey_ramp
from filters import apply_filters

def run(df, filters, config):

    # Apply filters. include_na=False drops blank rows so the dashboard's
    # aggregate metrics only count records that match the selected value.
    filtered_df = apply_filters(df, filters, include_na=False)

    # Title
    st.title("Survey Data Dashboard")

    # Phase 1 Metrics
    st.markdown("### 📊 Phase 1 Overview")
    total_responses = len(filtered_df)
    unique_companies = filtered_df['company'].nunique()
    unique_places = filtered_df['place'].nunique()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Responses", total_responses)

    with col2:
        st.metric("Unique Companies", unique_companies)

    with col3:
        st.metric("Unique Places", unique_places)
    
    # Phase 2 Metrics
    st.markdown("### 🎯 Phase 2 Overview")
    render_phase2_metrics(filtered_df)
    
    st.markdown("---")

    # Breakdown pie charts, two per row. Company/place use a 1% "Other" cutoff;
    # the hierarchy breakdowns use 3% and lower-case their labels.
    pie_specs = [
        {'column': 'company', 'threshold': 0.01, 'title': 'Breakdown by Company', 'lowercase': False},
        {'column': 'place', 'threshold': 0.01, 'title': 'Breakdown by Place', 'lowercase': False},
        {'column': 'des_dt', 'threshold': 0.03, 'title': 'Breakdown by N+3(dt)', 'lowercase': True},
        {'column': 'des_dg', 'threshold': 0.03, 'title': 'Breakdown by N+2(dg)', 'lowercase': True},
        {'column': 'des_dan', 'threshold': 0.03, 'title': 'Breakdown by N+1(dan)', 'lowercase': True},
        {'column': 'des_centro_ges', 'threshold': 0.03, 'title': 'Breakdown by center', 'lowercase': True},
    ]

    for row_start in range(0, len(pie_specs), 2):
        cols = st.columns(2)
        for col, spec in zip(cols, pie_specs[row_start:row_start + 2]):
            with col:
                fig = build_breakdown_pie(
                    filtered_df,
                    spec['column'],
                    spec['threshold'],
                    spec['title'],
                    lowercase=spec['lowercase'],
                )
                st.plotly_chart(fig, width='stretch')

    # Process use_cases: split by ';'
    use_cases_all = []
    for uc in filtered_df['use_cases'].dropna():
        use_cases_all.extend([item.strip() for item in uc.split(';') if item.strip()])

    use_cases_counts = Counter(use_cases_all)

    # Vertical bar chart for use_cases
    use_cases_df = pd.DataFrame(list(use_cases_counts.items()), columns=['use_case', 'count'])
    use_cases_df = collapse_to_other(use_cases_df, 'use_case', 0.01)
    use_color_map = dict(zip(use_cases_df['use_case'], grey_ramp(len(use_cases_df))))
    fig3 = px.bar(use_cases_df, x='count', y='use_case', title='Use Cases Breakdown', color='use_case', color_discrete_map=use_color_map, orientation='h', labels={'use_case': ''})
    st.plotly_chart(fig3, width='stretch')

    # Distribution of nvl_ fields
    st.subheader("Distribution of Skill Levels")
    nvl_fields = ['nvl_excel', 'nvl_python', 'nvl_sas', 'nvl_sql', 'nvl_vba']
    labels = [
        "nunca lo he utilizado",
        "alguna base",
        "usuario habitual",
        "usuario experto",
        "usuario avanzado"
    ]
    distribution = pd.DataFrame(index=labels, columns=nvl_fields)
    for field in nvl_fields:
        counts = filtered_df[field].value_counts()
        for label in labels:
            distribution.loc[label, field] = counts.get(label, 0)
    # Friendly column names for visualization
    friendly_names = {
        'nvl_excel': 'Excel skill',
        'nvl_python': 'Python skill',
        'nvl_sas': 'SAS skill',
        'nvl_sql': 'SQL skill',
        'nvl_vba': 'VBA skill'
    }
    distribution_display = distribution.rename(columns=friendly_names)
    # Heatmap styling: black to accent blue (#1E88E5)
    def blue_heatmap(val, min_val, max_val):
        if pd.isna(val):
            return ''
        # Normalize value between 0 and 1
        norm = 0 if max_val == min_val else (val - min_val) / (max_val - min_val)
        # Interpolate between black and blue
        r = int(30 * norm)
        g = int(136 * norm)
        b = int(229 * norm)
        return f'background-color: rgb({r},{g},{b}); color: white' if val > 0 else ''

    def style_heatmap(df):
        styled = df.copy()
        min_max = {col: (df[col].min(), df[col].max()) for col in df.columns}
        def style_func(val, col):
            min_val, max_val = min_max[col]
            return blue_heatmap(val, min_val, max_val)
        return df.style.apply(lambda col: [style_func(v, col.name) for v in col], axis=0)

    st.dataframe(style_heatmap(distribution_display))

    # Full dataset table
    st.subheader(f"Filtered Dataset ({len(filtered_df)} records)")
    # Reorder columns to put 'name' first
    filtered_df_display = filtered_df[['name'] + [col for col in filtered_df.columns if col != 'name']].sort_values('name')
    # Configure 'name' column to be pinned (fixed when scrolling)
    column_config = {
        'name': st.column_config.Column(pinned=True)
    }
    st.dataframe(filtered_df_display, column_config=column_config, width='stretch')
    # Export filtered result to XLS
    import io

    output = io.BytesIO()
    if st.button("Export filtered result to XLS"):
        # Build filters summary from filters dict
        filters_summary = []
        for col in filters:
            selected = filters[col]
            unique_vals = sorted(df[col].dropna().unique())
            if set(selected) == set(unique_vals):
                selected_str = 'All'
            else:
                selected_str = ', '.join(map(str, selected))
            filters_summary.append({'Filter': col, 'Selected': selected_str})
        filters_df = pd.DataFrame(filters_summary)
        # Write DataFrame to Excel in memory
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            filtered_df.to_excel(writer, index=False, sheet_name='FilteredData')
            filters_df.to_excel(writer, index=False, sheet_name='FiltersApplied')
        output.seek(0)
        st.download_button(
            label="Download XLS file",
            data=output,
            file_name="filtered_result.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


def render_phase2_metrics(filtered_df):
    """Render Phase 2 selection metrics and summary."""
    # Check if Phase 2 columns exist
    phase2_cols = ['ind_confirm', 'ind_session', 'ind_waitlist']
    has_phase2 = all(col in filtered_df.columns for col in phase2_cols)
    
    if not has_phase2:
        st.info("ℹ️ Phase 2 data not available. Use 'Phase 2 Sync' tab to import data.")
        return
    
    # Ensure ind_confirm is numeric with no NULLs
    filtered_df_clean = filtered_df.copy()
    if 'ind_confirm' in filtered_df_clean.columns:
        filtered_df_clean['ind_confirm'] = pd.to_numeric(filtered_df_clean['ind_confirm'], errors='coerce').fillna(0).astype(int)
    if 'ind_session' in filtered_df_clean.columns:
        filtered_df_clean['ind_session'] = pd.to_numeric(filtered_df_clean['ind_session'], errors='coerce').fillna(0).astype(int)
    if 'ind_waitlist' in filtered_df_clean.columns:
        filtered_df_clean['ind_waitlist'] = pd.to_numeric(filtered_df_clean['ind_waitlist'], errors='coerce').fillna(0).astype(int)
    
    # Calculate metrics
    total = len(filtered_df_clean)
    confirmed = (filtered_df_clean['ind_confirm'] == 1).sum()
    selected = (filtered_df_clean['ind_session'] == 1).sum()
    waitlist = (filtered_df_clean['ind_waitlist'] == 1).sum()
    pending = confirmed - selected - waitlist
    
    # Display metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Phase 2 Confirmed",
            confirmed,
            delta=f"{confirmed/total*100:.1f}% of total" if total > 0 else None,
            delta_color="off"
        )
    
    with col2:
        st.metric(
            "Selected for Session",
            selected,
            delta=f"{selected/confirmed*100:.1f}% of confirmed" if confirmed > 0 else None,
            delta_color="off"
        )
    
    with col3:
        st.metric(
            "Waitlist",
            waitlist,
            delta=f"{waitlist/confirmed*100:.1f}% of confirmed" if confirmed > 0 else None,
            delta_color="off"
        )
    
    with col4:
        st.metric(
            "Pending Decision",
            max(0, pending),
            delta="awaiting selection" if pending > 0 else None,
            delta_color="off"
        )
    
    with col5:
        conversion = selected / total * 100 if total > 0 else 0
        st.metric(
            "Conversion Rate",
            f"{conversion:.1f}%",
            delta="Phase 1 → Selected",
            delta_color="off"
        )
    
    # Selection breakdown by hierarchy (if we have confirmed records)
    if confirmed > 0:
        with st.expander("📊 Selection Breakdown by Hierarchy", expanded=False):
            # Ensure ind_confirm is numeric with no NULLs
            filtered_df_hier = filtered_df.copy()
            if 'ind_confirm' in filtered_df_hier.columns:
                filtered_df_hier['ind_confirm'] = pd.to_numeric(filtered_df_hier['ind_confirm'], errors='coerce').fillna(0).astype(int)
            confirmed_df = filtered_df_hier[filtered_df_hier['ind_confirm'] == 1].copy()
            
            hierarchy_cols = [
                ('des_dt', 'N+3 (DT)'),
                ('des_dg', 'N+2 (DG)'),
                ('des_dan', 'N+1 (DAN)')
            ]
            
            for col_name, display_name in hierarchy_cols:
                if col_name not in confirmed_df.columns:
                    continue
                
                st.markdown(f"**{display_name}**")
                
                grouped = confirmed_df.groupby(col_name).agg({
                    'id': 'count',
                    'ind_session': lambda x: (x == 1).sum(),
                    'ind_waitlist': lambda x: (x == 1).sum()
                }).reset_index()
                
                grouped.columns = [display_name, 'Confirmed', 'Selected', 'Waitlist']
                grouped['Pending'] = grouped['Confirmed'] - grouped['Selected'] - grouped['Waitlist']
                grouped['Selection %'] = (grouped['Selected'] / grouped['Confirmed'] * 100).round(1)
                
                # Sort by confirmed count
                grouped = grouped.sort_values('Confirmed', ascending=False).head(10)
                
                st.dataframe(grouped, hide_index=True, width='stretch')