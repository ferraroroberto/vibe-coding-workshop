# How the Workshop Images Were Created

All Minion-style illustrations used in this Python vibe coding workshop were generated with **Google Gemini** (image generation / conversational AI). The conversation and generations were done in a single Gemini chat thread.

**Gemini chat used:** [https://gemini.google.com/app/ee68aab63de3a8b3](https://gemini.google.com/app/ee68aab63de3a8b3)

---

## Process Overview

1. **Define the storyline**  
   The workshop is a “day in the life” of a data analyst. Each exercise has a scenario (e.g. “The First Request”, “The Sanity Check”). The goal was one Minion illustration per exercise that follows this narrative.

2. **Provide the exercise table**  
   The full table (Section, Exercise, Scenario/Narrative, Tech Focus) was pasted into Gemini so it could align each image with the correct story beat.

3. **Generate in batches**  
   - First: the **9 exercise images** (Intro + ETL 1–3 + Viz 4–5 + Auto 6–7 + Bonus 8).  
   - Then: the **5 workshop slides** (Welcome, Congratulations, Break Time, Team Agreement, Survey/Participants Opinion).  
   - Finally: the **exercises list / menu** image (Minion chef presenting the workshop as a menu).

4. **Iterate on prompts**  
   Descriptions were refined in the same chat (e.g. “Survey” should feel like feedback/suggestions, not inquisitive; Minion expression adjusted to be more neutral).

---

## Image Sets and Corresponding Assets

### 1. Exercise storyline (9 images)

| # | Section | Exercise | Scenario / narrative | Asset file |
|---|:--------|:---------|:---------------------|:-----------|
| 0 | Intro | Hello World | Day 1: Setting up your cockpit. Proving you can fly. | `intro_python.jpg` |
| 1 | ETL | The Great Merger | The boss sends 3 quarterly sales files; combine into one YTD report. | `etl_merger.jpg` |
| 2 | ETL | The Detective | Combined data looks suspicious (duplicates, negative sales); clean it. | `etl_detective.jpg` |
| 3 | ETL | The Messy Survey | HR sends a messy CSV; correlate sales with employee satisfaction. | `etl_survey.jpg` |
| 4 | Viz | The Manager's Chart | Manager wants “Revenue by Category” chart for the presentation. | `viz_managers_chart.jpg` |
| 5 | Viz | The Report Generator | Boss wants numbers behind the chart; Excel with Summary + Data tabs. | `viz_report_generator.jpg` |
| 6 | Auto | The Professional Polish | Automate Excel formatting (bold headers, auto-fit) to impress. | `auto_excel_polish.jpg` |
| 7 | Auto | The File Organizer | Project done; folder full of random dumps; organize workspace. | `auto_file_organizer.jpg` |
| 8 | Bonus | The Big Data Stress Test | Company scales 100x; laptop can’t handle the files. | `etl_bonus_big_data.jpg` |

### 2. Workshop slides (5 images)

| Slide | Purpose | Asset file |
|:------|:--------|:-----------|
| Welcome | Opening slide; friendly, inviting. | `welcome.jpg` |
| Congratulations | End-of-workshop celebration (confetti, congratulatory sign). | `congratulations.jpg` |
| Break Time | Mid-workshop break (e.g. relaxed Minion, beach vibe). | `break_time.jpg` |
| Team Agreement | Collaboration; Minions around a “TEAM AGREEMENT” whiteboard. | `team_agreement.jpg` |
| Survey / Participants Opinion | Feedback and suggestions; neutral, helpful (suggestion box, clipboard). | `survey.jpg` |

### 3. Supporting menu (1 image)

| Use | Description | Asset file |
|:----|:------------|:-----------|
| Exercises list / menu | Minion chef presenting the workshop exercises as a menu (Appetizers, Main Courses, Dessert). | `menu.jpg` |

All assets live in the repo under **`assets/`**.

---

## Tips for Recreating or Extending

- **Keep one Gemini thread** for the whole set so the style and “Minion” look stay consistent.  
- **Reference the exercise table** (e.g. from `exercises_selection.md`) when asking for new exercise images.  
- **Specify tone** when it matters (e.g. “Survey = feedback/suggestions, neutral and helpful, not inquisitive”).  
- **Ask for small edits** (e.g. expression, props, text on signs) in follow-up messages in the same chat.

Using the link above, you can reopen the same Gemini conversation to see the exact prompts and regenerate or adapt images.
