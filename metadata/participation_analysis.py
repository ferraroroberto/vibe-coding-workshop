import streamlit as st
import pandas as pd
import plotly.express as px
import logging
import os

logger = logging.getLogger(__name__)


def run(df, filters, config):
    """
    Participation Analysis Module: Compare survey participation against total employee population.
    
    Process:
    1. Load unfiltered employee and work center data (total population)
    2. Calculate total employees by hierarchy level (DAN, DG, DT)
    3. Apply filters to survey data (participation)
    4. Calculate participation metrics by hierarchy level
    5. Display treemaps with drill-down capability
    """
    st.header("📈 Participation Analysis")
    st.markdown("Compare survey participation rates across organizational hierarchy")
    
    # Extract config
    emp_config = config.get('source_path_employees', {})
    wc_config = config.get('source_path_workcenters', {})
    
    if not emp_config or not wc_config:
        st.error("⚠️ Employee or work center configuration missing in config.json")
        return
    
    # Build file paths
    emp_path = os.path.join(emp_config.get('path', ''), emp_config.get('file', ''))
    wc_path = os.path.join(wc_config.get('path', ''), wc_config.get('file', ''))
    
    # Load unfiltered data (total population)
    try:
        # Load employee data (semicolon separator)
        df_emp = pd.read_csv(emp_path, sep=';', encoding='utf-8')
        emp_keep_cols = emp_config.get('keep', [])
        df_emp = df_emp[emp_keep_cols]
        
        # Load work center data (comma separator)
        df_wc = pd.read_csv(wc_path, sep=',', encoding='utf-8')
        wc_keep_cols = wc_config.get('keep', [])
        df_wc = df_wc[wc_keep_cols]
        
        # Join employee with work center to get hierarchy
        df_total = df_emp.merge(
            df_wc,
            left_on='FK_CENTRO',
            right_on='PK_CENTRO',
            how='left'
        )
        
        logger.info(f"✅ Loaded {len(df_total)} total employees with hierarchy data")
        
    except FileNotFoundError as e:
        st.error(f"❌ File not found: {e}")
        return
    except Exception as e:
        st.error(f"❌ Error loading files: {e}")
        logger.error(f"Error loading source files: {e}")
        return
    
    # Apply filters to survey data (participation)
    filtered_df = df.copy()
    for col, selected in filters.items():
        if selected and col in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[col].isin(selected)]
    
    # Pre-calculate aggregated metrics for overall display
    # We'll aggregate by each hierarchy level to get areas with participants (most aggregate to least)
    hierarchy_levels = ['DAN', 'DG', 'DT']
    all_treemap_data = {}
    
    for level in hierarchy_levels:
        treemap_data = generate_treemap_data(df_total, filtered_df, level)
        if treemap_data is not None and len(treemap_data) > 0:
            # Filter to show only areas with at least 1 participant
            treemap_data = treemap_data[treemap_data['participants'] > 0]
            all_treemap_data[level] = treemap_data
    
    # Calculate overall metrics based on aggregated hierarchy data
    # Use the most granular level with data to avoid double counting
    total_employees = 0
    total_participants = len(filtered_df)
    
    # Find areas with participants at each level and sum their total employees
    # Use DT (most granular with good data coverage) if available, else DG, else DAN
    if 'DT' in all_treemap_data and len(all_treemap_data['DT']) > 0:
        total_employees = all_treemap_data['DT']['total_employees'].sum()
    elif 'DG' in all_treemap_data and len(all_treemap_data['DG']) > 0:
        total_employees = all_treemap_data['DG']['total_employees'].sum()
    elif 'DAN' in all_treemap_data and len(all_treemap_data['DAN']) > 0:
        total_employees = all_treemap_data['DAN']['total_employees'].sum()
    
    overall_participation = (total_participants / total_employees * 100) if total_employees > 0 else 0
    
    # Display overall metrics
    st.markdown("### 📊 Overall Metrics (Areas with Participants)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Employees (in participating areas)", f"{total_employees:,}")
    
    with col2:
        st.metric("Total Participants (Filtered)", f"{total_participants:,}")
    
    with col3:
        st.metric("Overall Participation Rate", f"{overall_participation:.2f}%")
    
    st.markdown("---")
    
    # Display treemaps for all 4 levels simultaneously
    for level in hierarchy_levels:
        if level in all_treemap_data and len(all_treemap_data[level]) > 0:
            display_treemap(all_treemap_data[level], level)
            display_top_areas(all_treemap_data[level], level)
            st.markdown("---")
        else:
            st.warning(f"⚠️ No areas with participants for {level} level")


