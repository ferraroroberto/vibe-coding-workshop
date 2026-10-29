# Project Instructions

Canonical instructions for AI coding agents working in this repository. Claude Code reads this file directly as project memory. Other agents (Cursor, Codex, etc.) reach it via the one-line `AGENTS.md` pointer.

## Streamlit conventions
*Apply only if this project uses Streamlit.*

- `st.set_page_config(layout="wide", page_title="...")` MUST be the first Streamlit call.
- Use `width="stretch"` (and `width="content"` where appropriate) in new and modified code. **Never** introduce new `use_container_width=True` — it is deprecated. When you touch existing code that uses `use_container_width`, migrate it.
- All mutable state in `st.session_state`. No module-level globals.
- `@st.cache_data` for DataFrames/files; `@st.cache_resource` for DB clients/models.
- Every widget needs a stable, explicit `key=`.
- UI code only in the UI directory (e.g. `app/`). Data logic stays in the non-UI package (e.g. `src/`). Never import `streamlit` from non-UI code.
- User feedback via `st.error()` / `st.warning()` / `st.success()`, not `st.write()`.
- **App layout:** main file (e.g. `app.py`) handles only page config, shared state, sidebar, and tab/radio routing. Each tab/mode lives in its own file exposing a `main(...)` (or `render_*`) function. Default to `st.tabs()`; use a sidebar radio only when asked.

## This repository
Python data/automation/visualization workshop content with a Streamlit slideshow plus per-exercise starter and solution files.
See `README.md` for setup, layout, and usage.

## Internal architecture

[`docs/architecture.mmd`](docs/architecture.mmd) is a hand-authored Mermaid diagram of this repo's own internal structure (exercise content, the `scripts/` build/facilitator tooling, the generated `slideshow/` + `live/` bundle, the standalone `tips/` / `slideshow_ai/` presentations, and the independent `streamlit_demo/` + `metadata/` apps). Update it in the same PR as any material structural change (an exercise category added/removed, a build script relocated, a new standalone app folder) — same anti-staleness contract as a `.fleet.toml` `description` field. It is not auto-generated and not covered by any test suite.

## Gate ratchets

`scripts/verify-before-ship.ps1` runs eight ratchets. Each `scripts/<name>_ratchet.py` is vendored byte-for-byte from the scaffold (`.fleet.toml` `[vendored]`, `[<name>_ratchet]`): re-vendor with `/propagate-vendored <name>_ratchet`, never edit. Each fails when a measure rises above its shrink-only `.<name>-ratchet-baseline.json` (empty today except doc refs, one README path); exit 3 (could not measure) is a failure, never a pass. Shrink a baseline with `--update-baseline`; `--update-baseline --allow-additions` is the only way to add an entry and shows in review.

- **Structure:** a new file over 1,000 lines, a new function over 100 lines or a directory past 40 modules, and any baselined offender that grows past its size. `exercises/**` is excluded (solutions are teaching material, written long on purpose) and no `shape` is declared. Where code goes: [`docs/layout.md`](docs/layout.md).
- **Instruction:** lints `CLAUDE.md` and `AGENTS.md` against the weekly prompt audit's deterministic rules; fails when a rule-hit count rises or a file passes its size cap.
- **Doc refs:** `README.md`, `CLAUDE.md` or `docs/` naming a repo path, module, relative link or loopback port that does not exist.
- **Dead code:** a new Python function, class or method that nothing in the repo refers to.
- **Static:** a new duplicated block (`jscpd`, run through `npx`), unused import or variable, or likely-bug and security finding (`ruff`); Node and `ruff` from `requirements.txt` must be present.
- **Docs:** the root `README.md` past its 40 KiB budget, or `README.md` and `docs/**/*.md` gaining a history marker (an issue reference, a dated heading or a changelog heading). State the present-tense why in words; history lives in the issue and `git log`.
- **Comment:** a file gaining an issue reference (`#NNN`) inside a Python, JS, CSS or PowerShell comment. A comment states the present-tense why.
- **Conventions:** a tracked Python file gaining a `no-window` hit (a subprocess spawn without `creationflags`) or a `no-drive-path` hit (a string literal starting with a drive letter). The other rules are off on purpose: `logging-not-print` scans `app/` and `src/`, which this repo does not have, and `secret-compare` and `git-wrapper` need a helper this repo does not have. A call that must break a rule carries a reasoned `# <rule>-exempt: <why>` marker.

## UX surface
- design spec applies: no        # no web app: a workshop slide deck (tips/), Streamlit demos and exercises, not a FastAPI + static-PWA UI
