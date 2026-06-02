"""Shared transformation rules for the two sync tabs (data_sync, phase_two_sync).

Both sync flows apply the same two config-driven transforms when moving source
rows into the master workbook:

* **replicate** — copy a source column's value into a destination column,
  substituting a configured ``missing_field_value`` when the source is blank and
  the origin is flagged in ``missing_fields``.
* **binary_check** — convert a "Sí"/other text answer into ``1``/``0`` in a
  destination column.

The two tabs write into different targets (a fresh ``pd.Series`` vs. an existing
``full_df`` row plus a master-df mirror), so the write itself is supplied via
callbacks while the decision logic lives here.
"""

import pandas as pd
from typing import Callable, Optional


def _is_blank(value) -> bool:
    return pd.isna(value) or str(value).strip() == ''


def to_binary(value) -> int:
    """Return ``1`` when ``value`` contains "sí" (case-insensitive), else ``0``."""
    value_str = str(value).strip() if pd.notna(value) else ''
    return 1 if 'sí' in value_str.lower() else 0


def apply_replicate_rules(
    rules: list,
    get_source: Callable[[str], object],
    set_excel: Callable[[int, object], None],
    *,
    missing_field_value: str = 'sin respuesta',
    missing_fields: Optional[list] = None,
    set_master: Optional[Callable[[str, object], None]] = None,
    also_write_origin: bool = False,
) -> None:
    """Apply each replicate rule, writing via the supplied callbacks.

    ``get_source(origin_key)`` returns the source value (or ``None`` if absent);
    ``set_excel(col_index, value)`` writes into the Excel row. When
    ``set_master`` is given, the value is mirrored into the master df under the
    rule's ``column_id``. ``also_write_origin`` additionally writes the value
    back into the origin column index (data_sync's behaviour).
    """
    missing_fields = missing_fields or []
    for rule in rules:
        origin = rule.get('origin')
        destination = rule.get('destination')
        column_id = rule.get('column_id')

        value = get_source(str(origin))
        if value is None:
            continue

        if _is_blank(value) and origin in missing_fields:
            value = missing_field_value

        if destination is not None:
            set_excel(destination, value)
        if also_write_origin and origin is not None:
            set_excel(origin, value)
        if set_master is not None and column_id:
            set_master(column_id, value)


def apply_binary_checks(
    rules: list,
    get_source: Callable[[str], object],
    set_excel: Callable[[int, object], None],
    *,
    set_master: Optional[Callable[[str, object], None]] = None,
    keep_original: bool = False,
) -> None:
    """Apply each binary_check rule, writing via the supplied callbacks.

    Converts the source column's value to ``1``/``0`` in the destination column.
    ``keep_original`` also writes the untouched source value back into the source
    column index (data_sync's behaviour). When ``set_master`` is given, the
    binary value is mirrored into the master df under the rule's ``column_id``.
    """
    for rule in rules:
        source_col = rule.get('column')
        destination = rule.get('destination')
        column_id = rule.get('column_id', '')

        original_value = get_source(str(source_col))
        if original_value is None:
            continue

        if keep_original and source_col is not None:
            set_excel(source_col, original_value)

        binary_value = to_binary(original_value)
        if destination is not None:
            set_excel(destination, binary_value)
        if set_master is not None and column_id:
            set_master(column_id, binary_value)
