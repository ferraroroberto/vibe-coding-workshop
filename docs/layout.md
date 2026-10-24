# Layout

This is workshop content, not an application: slides, exercises and demos. There is no `app/`, `src/` or `tests/`, so no root-layout `shape` is declared and the structure ratchet's layout check reports "not applicable". The other four checks (file size, function length, flat directories, layer contract) run against `.structure-ratchet-baseline.json`.

```
vibe-coding-workshop/
├── exercises/        # one folder per exercise: bilingual starter, solution, setup-data script, requirements (data/ is generated)
├── slideshow/        # the workshop deck: slideshow_config.json drives the generated slideshow.html / slideshow_es.html
│   └── assets/       # one image per exercise plus welcome, menu, break and survey images
├── slideshow_ai/     # the standalone bilingual "Not Everything Is AI" keynote, one hand-edited HTML file (no build)
│   ├── assets/       # keynote images
│   ├── kahoot/       # question exports for the audience quiz
│   └── mockups/      # self-contained live HTML demos linked from the keynote
├── tips/             # the "Vibe Coding Tips" deck: index.html, styles.css, script.js
│   ├── docs/         # the written tips
│   └── examples/     # one worked example per tip
├── preparation/      # how the deck, the images and the live bundle are built and extended
├── scripts/          # build and facilitator tooling, run from the repo root; also the vendored structure and instruction ratchets and the gate
├── streamlit_demo/   # Streamlit reference app
│   ├── pages/        # one file per demo page
│   ├── data/         # data loader for the demos
│   └── scripts/      # mock-data generator
├── metadata/         # standalone Streamlit survey dashboard with its own README
├── docs/             # this file and architecture.mmd
└── .github/agents/   # a commit-and-push agent prompt
```

## Where new code goes

- A new exercise: a folder under `exercises/`, registered in `slideshow/slideshow_config.json`, then `scripts/build_slideshow.py` regenerates the deck.
- A new facilitator or build script: `scripts/`.
- A new keynote demo: `slideshow_ai/mockups/`.
- A new demo page: `streamlit_demo/pages/`.
- Reusable logic in the dashboard: a module in `metadata/`, split by concern. It has no subpackages, so stay under 40 modules.

## Declared exceptions

- **`exercises/**` is excluded from the structure ratchet.** Exercise solutions are teaching material, written long on purpose; splitting them would hide the point of the exercise.
- **No `shape`.** No preset fits workshop content, so the root-layout check is skipped rather than bent to match.
- **Baselined offenders** are two slideshow HTML files over 1,000 lines (built by `scripts/build_slideshow.py`) and eight long functions in `metadata/`, `scripts/test_libraries.py` and `streamlit_demo/pages/`. They are held at today's size and may not grow; splitting them is separate work.
