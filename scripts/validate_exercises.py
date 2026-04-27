#!/usr/bin/env python3
"""
Validate all exercises by running setup data and solution scripts in sequence.

This module is for local deployment validation. Since data folders are in .gitignore,
running this script ensures that:
  1. Each exercise's exercise_setup_data.py generates data successfully
  2. Each exercise's exercise_solution.py runs successfully against that data

Usage:
  pip install -r requirements.txt   # Install dependencies first
  python validate_exercises.py

Run from the project root. Requires a Python environment with project dependencies installed.
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

# Project root (parent of scripts directory)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXERCISES_DIR = PROJECT_ROOT / "exercises"

SETUP_SCRIPT = "exercise_setup_data.py"
SOLUTION_SCRIPT = "exercise_solution.py"

log = logging.getLogger(__name__)


def get_exercise_folders():
    """Return sorted list of exercise folder paths."""
    if not EXERCISES_DIR.exists():
        return []
    return sorted(
        p for p in EXERCISES_DIR.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )


def run_script(exercise_path: Path, script_name: str) -> tuple[bool, str]:
    """
    Run a Python script from the exercise directory.
    Returns (success: bool, output: str).
    """
    script_path = exercise_path / script_name
    if not script_path.exists():
        return True, f"(no {script_name})"

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=str(exercise_path),
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = result.stdout + result.stderr
        if result.returncode != 0:
            return False, output.strip() or f"Exit code {result.returncode}"
        return True, output.strip() or "OK"
    except subprocess.TimeoutExpired:
        return False, "Timeout (120s)"
    except Exception as e:
        return False, str(e)


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    log.info("=" * 60)
    log.info("Exercise Validation (setup data + solutions)")
    log.info("=" * 60)
    log.info("Project root: %s", PROJECT_ROOT)
    log.info("Exercises dir: %s", EXERCISES_DIR)

    exercises = get_exercise_folders()
    if not exercises:
        log.error("No exercise folders found.")
        sys.exit(1)

    results = []
    all_passed = True

    for exercise_path in exercises:
        name = exercise_path.name
        log.info("\n--- %s ---", name)

        setup_ok, setup_out = run_script(exercise_path, SETUP_SCRIPT)
        if not setup_ok:
            log.error("  SETUP FAILED:\n%s", setup_out[:500])
            if len(setup_out) > 500:
                log.error("  ... (truncated)")
            results.append((name, "setup", False))
            all_passed = False
            continue
        log.info("  Setup: %s%s", setup_out[:80], '...' if len(setup_out) > 80 else '')

        solution_ok, solution_out = run_script(exercise_path, SOLUTION_SCRIPT)
        if not solution_ok:
            log.error("  SOLUTION FAILED:\n%s", solution_out[:500])
            if len(solution_out) > 500:
                log.error("  ... (truncated)")
            results.append((name, "solution", False))
            all_passed = False
            continue
        log.info("  Solution: %s%s", solution_out[:80], '...' if len(solution_out) > 80 else '')

        results.append((name, "both", True))
        log.info("  PASSED")

    log.info("\n" + "=" * 60)
    log.info("Summary")
    log.info("=" * 60)
    passed = sum(1 for _, _, ok in results if ok)
    failed = sum(1 for _, _, ok in results if not ok)
    log.info("Passed: %d/%d", passed, len(exercises))
    if failed:
        log.error("Failed: %d", failed)
        for name, phase, ok in results:
            if not ok:
                log.error("  - %s (%s)", name, phase)
        sys.exit(1)
    log.info("All exercises validated successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
