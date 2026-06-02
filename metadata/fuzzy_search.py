"""Shared fuzzy name-search helper for the metadata dashboard."""

import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def fuzzy_filter_by_name(df: pd.DataFrame, search_term: str, threshold: int = 70) -> pd.DataFrame:
    """Filter ``df`` to rows whose ``name`` fuzzily matches ``search_term``.

    Matches above ``threshold`` (partial-ratio score) are kept and the result is
    ordered best-match-first. Returns ``df`` unchanged when ``search_term`` is
    empty, and an empty slice when nothing clears the threshold.
    """
    if not search_term:
        return df

    names = df['name'].dropna().tolist()
    matches = process.extract(search_term, names, scorer=fuzz.partial_ratio, limit=None)
    good_matches = [(name, score) for name, score in matches if score >= threshold]
    if not good_matches:
        return df[df['name'].isin([])]

    good_matches.sort(key=lambda x: x[1], reverse=True)
    matched_names = [name for name, _ in good_matches]
    name_to_order = {name: i for i, (name, _) in enumerate(good_matches)}
    filtered = df[df['name'].isin(matched_names)]
    return (
        filtered.assign(match_order=filtered['name'].map(name_to_order))
        .sort_values('match_order')
        .drop('match_order', axis=1)
    )
