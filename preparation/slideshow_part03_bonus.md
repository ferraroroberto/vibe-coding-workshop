# Slideshow Part 3: Bonus Exercises Section

## Overview

This guide documents the **Bonus Exercises** section added to the workshop slideshow. It extends the structure from Part 1 (exercise slides) and Part 2 (sequence, menu, navigation) with:

- A **separate Bonus menu** (image + content) reachable from the main menu
- **Eight bonus-only exercises**, each with a title slide and a content slide
- **Navigation** between main menu, bonus menu, bonus exercises, break, and finish
- **Placeholder images** for the bonus exercises until custom images are generated (see `prompt_bonus_images_gemini.md`)

The **main menu** still lists all original exercises (including **Bonus: The Big Data Stress Test**), which stays on the main flow. The **Bonus Exercises** button opens the separate bonus menu with the eight additional exercises.

---

## What Was Added

### 1. Data split: main vs bonus

- **`mainExercises`**: The full `exercises` array (Intro, ETL 1–3, Viz 1–2, Auto 1–2, **Bonus: The Big Data Stress Test**). No exercises were removed from the main menu.
- **`bonusExercises`**: A separate array of 8 bonus-only exercises:
  - Auto: PDF Report  
  - ETL: API Pipeline  
  - Viz: D3 Bar Chart  
  - Viz: D3 Force Network  
  - Viz: Geo Heatmap  
  - Viz: Interactive Dashboard  
  - Viz: Seaborn Scatter  
  - Viz: Seaborn Statistical  

Each bonus exercise has: `number`, `title`, `image` (path under `assets/`), and `content` (markdown description).

### 2. Slide order (full sequence)

1. Welcome  
2. Team Agreement  
3. Main menu image  
4. Main menu content (main exercises list + **Bonus Exercises** + Break Time + Finish Session)  
5. **Main exercise slides** (9 × 2 = 18 slides: title + content for each main exercise)  
6. **Bonus menu image**  
7. **Bonus menu content** (list of 8 bonus exercises + ← Back to Menu + **Break Time** + Finish Session)  
8. **Bonus exercise slides** (8 × 2 = 16 slides: title + content for each bonus exercise)  
9. Break Time (with **← Back to Bonus** and **← Back to Menu**)  
10. Survey  
11. Congratulations  

### 3. New navigation

- **Main menu**
  - **Bonus Exercises** → `goToBonusMenu()` (bonus menu content slide).
  - Break Time, Finish Session unchanged.

- **Bonus menu**
  - Each bonus exercise item → `goToBonusExercise(index)` (that exercise’s title slide).
  - **← Back to Menu** → main menu content.
  - **Break Time** → break slide.
  - **Finish Session** → survey slide.

- **Bonus exercise slides**
  - **← Bonus Menu** → bonus menu content.
  - **← Main Menu** → main menu content.
  - **Break Time** → break slide.
  - **Finish Session** → survey slide.

- **Break Time slide**
  - **← Back to Bonus** → bonus menu content.
  - **← Back to Menu** → main menu content.

### 4. Styling

- Main and bonus menus share the same list style: **one line per exercise** (single-column grid: `grid-template-columns: 1fr` for `.menu-grid`).
- Bonus menu has a heading “Bonus Exercises” and the same `.menu-item` / `.menu-actions` styling as the main menu.
- Bonus exercise slides use the same `.slide-title` and `.slide-content` styles and the same `.exercise-actions` button block as main exercises.

### 5. Assets (images)

- **Main Bonus** (Big Data Stress Test): still uses `assets/etl_bonus_big_data.jpg` (unchanged).
- **Bonus-only exercises**: each uses an asset under `assets/`:
  - `bonus_auto_pdf_report.jpg`  
  - `bonus_etl_api_pipeline.jpg`  
  - `bonus_viz_d3_bar_chart.jpg`  
  - `bonus_viz_d3_force_network.jpg`  
  - `bonus_viz_geo_heatmap.jpg`  
  - `bonus_viz_interactive_dashboard.jpg`  
  - `bonus_viz_seaborn_scatter.jpg`  
  - `bonus_viz_seaborn_statistical.jpg`  

Until custom images exist, these can be **placeholder copies** of an existing asset (e.g. `etl_merger.jpg`). To replace them with real illustrations, use the prompt in **`preparation/prompt_bonus_images_gemini.md`** (e.g. with Gemini / Nano Banana Pro), then save the generated images with the exact filenames above into `assets/`. No slideshow code changes are required after substitution.

---

## Implementation summary

| Item | Implementation |
|------|----------------|
| Main menu | Shows all 9 exercises (including Big Data Stress Test) + Bonus Exercises + Break Time + Finish Session. |
| Bonus menu | Two slides (image + content). Content: 8 bonus items + Back to Menu + Break Time + Finish Session. |
| Bonus exercises | 8 exercises × 2 slides each; same layout and actions as main exercises, with Bonus Menu and Main Menu in actions. |
| Break slide | Buttons: “← Back to Bonus” and “← Back to Menu”. |
| Menu list style | Single column for both menus (one line per exercise). |
| Placeholder images | One placeholder image per bonus asset; replace with final art when ready. |

---

## Files to reference

- **Slideshow**: `slideshow.html` (generation logic, `mainExercises` / `bonusExercises`, `goToBonusMenu`, `goToBonusExercise`, break buttons).
- **Image creation**: `preparation/how_images_were_created.md` (style and process).
- **Prompt for new bonus images**: `preparation/how_images_were_created.md` Part 2 (table and instructions for Gemini / Nano Banana Pro).
- **Earlier parts**: `slideshow_part01_exercises.md`, `slideshow_part02_sequence.md`.

---

## Testing checklist

- [ ] Main menu shows all 9 exercises in one column and “Bonus Exercises”, “Break Time”, “Finish Session”.
- [ ] “Bonus Exercises” opens the bonus menu content slide.
- [ ] Bonus menu shows 8 exercises in one column and “← Back to Menu”, “Break Time”, “Finish Session”.
- [ ] Each bonus exercise opens its title slide; content slide has “← Bonus Menu”, “← Main Menu”, “Break Time”, “Finish Session”.
- [ ] From Break, “← Back to Bonus” goes to bonus menu and “← Back to Menu” to main menu.
- [ ] All bonus exercise images load (placeholders or final assets).
- [ ] Arrow keys still move through the full slide sequence including bonus slides.