def generate_treemap_data(df_total, df_participants, level):
    """
    Generate treemap data for a specific hierarchy level.
    
    Args:
        df_total: Unfiltered employee data with hierarchy
        df_participants: Filtered survey data (participants)
        level: Hierarchy level (DAN, DG, DT, RED)
    
    Returns:
        DataFrame with columns: area, total_employees, participants, participation_rate
    """
    # Map level to column names
    level_map = {
        'DAN': ('COD_DAN', 'DES_DAN'),
        'DG': ('COD_DG', 'DES_DG'),
        'DT': ('COD_DT', 'DES_DT')
    }
    
    if level not in level_map:
        return None
    
    cod_col, des_col = level_map[level]
    
    # Calculate total employees by area (unfiltered)
    total_by_area = df_total.groupby(des_col).size().reset_index(name='total_employees')
    
    # Map survey column names (lowercase)
    survey_des_col = des_col.lower()
    
    # Calculate participants by area (filtered survey data)
    if survey_des_col in df_participants.columns:
        participants_by_area = df_participants.groupby(survey_des_col).size().reset_index(name='participants')
        participants_by_area.columns = [des_col, 'participants']
    else:
        # If column not in survey data, no participants
        participants_by_area = pd.DataFrame({des_col: [], 'participants': []})
    
    # Merge total and participants
    treemap_data = total_by_area.merge(
        participants_by_area,
        on=des_col,
        how='left'
    )
    
    # Fill missing participants with 0
    treemap_data['participants'] = treemap_data['participants'].fillna(0).astype(int)
    
    # Calculate participation rate
    treemap_data['participation_rate'] = (
        treemap_data['participants'] / treemap_data['total_employees'] * 100
    ).round(2)
    
    # Rename area column
    treemap_data = treemap_data.rename(columns={des_col: 'area'})
    
    # Clean area names (lowercase for consistency)
    treemap_data['area'] = treemap_data['area'].str.lower()
    
    # Remove rows with null area
    treemap_data = treemap_data[treemap_data['area'].notna()]
    
    # Sort by total employees (descending)
    treemap_data = treemap_data.sort_values('total_employees', ascending=False)
    
    return treemap_data


def display_treemap(treemap_data, level):
    """
    Display treemap visualization with size=total employees and color=participation rate.
    """
    # Map level to display label
    level_labels = {
        'DT': 'N+3(dt)',
        'DG': 'N+2(dg)',
        'DAN': 'N+1(dan)'
    }
    display_label = level_labels.get(level, level)
    st.markdown(f"### 🗺️ Treemap: {display_label}")
    
    # Create custom labels
    treemap_data['label'] = treemap_data.apply(
        lambda row: f"{row['area']}<br>{row['participants']}/{row['total_employees']} ({row['participation_rate']}%)",
        axis=1
    )
    
    # Generate color based on participation rate (blue for top, grey shades for rest)
    treemap_data_sorted = treemap_data.sort_values('participation_rate', ascending=False).reset_index(drop=True)
    
    n_areas = len(treemap_data_sorted)
    color_map = {}
    
    if n_areas > 0:
        # Top area gets blue
        color_map[treemap_data_sorted.iloc[0]['area']] = '#1E88E5'
        
        # Rest get grey shades from light to dark
        for i in range(1, n_areas):
            if n_areas > 2:
                factor = i / (n_areas - 1)
            else:
                factor = 1
            gray = int(217 + (64 - 217) * factor)  # From #D9D9D9 (217) to #404040 (64)
            color_map[treemap_data_sorted.iloc[i]['area']] = f'rgb({gray},{gray},{gray})'
    
    # Create treemap
    fig = px.treemap(
        treemap_data,
        path=['area'],
        values='total_employees',
        color='participation_rate',
        color_discrete_map=color_map,
        hover_data={
            'area': False,
            'total_employees': ':,',
            'participants': ':,',
            'participation_rate': ':.2f'
        },
        labels={
            'total_employees': 'Total Employees',
            'participants': 'Participants',
            'participation_rate': 'Participation Rate (%)'
        }
    )
    
    # Update layout
    fig.update_traces(
        textinfo='label',
        textfont_size=12,
        marker=dict(line=dict(width=2, color='white'))
    )
    
    fig.update_layout(
        height=600,
        margin=dict(t=10, l=10, r=10, b=10)
    )
    
    st.plotly_chart(fig, width='stretch', key=f"treemap_{level}")


def display_top_areas(treemap_data, level):
    """
    Display top areas by participation rate and absolute participation.
    """
    # Map level to display label
    level_labels = {
        'DT': 'N+3(dt)',
        'DG': 'N+2(dg)',
        'DAN': 'N+1(dan)'
    }
    display_label = level_labels.get(level, level)
    st.markdown(f"### 🏆 Top Areas by Participation {display_label}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Top 5 by Participation Rate**")
        top_rate = treemap_data.sort_values('participation_rate', ascending=False).head(5)
        
        for idx, row in top_rate.iterrows():
            st.markdown(
                f"**{row['area'].title()}**: {row['participation_rate']:.2f}% "
                f"({row['participants']}/{row['total_employees']})"
            )
    
    with col2:
        st.markdown("**Top 5 by Absolute Participation**")
        top_abs = treemap_data.sort_values('participants', ascending=False).head(5)
        
        for idx, row in top_abs.iterrows():
            st.markdown(
                f"**{row['area'].title()}**: {row['participants']} participants "
                f"({row['participation_rate']:.2f}% of {row['total_employees']})"
            )
    
    st.markdown("---")
    
    # Show full data table
    with st.expander("📋 View Full Data Table"):
        display_data = treemap_data.copy()
        display_data['area'] = display_data['area'].str.title()
        display_data = display_data.sort_values('participation_rate', ascending=False)
        
        st.dataframe(
            display_data[['area', 'total_employees', 'participants', 'participation_rate']],
            hide_index=True,
            width='stretch',
            column_config={
                'area': st.column_config.TextColumn('Area', width='medium'),
                'total_employees': st.column_config.NumberColumn('Total Employees', format='%d'),
                'participants': st.column_config.NumberColumn('Participants', format='%d'),
                'participation_rate': st.column_config.NumberColumn('Participation Rate (%)', format='%.2f%%')
            }
        )
