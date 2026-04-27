import logging
import os
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

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
    log.info('Detected pip.ini files:')
    for f in found:
        log.info('%s', f)
else:
    log.info('No pip.ini file found in standard locations.')

log.info("Active Python executable: %s", python_exe)
log.info("Assumed virtual environment directory: %s", venv_dir)
