"""Shared sidebar-filter helper for the metadata dashboard tabs.

Every tab applies the sidebar's column filters to its working frame with the
same loop. The one *legitimate* difference between tabs is whether a blank
(``NaN``) value in a filtered column should survive the filter:

- **Editing tabs** (``data_entry``, ``phase_two_entry``, ``selection_management``)
  keep blank rows (``include_na=True``) so a freshly-added record whose filter
  column is still empty stays visible and editable.
- **Read-only analytics tabs** (``explore``, ``participation_analysis``) drop
  blank rows (``include_na=False``) so aggregate metrics only count records that
  actually match the selected value.

Centralising the loop keeps that one real difference an explicit, per-caller
flag instead of an easy-to-miss ``| df[col].isna()`` fork copied five times.
"""

import pandas as pd


def apply_filters(df: pd.DataFrame, filters: dict, *, include_na: bool) -> pd.DataFrame:
    """Return ``df`` filtered by the sidebar ``filters`` mapping.

    ``filters`` maps a column name to the list of selected values; an empty
    selection means "no filter on this column". Columns absent from ``df`` are
    skipped. When ``include_na`` is true, rows whose value in a filtered column
    is blank (``NaN``) are kept regardless of the selection.
    """
    filtered_df = df.copy()
    for col, selected in filters.items():
        if selected and col in filtered_df.columns:
            mask = filtered_df[col].isin(selected)
            if include_na:
                mask = mask | filtered_df[col].isna()
            filtered_df = filtered_df[mask]
    return filtered_df
