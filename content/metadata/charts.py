"""Shared chart-building helpers for the metadata dashboard.

The dashboard renders many categorical breakdowns with the same look: the
largest slice in accent blue and the rest in a light-to-dark grey ramp, with
small slices rolled into an "Other" bucket. These helpers own that logic so the
colour ramp and the roll-up threshold live in one place.
"""

import pandas as pd
import plotly.express as px

ACCENT_BLUE = '#1E88E5'


def grey_ramp(n: int) -> list:
    """Return ``n`` colours: index 0 is accent blue, the rest ramp grey.

    The grey shades interpolate from light ``#D9D9D9`` (217) to dark ``#404040``
    (64), light-to-dark, so the leading (largest) category stands out in blue.
    """
    colors = [ACCENT_BLUE]
    for i in range(1, n):
        factor = (i - 1) / (n - 2) if n > 2 else 0
        gray = int(217 + (64 - 217) * factor)  # #D9D9D9 -> #404040
        colors.append(f'rgb({gray},{gray},{gray})')
    return colors


def collapse_to_other(counts_df: pd.DataFrame, column: str, threshold: float) -> pd.DataFrame:
    """Roll categories below ``threshold`` (fraction of total) into "Other".

    ``counts_df`` must have ``column`` and ``count`` columns. Returns a frame
    sorted by count descending with an ``Other`` row appended when any small
    categories were collapsed.
    """
    df = counts_df.sort_values('count', ascending=False)
    total = df['count'].sum()
    df = df.assign(percentage=df['count'] / total)
    main = df[df['percentage'] >= threshold]
    rest_count = df[df['percentage'] < threshold]['count'].sum()
    if rest_count > 0:
        rest_df = pd.DataFrame({column: ['Other'], 'count': [rest_count], 'percentage': [rest_count / total]})
        return pd.concat([main, rest_df], ignore_index=True)
    return main


def build_breakdown_pie(df: pd.DataFrame, column: str, threshold: float, title: str, lowercase: bool = False):
    """Build a blue+grey pie chart of value counts for ``column``.

    Categories below ``threshold`` are collapsed into "Other"; the largest slice
    is accent blue and the rest follow :func:`grey_ramp`. Set ``lowercase`` to
    lower-case category labels (used by the hierarchy breakdowns).
    """
    counts_df = df[column].value_counts().reset_index()
    counts_df.columns = [column, 'count']
    counts_df = collapse_to_other(counts_df, column, threshold)
    if lowercase:
        counts_df[column] = counts_df[column].str.lower()
    color_map = dict(zip(counts_df[column], grey_ramp(len(counts_df))))
    return px.pie(
        counts_df,
        values='count',
        names=column,
        title=title,
        color=column,
        color_discrete_map=color_map,
    )
