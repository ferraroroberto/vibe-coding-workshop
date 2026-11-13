# Layout

This is workshop content, not an application: slides, exercises and demos. The decks are hand-written HTML, CSS and JS opened straight from the file system with no build step, so `.fleet.toml` declares the `static-site` shape. The workshop itself is site source and lives in `content/`, the shape's untyped folder; the seven workshop folders sit there as siblings so their relative links to each other (`../exercises/...`, `../slideshow/...`) keep working from the file system.

```
vibe-coding-workshop/
├── content/
│   ├── exercises/        # one folder per exercise: bilingual starter, solution, setup-data script, requirements (data/ is generated)
│   ├── slideshow/        # the workshop deck: slideshow_config.json drives the generated slideshow_data_{en,es}.js; each language is an HTML shell + stylesheet + data script
│   │   └── assets/       # one image per exercise plus welcome, menu, break and survey images
│   ├── slideshow_ai/     # the standalone bilingual "Not Everything Is AI" keynote, one hand-edited HTML file (no build)
│   │   ├── assets/       # keynote images
│   │   ├── kahoot/       # question exports for the audience quiz
│   │   └── mockups/      # self-contained live HTML demos linked from the keynote
│   ├── tips/             # the "Vibe Coding Tips" deck: index.html, styles.css, script.js
│   │   ├── docs/         # the written tips
│   │   └── examples/     # one worked example per tip
│   ├── preparation/      # how the deck, the images and the live bundle are built and extended
│   ├── streamlit_demo/   # Streamlit reference app
│   │   ├── pages/        # one file per demo page
│   │   ├── data/         # data loader for the demos
│   │   └── scripts/      # mock-data generator
│   └── metadata/         # standalone Streamlit survey dashboard with its own README
├── scripts/          # build and facilitator tooling, run from the repo root; also the vendored structure, instruction, doc-refs, dead-code, static, docs, comment and conventions ratchets and the gate
├── docs/             # this file, architecture.mmd and candidate-selection-state.md
└── .github/agents/   # a commit-and-push agent prompt
```

## Where new code goes

- A new exercise: a folder under `content/exercises/`, registered in `content/slideshow/slideshow_config.json`, then `scripts/build_slideshow.py` regenerates the deck.
- A new facilitator or build script: `scripts/`.
- A new keynote demo: `content/slideshow_ai/mockups/`.
- A new demo page: `content/streamlit_demo/pages/`.
- Reusable logic in the dashboard: a module in `content/metadata/`, split by concern. It has no subpackages, so stay under 40 modules.

## Declared exceptions

- **`content/exercises/**` is excluded from the structure ratchet.** Exercise solutions are teaching material, written long on purpose; splitting them would hide the point of the exercise.
