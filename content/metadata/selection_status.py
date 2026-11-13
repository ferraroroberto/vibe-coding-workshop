"""Phase 2 candidate status, shared by the tabs that edit the same decisions.

The status lives in two 0/1 columns, ``ind_session`` and ``ind_waitlist``. This module
is the only place that turns them into a ``CandidateStatus``; every reader calls
``candidate_status`` (one row), ``status_counts`` (a frame) or ``status_table`` (a frame
grouped by a column) and never compares the flags itself. The state table is in
``docs/candidate-selection-state.md``.
"""

from enum import Enum

import pandas as pd


class CandidateStatus(str, Enum):
    """The closed set of candidate states. The values are the labels the tabs display."""

    SELECTED = 'Selected'   # ind_session is 1 and ind_waitlist is 0
    WAITLIST = 'Waitlist'   # ind_waitlist is 1 and ind_session is 0
    PENDING = 'Pending'     # both flags are 0: no decision yet
    CONFLICT = 'Conflict'   # both flags are 1: an impossible decision, never counted twice
    UNKNOWN = 'Unknown'     # a flag is blank or not 0/1: the decision could not be read


COUNT_KEYS = {
    CandidateStatus.SELECTED: 'selected',
    CandidateStatus.WAITLIST: 'waitlist',
    CandidateStatus.PENDING: 'pending',
    CandidateStatus.CONFLICT: 'conflict',
    CandidateStatus.UNKNOWN: 'unknown',
}


def _read_flag(value):
    """Return 0 or 1 for a readable flag, ``None`` for a blank or out-of-range one."""
    if isinstance(value, str):
        value = value.strip()
        if value in ('0', '1'):
            return int(value)
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        return None
    if value in (0, 1):
        return int(value)
    return None


def candidate_status(row) -> CandidateStatus:
    """Return the status of one candidate row; a column the row lacks counts as 0."""
    session = _read_flag(row.get('ind_session', 0))
    waitlist = _read_flag(row.get('ind_waitlist', 0))
    if session is None or waitlist is None:
        return CandidateStatus.UNKNOWN
    if session and waitlist:
        return CandidateStatus.CONFLICT
    if session:
        return CandidateStatus.SELECTED
    if waitlist:
        return CandidateStatus.WAITLIST
    return CandidateStatus.PENDING


def status_column(df: pd.DataFrame) -> pd.Series:
    """Return each row's status label as a plain string, aligned to ``df.index``."""
    if df.empty:
        return pd.Series([], index=df.index, dtype=object)
    return df.apply(lambda row: candidate_status(row).value, axis=1)


def status_counts(df: pd.DataFrame) -> dict:
    """Return the row count per status plus ``total``; the five states add up to ``total``."""
    labels = status_column(df)
    counts = {'total': len(df)}
    for status, key in COUNT_KEYS.items():
        counts[key] = int((labels == status.value).sum())
    return counts


def status_table(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Return one ``status_counts`` row per value of ``column`` (blank values are skipped)."""
    rows = [{column: group, **status_counts(part)} for group, part in df.groupby(column)]
    return pd.DataFrame(rows, columns=[column, 'total', *COUNT_KEYS.values()])


def exclusive_flags(session, waitlist, was_session, was_waitlist) -> tuple:
    """Return ``(ind_session, ind_waitlist)`` that are never both 1.

    When both are ticked, the one that was just ticked wins; when both were just
    ticked, or neither is new (an old conflict saved while editing another field),
    Selected wins.
    """
    session, waitlist = int(bool(session)), int(bool(waitlist))
    if session and waitlist:
        newly_waitlist = _read_flag(was_waitlist) != 1
        newly_session = _read_flag(was_session) != 1
        if newly_waitlist and not newly_session:
            return 0, 1
        return 1, 0
    return session, waitlist
