"""The organisational hierarchy shared by every dashboard tab.

Each tab used to spell out the hierarchy columns and their display labels on its
own, so a level read differently from tab to tab and a rename had to be made in
several places. The ordered ``HIERARCHY_LEVELS`` constant below is the single
definition; a tab picks the levels it shows, in the order it wants, with
``hierarchy_levels``.
"""

from typing import Dict, List, Tuple

# (column, display label), broadest level first.
HIERARCHY_LEVELS: Tuple[Tuple[str, str], ...] = (
    ('des_red', 'Network'),
    ('des_dt', 'N+3 (DT)'),
    ('des_dg', 'N+2 (DG)'),
    ('des_dan', 'N+1 (DAN)'),
    ('des_centro_ges', 'Work Center'),
)

HIERARCHY_LABELS: Dict[str, str] = dict(HIERARCHY_LEVELS)


def hierarchy_levels(*columns: str) -> List[Tuple[str, str]]:
    """Return ``(column, label)`` pairs for ``columns``, in the order given.

    Raises ``KeyError`` for a column that is not a hierarchy level, so a typo
    fails loudly instead of silently dropping a level from a tab.
    """
    return [(column, HIERARCHY_LABELS[column]) for column in columns]
