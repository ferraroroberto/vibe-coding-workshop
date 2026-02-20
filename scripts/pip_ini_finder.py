import os
import sys
from pathlib import Path

# Get current Python executable
python_exe = sys.executable
venv_dir = Path(python_exe).parent.parent

# Possible pip.ini locations on Windows
locations = [
    Path(os.getenv('APPDATA', '')) / 'pip' / 'pip.ini',
    Path('C:/ProgramData/pip/pip.ini'),
    venv_dir / 'pip.ini',
]

found = []
for loc in locations:
    if loc.is_file():
        found.append(str(loc))

if found:
    print('Detected pip.ini files:')
    for f in found:
        print(f)
else:
    print('No pip.ini file found in standard locations.')

print(f"Active Python executable: {python_exe}")
print(f"Assumed virtual environment directory: {venv_dir}")
