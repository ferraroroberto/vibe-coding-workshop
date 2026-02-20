import os
import shutil
import re

base_dir = os.path.dirname(__file__)
exercises_dir = os.path.join(base_dir, 'exercises')
live_dir = os.path.join(base_dir, 'live')
slideshow_file = os.path.join(base_dir, 'slideshow_es.html')

# Delete live folder if exists
if os.path.exists(live_dir):
    shutil.rmtree(live_dir)

os.makedirs(live_dir, exist_ok=True)

# Map internal names to display names
name_mapping = {
    'intro_python': 'Intro_Hello_World',
    'etl_merger': 'The_Great_Merger',
    'etl_detective': 'The_Detective',
    'etl_survey': 'The_Messy_Survey',
    'viz_managers_chart': 'The_Managers_Chart',
    'viz_report_generator': 'The_Report_Generator',
    'auto_excel_polish': 'The_Professional_Polish',
    'auto_file_organizer': 'The_File_Organizer',
    'etl_bonus_big_data': 'The_Big_Data_Stress_Test',
    'bonus_auto_pdf_report': 'Auto_PDF_Report',
    'bonus_etl_api_pipeline': 'ETL_API_Pipeline',
    'bonus_viz_d3_bar_chart': 'D3_Bar_Chart',
    'bonus_viz_d3_force_network': 'D3_Force_Network',
    'bonus_viz_geo_heatmap': 'Viz_Geo_Heatmap',
    'bonus_viz_interactive_dashboard': 'Interactive_Dashboard',
    'bonus_viz_seaborn_scatter': 'Seaborn_Scatter',
    'bonus_viz_seaborn_statistical': 'Seaborn_Statistical'
}

# Extract exercise order from slideshow
exercise_order = []
with open(slideshow_file, 'r', encoding='utf-8') as f:
    content = f.read()
    # Find all image lines
    matches = re.findall(r'image: "assets/([^"]+)\.jpg"', content)
    for match in matches:
        # Keep original name for mapping, remove 'bonus_' only if needed for sorting or just use mapping directly
        # The internal names in mapping include 'bonus_' where applicable based on previous list_dir
        # Actually in list_dir, the folders don't have 'bonus_' prefix except maybe 'etl_bonus_big_data' ?
        # Let's check the folder names again.
        # list_dir exercises:
        # auto_excel_polish, auto_file_organizer, auto_pdf_report (no bonus_), etl_api_pipeline (no bonus_),
        # etl_bonus_big_data (has bonus), etl_detective, etl_merger, etl_survey, intro_python,
        # viz_d3_bar_chart, viz_d3_force_network, viz_geo_heatmap, viz_interactive_dashboard,
        # viz_managers_chart, viz_report_generator, viz_seaborn_scatter, viz_seaborn_statistical
        
        # The slideshow has 'bonus_' prefix for images that map to folders WITHOUT 'bonus_' sometimes?
        # unique mapping:
        # image: assets/bonus_auto_pdf_report.jpg -> folder: auto_pdf_report
        # image: assets/bonus_etl_api_pipeline.jpg -> folder: etl_api_pipeline
        # image: assets/bonus_viz_d3_bar_chart.jpg -> folder: viz_d3_bar_chart
        # ...
        
        # So we need to normalize the image name to the folder name.
        folder_name = match
        if folder_name.startswith('bonus_') and folder_name != 'bonus_etl_big_data': 
             # wait, etl_bonus_big_data is the folder. image is assets/etl_bonus_big_data.jpg. NO 'bonus_' prefix in image name for that one?
             # Let's check the grep again.
             # line 627: image: "assets/etl_bonus_big_data.jpg" -> folder etl_bonus_big_data
             # line 654: image: "assets/bonus_auto_pdf_report.jpg" -> folder auto_pdf_report? 
             # YES.
             
             # So if image starts with 'bonus_', strip it to get folder name.
             # EXCEPT if the folder actually starts with bonus_? No, none do except etl_bonus_big_data which doesn't start with bonus_.
             pass

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
        
        # Check if manual mapping exists
        display_name = display_names.get(exercise, exercise)
        
        if os.path.exists(data_dir):
            numbered_name = f"{i:02d}_{display_name}"
            live_exercise_dir = os.path.join(live_dir, numbered_name)
            os.makedirs(live_exercise_dir, exist_ok=True)
            for file in os.listdir(data_dir):
                src = os.path.join(data_dir, file)
                dst = os.path.join(live_exercise_dir, file)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)