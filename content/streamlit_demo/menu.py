"""
Menu / Page Registry
====================
Metadata registry used by the home page to display description cards for each
demo.  Routing is handled entirely by Streamlit's multipage auto-discovery of
the ``pages/`` directory — adding a new demo requires only creating
``pages/my_demo.py``.  Adding an entry here is optional and controls only
whether a card appears on the home page.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Page registry – drives the home-page description cards only.
# Order here = order of cards; sidebar order comes from Streamlit's
# filename-based auto-discovery of the ``pages/`` directory.
# ---------------------------------------------------------------------------
PAGES: list[dict] = [
    {
        "label": "Data Input",
        "icon": "⌨",
        "description": "Text fields, sliders, selects, forms with submit buttons.",
    },
    {
        "label": "Visualization",
        "icon": "📊",
        "description": "Tables, editable dataframes, line/bar/scatter charts, KPI metrics.",
    },
    {
        "label": "CRUD Operations",
        "icon": "🗂",
        "description": "Create, read, update and delete records from an in-memory dataset.",
    },
    {
        "label": "File Handling",
        "icon": "📁",
        "description": "Upload CSV / TXT / JSON files and download generated files.",
    },
    {
        "label": "Process Runner",
        "icon": "💻",
        "description": "Execute a long-running task with live logs, progress bars and status.",
    },
    {
        "label": "State Management",
        "icon": "🧠",
        "description": "Demonstrate st.session_state and cross-module shared state.",
    },
]


# ---------------------------------------------------------------------------
# Home page renderer
# ---------------------------------------------------------------------------
def render_home() -> None:
    """Render the landing / home page with an overview of all demos."""
    st.title("Streamlit Demo Playground")
    st.markdown(
        """
        Welcome! This application is a **self-contained reference project** that
        showcases the most common Streamlit patterns you will need when building
        internal tools and dashboards.

        Use the **sidebar** on the left to navigate between demos.  Each demo is
        a standalone module that focuses on a single capability.
        """
    )

    st.markdown("---")
    st.subheader("Available Demos")

    # Render a card-like grid of demos
    cols = st.columns(3)
    for idx, page in enumerate(PAGES):
        with cols[idx % 3]:
            st.markdown(f"#### {page['icon']} {page['label']}")
            st.write(page["description"])

    st.markdown("---")
    st.info(
        "**Tip:** All data is generated locally — no external services are required. "
        "If the mock data files are missing they will be created automatically on first run."
    )
