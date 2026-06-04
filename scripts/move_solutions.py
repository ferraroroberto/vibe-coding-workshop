import logging
import os
import glob
import re
import shutil
from pathlib import Path

log = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def process_exercise(exercise_dir: str) -> None:
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
        # Find DATA_DIR or BASE_DIR
        dir_var = None
        if 'DATA_DIR' in content:
            dir_var = 'DATA_DIR'
        elif 'BASE_DIR' in content:
            dir_var = 'BASE_DIR'

        if dir_var and 'os.makedirs' not in content:
            setup_code = f"\n# Ensure solutions directory exists\nos.makedirs(os.path.join({dir_var}, 'solutions'), exist_ok=True)\n"

            if 'def main():' in content:
                content = content.replace('def main():', f'{setup_code}\ndef main():')
            else:
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
                log.info("Moved %s to %s", src, dst)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    exercises_dir = str(PROJECT_ROOT / 'exercises')
    for exercise_dir in glob.glob(os.path.join(exercises_dir, '*')):
        if os.path.isdir(exercise_dir):
            process_exercise(exercise_dir)


if __name__ == '__main__':
    main()
