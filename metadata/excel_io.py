"""Shared Excel I/O helpers for the metadata dashboard.

Every tab that writes back to the master workbook needs the same three things:
read the full sheet, translate the config's ``column_id`` <-> column-index
mapping, and write the result back atomically (temp file + ``os.replace``) so a
crash mid-write can never corrupt the workbook. These primitives live here so a
fix or hardening happens once instead of in six near-identical copies.
"""

import os
import tempfile

import pandas as pd


def load_full_sheet(config: dict) -> pd.DataFrame:
    """Read the entire master sheet with its header row intact."""
    excel_path = config['excel_path']
    sheet = config['excel_interpreter_spec']['sheet_name']
    return pd.read_excel(excel_path, sheet_name=sheet, header=0, engine='openpyxl')


def build_column_id_to_index(config: dict) -> dict:
    """Map each ``column_id`` to its column index, skipping ``skip`` columns."""
    columns = config['excel_interpreter_spec']['columns']
    return {col['column_id']: col['column'] for col in columns if col['column_id'] != 'skip'}


def build_column_index_to_id(config: dict) -> dict:
    """Inverse of :func:`build_column_id_to_index`, keyed by column index."""
    return {index: col_id for col_id, index in build_column_id_to_index(config).items()}


def find_id_column_name(full_df: pd.DataFrame, config: dict) -> str:
    """Return the workbook column name that holds the ``id`` field.

    Falls back to the first column when the config has no ``id`` mapping.
    """
    id_index = build_column_id_to_index(config).get('id', 0)
    return full_df.columns[id_index]


def atomic_write_sheet(full_df: pd.DataFrame, config: dict) -> None:
    """Write ``full_df`` to the configured sheet atomically.

    The frame is written to a temp file in the same directory, then swapped in
    with ``os.replace`` so the original is never left half-written.
    """
    excel_path = config['excel_path']
    sheet = config['excel_interpreter_spec']['sheet_name']
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx', dir=os.path.dirname(excel_path)) as tmp_file:
        tmp_path = tmp_file.name
    with pd.ExcelWriter(tmp_path, engine='openpyxl') as writer:
        full_df.to_excel(writer, sheet_name=sheet, index=False)
    os.replace(tmp_path, excel_path)


def save_dataframe_to_excel(df: pd.DataFrame, config: dict) -> None:
    """Persist the working ``df`` (keyed by ``id``) back to the master workbook.

    Loads the full sheet, drops rows no longer present in ``df`` (handles
    deletes), updates the rows that remain and appends new ones, mapping each
    ``column_id`` back to its original workbook column, then writes atomically.
    """
    full_df = load_full_sheet(config)
    column_map = build_column_id_to_index(config)
    id_column = find_id_column_name(full_df, config)

    # Keep only rows that still exist in df (handles deletes).
    full_df = full_df[full_df[id_column].isin(df['id'])].reset_index(drop=True)

    existing_ids = set(full_df[id_column].values)
    for _, row in df.iterrows():
        row_id = row['id']
        if row_id in existing_ids:
            full_idx = full_df[full_df[id_column] == row_id].index[0]
            for col_id, value in row.items():
                if col_id in column_map:
                    full_df.at[full_idx, full_df.columns[column_map[col_id]]] = value
        else:
            new_row = {}
            for col in full_df.columns:
                if col == id_column:
                    new_row[col] = row['id']
                else:
                    col_id = next((cid for cid, cidx in column_map.items() if full_df.columns[cidx] == col), None)
                    new_row[col] = row.get(col_id) if col_id else None
            full_df = pd.concat([full_df, pd.DataFrame([new_row])], ignore_index=True)

    atomic_write_sheet(full_df, config)
