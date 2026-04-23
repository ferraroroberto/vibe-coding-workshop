# Vibe Coding Workshop

## 🧭 Context
**WHAT**: Hands-on Python workshop — exercises, slideshow, tips presentation, and a Streamlit reference app.
**WHY**: Teach data manipulation, automation, and visualization with Python in a corporate setting.
**STACK**: Python 3.7+, single-file HTML/CSS/JS for presentations, Streamlit for the demo app. Bash shell on Windows.

## 🗺️ Codebase Map
- `exercises/`: One folder per exercise (starter, solution, setup, data). Bilingual starters (English + Español).
- `slideshow/`: `slideshow.html` (EN), `slideshow_es.html` (ES), `slideshow_config.json`, `assets/`. Generated — do not hand-edit the HTML.
- `tips/`: Vibe Coding Tips presentation — `index.html`, `styles.css`, `script.js`, `docs/`, `examples/`.
- `streamlit_demo/`: Multi-page reference app (`main_menu.py`, `pages/`, `data/`, `scripts/`).
- `scripts/`: Build/validate/util scripts (`build_slideshow.py`, `validate_exercises.py`, `test_libraries.py`, `sync_slideshow_to_starters.py`, etc.).
- `preparation/`: Docs on how the slideshow and images were built; metaprompt for new exercises.
- `metadata/`: Participant data tooling (config, entry, sync, Streamlit app).
- `requirements.txt`: Pinned dependencies.
- `.venv/`: Local virtual environment (DO NOT TOUCH).

## 🚀 Workflow
1. **Plan**: Propose a brief phased plan (files to change, strategy) before coding.
2. **Approve**: Wait for user confirmation.
3. **Implement**: Scoped changes, one at a time.
4. **Test**: Run the relevant script with the local Python interpreter.
5. **Commit and push**: Only when asked; push to the current branch (do not switch branches).

## ⚖️ Core Principles
1. **Config First**: JSON for config, `.env` for secrets. No hardcoded paths/creds.
2. **Logging**: Use `logging` module with emojis (ℹ️, ⚠️, ❌). Never use `print()` for diagnostics; never write log files.
3. **Naming**: Files/Functions=`snake_case`, Classes=`PascalCase`, Constants=`UPPER_CASE`.
4. **No Secrets**: Never commit `.env` or credentials.
5. **Scope Discipline**: Do only what is asked. No "nice-to-haves", no bloat.
6. **Dependencies**: Pin versions in `requirements.txt`. Use the existing `.venv`.
7. **Imports**: Standard Lib → Third Party → Local.
8. **Error Handling**: Fail fast with clear messages.
9. **Streamlit**: Use `width='stretch'` instead of deprecated `use_container_width=True`.

## 📐 Project-Specific Rules
- **Slideshow is generated**: Never hand-edit `slideshow/slideshow.html` or `slideshow_es.html`. Edit exercises and/or `slideshow/slideshow_config.json`, then run `python scripts/build_slideshow.py` to regenerate both languages.
- **Bilingual starters**: Exercise starter files use `## English` and `## Español` sections — keep both in sync when editing.
- **New exercises**: Follow `preparation/metaprompt.md`; add folder under `exercises/` (starter, solution, setup, data), register in `slideshow_config.json`, rebuild slideshow, add image to `slideshow/assets/` if needed.
- **Validate after structural changes**: `python scripts/validate_exercises.py` and `python scripts/test_libraries.py`.
- **Single-file presentations**: `slideshow/*.html` and `tips/index.html` must stay self-contained (only local assets, no external runtime deps).
