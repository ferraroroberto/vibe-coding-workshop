import streamlit as st
import pandas as pd
import json
import plotly.express as px
from collections import Counter

def run(df, filters, config):

    # Apply filters to df
    filtered_df = df.copy()
    for col, selected in filters.items():
        if selected and col in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[col].isin(selected)]

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

    # Pie charts in two columns
    col1, col2 = st.columns(2)

    with col1:
        company_df = filtered_df['company'].value_counts().reset_index()
        company_df.columns = ['company', 'count']
        company_df = company_df.sort_values('count', ascending=False)
        total_company = company_df['count'].sum()
        company_df['percentage'] = company_df['count'] / total_company
        main_company = company_df[company_df['percentage'] >= 0.01]
        rest_count = company_df[company_df['percentage'] < 0.01]['count'].sum()
        if rest_count > 0:
            rest_df = pd.DataFrame({'company': ['Other'], 'count': [rest_count], 'percentage': [rest_count / total_company]})
            company_df = pd.concat([main_company, rest_df], ignore_index=True)
        else:
            company_df = main_company
        n_company = len(company_df)
        company_colors = ['#1E88E5']  # Top is blue
        for i in range(1, n_company):
            if n_company > 2:
                factor = (i - 1) / (n_company - 2)
            else:
                factor = 0
            gray = int(217 + (64 - 217) * factor)  # From #D9D9D9 (217) to #404040 (64)
            company_colors.append(f'rgb({gray},{gray},{gray})')
        company_color_map = dict(zip(company_df['company'], company_colors))
        fig1 = px.pie(company_df, values='count', names='company', title='Breakdown by Company', color='company', color_discrete_map=company_color_map)
        st.plotly_chart(fig1, width='stretch')

    with col2:
        place_df = filtered_df['place'].value_counts().reset_index()
        place_df.columns = ['place', 'count']
        place_df = place_df.sort_values('count', ascending=False)
        total_place = place_df['count'].sum()
        place_df['percentage'] = place_df['count'] / total_place
        main_place = place_df[place_df['percentage'] >= 0.01]
        rest_count = place_df[place_df['percentage'] < 0.01]['count'].sum()
        if rest_count > 0:
            rest_df = pd.DataFrame({'place': ['Other'], 'count': [rest_count], 'percentage': [rest_count / total_place]})
            place_df = pd.concat([main_place, rest_df], ignore_index=True)
        else:
            place_df = main_place
        n_place = len(place_df)
        place_colors = ['#1E88E5']  # Top is blue
        for i in range(1, n_place):
            if n_place > 2:
                factor = (i - 1) / (n_place - 2)
            else:
                factor = 0
            gray = int(217 + (64 - 217) * factor)  # From #D9D9D9 (217) to #404040 (64)
            place_colors.append(f'rgb({gray},{gray},{gray})')
        place_color_map = dict(zip(place_df['place'], place_colors))
        fig2 = px.pie(place_df, values='count', names='place', title='Breakdown by Place', color='place', color_discrete_map=place_color_map)
        st.plotly_chart(fig2, width='stretch')

    # Additional pie charts
    col1, col2 = st.columns(2)

    with col1:
        dt_df = filtered_df['des_dt'].value_counts().reset_index()
        dt_df.columns = ['des_dt', 'count']
        dt_df = dt_df.sort_values('count', ascending=False)
        total_dt = dt_df['count'].sum()
        dt_df['percentage'] = dt_df['count'] / total_dt
        main_dt = dt_df[dt_df['percentage'] >= 0.03]  # Change threshold to 3%
        rest_count = dt_df[dt_df['percentage'] < 0.03]['count'].sum()  # Change threshold to 3%
        if rest_count > 0:
            rest_df = pd.DataFrame({'des_dt': ['Other'], 'count': [rest_count], 'percentage': [rest_count / total_dt]})
            dt_df = pd.concat([main_dt, rest_df], ignore_index=True)
        else:
            dt_df = main_dt
        dt_df['des_dt'] = dt_df['des_dt'].str.lower()
        n_dt = len(dt_df)
        dt_colors = ['#1E88E5']  # Top is blue
        for i in range(1, n_dt):
            if n_dt > 2:
                factor = (i - 1) / (n_dt - 2)
            else:
                factor = 0
            gray = int(217 + (64 - 217) * factor)  # From #D9D9D9 (217) to #404040 (64)
            dt_colors.append(f'rgb({gray},{gray},{gray})')
        dt_color_map = dict(zip(dt_df['des_dt'], dt_colors))
        fig3 = px.pie(dt_df, values='count', names='des_dt', title='Breakdown by N+3(dt)', color='des_dt', color_discrete_map=dt_color_map)
        st.plotly_chart(fig3, width='stretch')

    with col2:
        dg_df = filtered_df['des_dg'].value_counts().reset_index()
        dg_df.columns = ['des_dg', 'count']
        dg_df = dg_df.sort_values('count', ascending=False)
        total_dg = dg_df['count'].sum()
        dg_df['percentage'] = dg_df['count'] / total_dg
        main_dg = dg_df[dg_df['percentage'] >= 0.03]  # Change threshold to 3%
        rest_count = dg_df[dg_df['percentage'] < 0.03]['count'].sum()  # Change threshold to 3%
        if rest_count > 0:
            rest_df = pd.DataFrame({'des_dg': ['Other'], 'count': [rest_count], 'percentage': [rest_count / total_dg]})
            dg_df = pd.concat([main_dg, rest_df], ignore_index=True)
        else:
            dg_df = main_dg
        dg_df['des_dg'] = dg_df['des_dg'].str.lower()
        n_dg = len(dg_df)
        dg_colors = ['#1E88E5']  # Top is blue
        for i in range(1, n_dg):
            if n_dg > 2:
                factor = (i - 1) / (n_dg - 2)
            else:
                factor = 0
            gray = int(217 + (64 - 217) * factor)  # From #D9D9D9 (217) to #404040 (64)
            dg_colors.append(f'rgb({gray},{gray},{gray})')
        dg_color_map = dict(zip(dg_df['des_dg'], dg_colors))
        fig4 = px.pie(dg_df, values='count', names='des_dg', title='Breakdown by N+2(dg)', color='des_dg', color_discrete_map=dg_color_map)
        st.plotly_chart(fig4, width='stretch')

    col1, col2 = st.columns(2)

    with col1:
        dan_df = filtered_df['des_dan'].value_counts().reset_index()
        dan_df.columns = ['des_dan', 'count']
        dan_df = dan_df.sort_values('count', ascending=False)
        total_dan = dan_df['count'].sum()
        dan_df['percentage'] = dan_df['count'] / total_dan
        main_dan = dan_df[dan_df['percentage'] >= 0.03]  # Change threshold to 3%
        rest_count = dan_df[dan_df['percentage'] < 0.03]['count'].sum()  # Change threshold to 3%
        if rest_count > 0:
            rest_df = pd.DataFrame({'des_dan': ['Other'], 'count': [rest_count], 'percentage': [rest_count / total_dan]})
            dan_df = pd.concat([main_dan, rest_df], ignore_index=True)
        else:
            dan_df = main_dan
        dan_df['des_dan'] = dan_df['des_dan'].str.lower()
        n_dan = len(dan_df)
        dan_colors = ['#1E88E5']  # Top is blue
        for i in range(1, n_dan):
            if n_dan > 2:
                factor = (i - 1) / (n_dan - 2)
            else:
                factor = 0
            gray = int(217 + (64 - 217) * factor)  # From #D9D9D9 (217) to #404040 (64)
            dan_colors.append(f'rgb({gray},{gray},{gray})')
        dan_color_map = dict(zip(dan_df['des_dan'], dan_colors))
        fig5 = px.pie(dan_df, values='count', names='des_dan', title='Breakdown by N+1(dan)', color='des_dan', color_discrete_map=dan_color_map)
        st.plotly_chart(fig5, width='stretch')

    with col2:
        centro_df = filtered_df['des_centro_ges'].value_counts().reset_index()
        centro_df.columns = ['des_centro_ges', 'count']
        centro_df = centro_df.sort_values('count', ascending=False)
        total_centro = centro_df['count'].sum()
        centro_df['percentage'] = centro_df['count'] / total_centro
        main_centro = centro_df[centro_df['percentage'] >= 0.03]  # Change threshold to 3%
        rest_count = centro_df[centro_df['percentage'] < 0.03]['count'].sum()  # Change threshold to 3%
        if rest_count > 0:
            rest_df = pd.DataFrame({'des_centro_ges': ['Other'], 'count': [rest_count], 'percentage': [rest_count / total_centro]})
            centro_df = pd.concat([main_centro, rest_df], ignore_index=True)
        else:
            centro_df = main_centro
        centro_df['des_centro_ges'] = centro_df['des_centro_ges'].str.lower()
        n_centro = len(centro_df)
        centro_colors = ['#1E88E5']  # Top is blue
        for i in range(1, n_centro):
            if n_centro > 2:
                factor = (i - 1) / (n_centro - 2)
            else:
                factor = 0
            gray = int(217 + (64 - 217) * factor)  # From #D9D9D9 (217) to #404040 (64)
            centro_colors.append(f'rgb({gray},{gray},{gray})')
        centro_color_map = dict(zip(centro_df['des_centro_ges'], centro_colors))
        fig6 = px.pie(centro_df, values='count', names='des_centro_ges', title='Breakdown by center', color='des_centro_ges', color_discrete_map=centro_color_map)
        st.plotly_chart(fig6, width='stretch')

    # Process use_cases: split by ';'
    use_cases_all = []
    for uc in filtered_df['use_cases'].dropna():
        use_cases_all.extend([item.strip() for item in uc.split(';') if item.strip()])

    use_cases_counts = Counter(use_cases_all)

    # Vertical bar chart for use_cases
    use_cases_df = pd.DataFrame(list(use_cases_counts.items()), columns=['use_case', 'count'])
    use_cases_df = use_cases_df.sort_values('count', ascending=False)
    total_use = use_cases_df['count'].sum()
    use_cases_df['percentage'] = use_cases_df['count'] / total_use
    main_use = use_cases_df[use_cases_df['percentage'] >= 0.01]
    rest_count = use_cases_df[use_cases_df['percentage'] < 0.01]['count'].sum()
    if rest_count > 0:
        rest_df = pd.DataFrame({'use_case': ['Other'], 'count': [rest_count], 'percentage': [rest_count / total_use]})
        use_cases_df = pd.concat([main_use, rest_df], ignore_index=True)
    else:
        use_cases_df = main_use
    n_use = len(use_cases_df)
    use_colors = ['#1E88E5']  # Top is blue
    for i in range(1, n_use):
        if n_use > 2:
            factor = (i - 1) / (n_use - 2)
        else:
            factor = 0
        gray = int(217 + (64 - 217) * factor)  # From #D9D9D9 (217) to #404040 (64)
        use_colors.append(f'rgb({gray},{gray},{gray})')
    use_color_map = dict(zip(use_cases_df['use_case'], use_colors))
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