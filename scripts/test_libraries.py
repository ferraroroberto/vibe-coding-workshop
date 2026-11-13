# Post-`pip install` smoke check for the workshop libraries in requirements.txt.
# Exits non-zero when any library is missing or fails its smoke call.
import importlib
import io
import logging
import os
import sys
from typing import Callable, Optional

log = logging.getLogger(__name__)


def _faker(mod):
    log.info("  Sample name: %s", mod.Faker().name())


def _duckdb(mod):
    conn = mod.connect()
    try:
        log.info("  Test query result: %s", conn.execute("SELECT 1 as test").fetchone())
    finally:
        conn.close()


def _pandas(mod):
    df = mod.DataFrame({"A": [1, 2], "B": [3, 4]})
    assert len(df) == 2
    log.info("  DataFrame created: %s", df.shape)


def _numpy(mod):
    log.info("  Array mean: %s", mod.array([1, 2, 3, 4, 5]).mean())


def _matplotlib(mod):
    mod.use("Agg")  # Non-interactive backend: no display needed
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    plt.close(fig)
    log.info("  Plot created and closed successfully.")


def _seaborn(mod):
    import matplotlib.pyplot as plt
    import pandas as pd

    mod.set_theme(style="whitegrid")
    tips = pd.DataFrame({
        "total_bill": [10.34, 21.01, 23.68, 24.59],
        "tip": [1.66, 3.50, 3.31, 3.61],
        "day": ["Sun", "Sun", "Mon", "Mon"],
    })
    fig, ax = plt.subplots()
    mod.scatterplot(data=tips, x="total_bill", y="tip", hue="day", ax=ax)
    plt.close(fig)
    log.info("  Scatterplot created successfully.")


def _plotly(mod):
    import plotly.express as px
    import plotly.graph_objects as go

    fig = px.bar(x=["A", "B", "C"], y=[1, 2, 3], title="Test")
    html = fig.to_html(full_html=False, include_plotlyjs=False)
    assert len(html) > 0
    assert go.Figure(data=[go.Indicator(mode="number", value=42)]) is not None
    log.info("  Bar chart HTML generated (%d chars).", len(html))


def _folium(mod):
    from folium.plugins import HeatMap

    m = mod.Map(location=[40.7128, -74.0060], zoom_start=10)
    HeatMap([[40.7128, -74.0060, 1.0]]).add_to(m)
    html = m._repr_html_()
    assert len(html) > 0
    log.info("  Map with HeatMap generated (%d chars).", len(html))


def _fpdf(mod):
    pdf = mod.FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.cell(200, 10, text="Test PDF", align="C")
    output = pdf.output()  # in memory, nothing is written to disk
    assert len(output) > 0
    log.info("  PDF generated in memory (%d bytes).", len(output))


def _openpyxl(mod):
    ws = mod.Workbook().active
    ws["A1"] = "Test"
    assert ws["A1"].value == "Test"
    log.info("  Workbook created and cell written.")


def _pyarrow(mod):
    table = mod.table({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    log.info("  Arrow table created with %d rows.", len(table))


def _xlsxwriter(mod):
    buffer = io.BytesIO()
    wb = mod.Workbook(buffer, {"in_memory": True})
    wb.add_worksheet().write("A1", "Test")
    wb.close()
    assert buffer.getbuffer().nbytes > 0
    log.info("  Workbook written in memory.")


def _streamlit(mod):
    assert callable(getattr(mod, "set_page_config", None))
    assert callable(getattr(mod, "write", None))
    log.info("  Run: streamlit run main_menu.py (from content/streamlit_demo/) to launch the demo app.")


# (display name, importable module, smoke call taking the imported module)
CHECKS: list[tuple[str, str, Optional[Callable]]] = [
    ("Faker", "faker", _faker),
    ("DuckDB", "duckdb", _duckdb),
    ("Pandas", "pandas", _pandas),
    ("NumPy", "numpy", _numpy),
    ("Matplotlib", "matplotlib", _matplotlib),
    ("Seaborn", "seaborn", _seaborn),
    ("Plotly", "plotly", _plotly),
    ("Folium", "folium", _folium),
    ("FPDF2", "fpdf", _fpdf),
    ("Openpyxl", "openpyxl", _openpyxl),
    ("PyArrow", "pyarrow", _pyarrow),
    ("XlsxWriter", "xlsxwriter", _xlsxwriter),
    ("Streamlit", "streamlit", _streamlit),
]


def run_check(name: str, module: str, smoke: Optional[Callable]) -> bool:
    """Import `module`, run its smoke call, and log a ✔/✘ line; True on success."""
    log.info("--- %s ---", name)
    try:
        mod = importlib.import_module(module)
        log.info("  Version: %s", getattr(mod, "__version__", "installed"))
        if smoke is not None:
            smoke(mod)
    except Exception as exc:
        log.error("\033[91m✘\033[0m %s failed: %s", name, exc)
        return False
    log.info("\033[92m✔\033[0m %s ok", name)
    return True


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    log.info("Workshop library smoke check (Python %s, %s)", sys.version.split()[0], os.getcwd())

    failed = [name for name, module, smoke in CHECKS if not run_check(name, module, smoke)]

    if failed:
        log.error("❌ %d of %d libraries failed: %s", len(failed), len(CHECKS), ", ".join(failed))
        return 1
    log.info("✅ All %d libraries passed.", len(CHECKS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
