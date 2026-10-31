"""Phase 2 candidate status, shared by the tabs that edit the same decisions.

A candidate is **Selected** when ``ind_session`` is 1, otherwise **Waitlist**
when ``ind_waitlist`` is 1, otherwise **Pending**. Selected wins when both flags
are set, so the three counts always add up to the number of rows.
"""

import pandas as pd

SELECTED = 'Selected'
WAITLIST = 'Waitlist'
PENDING = 'Pending'


def candidate_status(row) -> str:
    """Return the status label of one candidate row."""
    if row.get('ind_session', 0) == 1:
        return SELECTED
    if row.get('ind_waitlist', 0) == 1:
        return WAITLIST
    return PENDING


def status_counts(df: pd.DataFrame) -> dict:
    """Return ``{'total', 'selected', 'waitlist', 'pending'}`` row counts for ``df``."""
    selected = int((df['ind_session'] == 1).sum())
    waitlist = int(((df['ind_waitlist'] == 1) & (df['ind_session'] != 1)).sum())
    return {
        'total': len(df),
        'selected': selected,
        'waitlist': waitlist,
        'pending': len(df) - selected - waitlist,
    }
