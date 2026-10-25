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

## Structure ratchet

- **Structure ratchet.** `scripts/verify-before-ship.ps1` runs `scripts/structure_ratchet.py`, which fails on a new file over 1,000 lines, a new function over 100 lines or a directory past 40 modules, and on any baselined offender that grows past its size in `.structure-ratchet-baseline.json`; exit 3 (git unusable, a file that does not parse) is a failure, never a pass. The script is the scaffold's, vendored byte-for-byte (`.fleet.toml` `[vendored]`, `[structure_ratchet]`): re-vendor with `/propagate-vendored structure_ratchet`, never edit. `exercises/**` is excluded (solutions are teaching material, written long on purpose) and no `shape` is declared. Shrink the baseline with `--update-baseline`; `--update-baseline --allow-additions` is the only way to add an entry and shows in review. Where code goes: [`docs/layout.md`](docs/layout.md).

## Instruction ratchet

- **Instruction ratchet.** `scripts/verify-before-ship.ps1` also runs `scripts/instruction_ratchet.py`, which lints `CLAUDE.md` and `AGENTS.md` against the weekly prompt audit's deterministic rules and fails when a rule-hit count rises above `.instruction-ratchet-baseline.json` (empty today) or a file passes its size cap; exit 3 is a failure, never a pass. Vendored byte-for-byte like the structure ratchet (`.fleet.toml` `[vendored]`, `[instruction_ratchet]`): re-vendor with `/propagate-vendored instruction_ratchet`, never edit.

## Doc refs ratchet

- **Doc refs ratchet.** `scripts/verify-before-ship.ps1` also runs `scripts/doc_refs_ratchet.py`, which fails when `README.md`, `CLAUDE.md` or `docs/` names a repo path, module, relative link or loopback port that does not exist, beyond the shrink-only `.doc-refs-ratchet-baseline.json` (one README path today); exit 3 is a failure, never a pass. Vendored byte-for-byte like the other ratchets (`.fleet.toml` `[vendored]`, `[doc_refs_ratchet]`): re-vendor with `/propagate-vendored doc_refs_ratchet`, never edit.

## Dead code ratchet

- **Dead code ratchet.** `scripts/verify-before-ship.ps1` also runs `scripts/dead_code_ratchet.py`, which fails when a new Python function, class or method appears that nothing in the repo refers to, beyond the shrink-only `.dead-code-ratchet-baseline.json`; exit 3 is a failure, never a pass. Vendored byte-for-byte like the other ratchets (`.fleet.toml` `[vendored]`, `[dead_code_ratchet]`): re-vendor with `/propagate-vendored dead_code_ratchet`, never edit.

## Static ratchet

- **Static ratchet.** `scripts/verify-before-ship.ps1` also runs `scripts/static_ratchet.py`, which fails when a new duplicated block (jscpd, run through `npx`), unused import or variable, or likely-bug and security finding (ruff, so Node and `ruff` from `requirements.txt` must be present) appears beyond the shrink-only `.static-ratchet-baseline.json` (empty today); exit 3 is a failure, never a pass. Vendored byte-for-byte like the other ratchets (`.fleet.toml` `[vendored]`, `[static_ratchet]`): re-vendor with `/propagate-vendored static_ratchet`, never edit.

## Docs ratchet

- **Docs ratchet.** `scripts/verify-before-ship.ps1` also runs `scripts/docs_ratchet.py`, which fails when the root `README.md` passes its size budget (40 KiB) or `README.md` and `docs/**/*.md` gain a history marker (an issue reference, a dated heading or a changelog heading) beyond the shrink-only `.docs-ratchet-baseline.json` (empty today); exit 3 is a failure, never a pass. State the present-tense why in words, and keep history in the issue and `git log`. Vendored byte-for-byte like the other ratchets (`.fleet.toml` `[vendored]`, `[docs_ratchet]`): re-vendor with `/propagate-vendored docs_ratchet`, never edit.

## Comment ratchet

- **Comment ratchet.** `scripts/verify-before-ship.ps1` also runs `scripts/comment_ratchet.py`, which fails when a file gains an issue reference (`#NNN`) inside a Python, JS, CSS or PowerShell comment beyond the shrink-only `.comment-ratchet-baseline.json` (empty today); exit 3 is a failure, never a pass. A comment states the present-tense why, and history lives in the issue and `git log`. Vendored byte-for-byte like the other ratchets (`.fleet.toml` `[vendored]`, `[comment_ratchet]`): re-vendor with `/propagate-vendored comment_ratchet`, never edit.

## UX surface
- design spec applies: no        # no web app: a workshop slide deck (tips/), Streamlit demos and exercises, not a FastAPI + static-PWA UI
