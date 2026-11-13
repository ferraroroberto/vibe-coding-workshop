"""Shared CSV I/O helpers for the metadata dashboard.

Both the Data Import and Participation Analysis tabs read the same two
config-driven CSV sources -- employee data and work-center hierarchy -- with
identical path-building, separator, and column-selection logic. These
primitives live here once instead of being copy-pasted between the two tab
modules.
"""

import os

import pandas as pd


def resolve_employee_and_workcenter_paths(config: dict) -> tuple[str, str]:
    """Build the employee and work-center CSV file paths from ``config``.

    Combines each source's ``path``/``file`` fields under the
    ``source_path_employees`` / ``source_path_workcenters`` config keys.
    """
    emp_config = config.get('source_path_employees', {})
    wc_config = config.get('source_path_workcenters', {})
    emp_path = os.path.join(emp_config.get('path', ''), emp_config.get('file', ''))
    wc_path = os.path.join(wc_config.get('path', ''), wc_config.get('file', ''))
    return emp_path, wc_path


def load_employee_and_workcenter_data(config: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load the employee and work-center CSVs, subset to configured columns.

    Reads the employee CSV (semicolon-separated) and work-center CSV
    (comma-separated) from the paths built by
    :func:`resolve_employee_and_workcenter_paths`, then keeps only each
    source's configured ``keep`` columns. May raise ``FileNotFoundError``
    (missing CSV) or other read errors -- the caller owns surfacing those to
    the user.
    """
    emp_config = config.get('source_path_employees', {})
    wc_config = config.get('source_path_workcenters', {})
    emp_path, wc_path = resolve_employee_and_workcenter_paths(config)

    df_emp = pd.read_csv(emp_path, sep=';', encoding='utf-8')
    df_emp = df_emp[emp_config.get('keep', [])]

    df_wc = pd.read_csv(wc_path, sep=',', encoding='utf-8')
    df_wc = df_wc[wc_config.get('keep', [])]

    return df_emp, df_wc
