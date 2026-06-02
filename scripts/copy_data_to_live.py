import os
import shutil
import re

base_dir = os.path.dirname(__file__)
exercises_dir = os.path.join(base_dir, '..', 'exercises')
live_dir = os.path.join(base_dir, '..', 'live')
slideshow_file = os.path.join(base_dir, '..', 'slideshow', 'slideshow_es.html')

# Delete live folder if exists
if os.path.exists(live_dir):
    shutil.rmtree(live_dir)

os.makedirs(live_dir, exist_ok=True)

# Extract exercise order from slideshow
exercise_order = []
with open(slideshow_file, 'r', encoding='utf-8') as f:
    content = f.read()
    # Find all image lines
    matches = re.findall(r'image: "assets/([^"]+)\.jpg"', content)
    for match in matches:
        folder_name = match
        if folder_name.startswith('bonus_'):
            folder_name = folder_name.replace('bonus_', '')
            
        exercise_order.append(folder_name)

# Define display names for specific folder names (keys are FOLDER names)
display_names = {
    'intro_python': 'Intro_Hello_World',
    'etl_merger': 'The_Great_Merger',
    'etl_detective': 'The_Detective',
    'etl_survey': 'The_Messy_Survey',
    'viz_managers_chart': 'The_Managers_Chart',
    'viz_report_generator': 'The_Report_Generator',
    'auto_excel_polish': 'The_Professional_Polish',
    'auto_file_organizer': 'The_File_Organizer',
    'etl_bonus_big_data': 'The_Big_Data_Stress_Test',
    'auto_pdf_report': 'Auto_PDF_Report',
    'etl_api_pipeline': 'ETL_API_Pipeline',
    'viz_d3_bar_chart': 'D3_Bar_Chart',
    'viz_d3_force_network': 'D3_Force_Network',
    'viz_geo_heatmap': 'Viz_Geo_Heatmap',
    'viz_interactive_dashboard': 'Interactive_Dashboard',
    'viz_seaborn_scatter': 'Seaborn_Scatter',
    'viz_seaborn_statistical': 'Seaborn_Statistical'
}

# Now, for each exercise in order, if it has data, copy to live with numbered name
for i, exercise in enumerate(exercise_order):
    exercise_path = os.path.join(exercises_dir, exercise)
    if os.path.isdir(exercise_path):
        data_dir = os.path.join(exercise_path, 'data')
        starter_file = os.path.join(exercise_path, 'exercise_starter.md')

        # Check if manual mapping exists
        display_name = display_names.get(exercise, exercise)

        has_data = os.path.exists(data_dir)
        has_starter = os.path.isfile(starter_file)

        if has_data or has_starter:
            numbered_name = f"{i:02d}_{display_name}"
            live_exercise_dir = os.path.join(live_dir, numbered_name)
            os.makedirs(live_exercise_dir, exist_ok=True)
            if has_data:
                shutil.copytree(data_dir, os.path.join(live_exercise_dir, 'data'))
            if has_starter:
                shutil.copy2(starter_file, os.path.join(live_exercise_dir, 'exercise_starter.md'))