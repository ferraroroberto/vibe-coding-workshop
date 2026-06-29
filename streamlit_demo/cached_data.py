"""
Cached Data Accessors (UI layer)
================================
Thin Streamlit-cached wrappers around the pure-pandas loaders in
``data/loader.py``. Caching lives here, on the UI side, because the
``data/`` package is the non-UI data layer and must never import
``streamlit`` (project convention: "Never import ``streamlit`` from
non-UI code").

Pages should import their data from **this** module, not from
``data.loader`` directly, so every read goes through ``@st.cache_data``.
"""

import pandas as pd
import streamlit as st

from data import loader


@st.cache_data
def load_employees() -> pd.DataFrame:
    """Cached employees dataset for the UI."""
    return loader.load_employees()


@st.cache_data
def load_sales() -> pd.DataFrame:
    """Cached sales dataset for the UI."""
    return loader.load_sales()
