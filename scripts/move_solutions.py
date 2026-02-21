import os
import glob
import re
import shutil

def process_exercise(exercise_dir):
    solution_script = os.path.join(exercise_dir, 'exercise_solution.py')
    if not os.path.exists(solution_script):
        return

    with open(solution_script, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find output files
    # We look for variables like OUTPUT_FILE, OUTPUT_PDF, OUTPUT_HTML, OUTPUT_CSV, OUTPUT_EXCEL, OUTPUT_IMAGE, OUTPUT_SCATTER, OUTPUT_REGRESSION, OUTPUT_FACETED, OUTPUT_HEATMAP, OUTPUT_VIOLIN, OUTPUT_PAIRPLOT, OUTPUT_BOXSTRIP, PARQUET_FILE
    
    output_vars = [
        'OUTPUT_FILE', 'OUTPUT_PDF', 'OUTPUT_HTML', 'OUTPUT_CSV', 'OUTPUT_EXCEL', 
        'OUTPUT_IMAGE', 'OUTPUT_SCATTER', 'OUTPUT_REGRESSION', 'OUTPUT_FACETED', 
        'OUTPUT_HEATMAP', 'OUTPUT_VIOLIN', 'OUTPUT_PAIRPLOT', 'OUTPUT_BOXSTRIP', 
        'PARQUET_FILE', 'CHART_BAR', 'CHART_PIE'
    ]
    
    modified = False
    files_to_move = []
    
    for var in output_vars:
        # Look for var = os.path.join(DATA_DIR, "filename")
        pattern1 = rf'{var}\s*=\s*os\.path\.join\(([^,]+),\s*"([^"]+)"\)'
        # Look for var = "filename"
        pattern2 = rf'{var}\s*=\s*"([^"]+)"'
        
        def repl1(match):
            nonlocal modified
            dir_var = match.group(1)
            filename = match.group(2)
            if not filename.startswith('solutions/'):
                modified = True
                files_to_move.append(filename)
                return f'{var} = os.path.join({dir_var}, "solutions", "{filename}")'
            return match.group(0)
            
        def repl2(match):
            nonlocal modified
            filename = match.group(1)
            if not filename.startswith('solutions/'):
                modified = True
                files_to_move.append(filename)
                return f'{var} = "solutions/{filename}"'
            return match.group(0)
            
        content = re.sub(pattern1, repl1, content)
        content = re.sub(pattern2, repl2, content)

    if modified:
        # Add os.makedirs logic if not present
        # Find where the output file is written and add os.makedirs before it
        # Actually, it's easier to just add it at the beginning of main() or after imports
        
        # Let's just add a generic os.makedirs for the solutions folder
        # Find DATA_DIR or BASE_DIR
        dir_var = None
        if 'DATA_DIR' in content:
            dir_var = 'DATA_DIR'
        elif 'BASE_DIR' in content:
            dir_var = 'BASE_DIR'
            
        if dir_var and 'os.makedirs' not in content:
            # Add it after the configuration section
            setup_code = f"\n# Ensure solutions directory exists\nos.makedirs(os.path.join({dir_var}, 'solutions'), exist_ok=True)\n"
            
            # Insert before def main() or at the end of imports
            if 'def main():' in content:
                content = content.replace('def main():', f'{setup_code}\ndef main():')
            else:
                # Find last import
                lines = content.split('\n')
                last_import = -1
                for i, line in enumerate(lines):
                    if line.startswith('import ') or line.startswith('from '):
                        last_import = i
                if last_import != -1:
                    lines.insert(last_import + 1, setup_code)
                    content = '\n'.join(lines)

        with open(solution_script, 'w', encoding='utf-8') as f:
            f.write(content)
            
        # Move files
        data_dir = os.path.join(exercise_dir, 'data')
        solutions_dir = os.path.join(data_dir, 'solutions')
        os.makedirs(solutions_dir, exist_ok=True)
        
        for filename in files_to_move:
            src = os.path.join(data_dir, filename)
            dst = os.path.join(solutions_dir, filename)
            if os.path.exists(src):
                shutil.move(src, dst)
                print(f"Moved {src} to {dst}")

for exercise_dir in glob.glob('exercises/*'):
    if os.path.isdir(exercise_dir):
        process_exercise(exercise_dir)
