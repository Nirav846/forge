# FORGE Coach Trial Script v1

## Setup

1. Start the backend (from repo root):
   ```
   python run_forge_api.py
   ```

2. In a second terminal, start the frontend:
   ```
   cd forge_web && npm run dev
   ```

3. Open `http://localhost:5173` in a desktop browser
   (Chrome or Firefox recommended; 1280 px width minimum).

## Walkthrough Tasks

### Task 1 — Generate a basic program (5 min)

1. In the left panel, enter:
   - Athlete Name: "Test Athlete"
   - Sport: "Rugby"
   - Level: "Intermediate"
   - Available Minutes: 60
   - Goal: "Strength"
   - Mode: "Core"
2. Click **Generate**.
3. Look at the Coach Summary tab — read the rationale.
4. Switch to Block Builder — verify sessions and exercises render.

**What to look for:**
- Program generates in <5 seconds.
- Rationale text makes coaching sense.
- Exercises have sets, reps, rest, RPE.

### Task 2 — Premium athlete with injury flags (10 min)

1. Click the **UAT** button in the top header.
2. Click **PREM-01 (Rugby Prop)** in the sidebar.
3. Click **"Load into Form"**, close UAT, click **Generate**.
4. Inspect the Coach Summary — does it mention prop role?
5. Check personalization notes in the Right Panel — are shoulder risks noted?

**What to look for:**
- Role-specific coaching guidance appears.
- Injury flags produce visible adaptations in notes.

### Task 3 — Review weekly exposure data (10 min)

1. With the Rugby Prop program still loaded, scroll to the weekly
   summaries in Coach Summary view.
2. Look at each week's exposure summary: sprint, jump/landing,
   deceleration, eccentric, conditioning density.
3. Verify the data is real (counts and percentages, not "Not specified").
4. Compare with PREM-06 (Volleyball MB) which should show different
   jump/landing emphasis.

**What to look for:**
- Exposure data is per-week and varies by sport/role.
- Numbers are sensible (no negative counts, no 1000%+).

### Task 4 — Save, review, add notes (10 min)

1. With a program loaded, click **Save**.
2. Click **Approve** — badge changes to "Reviewed".
3. Click the **"Coach Notes"** expander below the properties strip.
4. Type "Good rotation emphasis for fast bowling" in coach notes.
5. Click outside the textarea — "Saving..." should appear briefly,
   then "Saved".
6. Type "Review this with lead S&C before delivery" in internal notes.
7. Click outside — same save feedback.

**What to look for:**
- Status toggle persists (reload artifact and confirm).
- Notes save on blur without losing the text.
- Save indicator shows different states (Saving → Saved).

### Task 5 — Duplicate and compare (10 min)

1. With a saved program loaded, click **Duplicate**.
2. A new copy appears with status "Draft".
3. Go back and load the original from the Library.
4. Switch to the **Compare** tab.
5. Select the duplicate program in the compare dropdown.

**What to look for:**
- Duplicate preserves the program content.
- Compare shows a structural diff without crashing.
- Duplicate starts as Draft (not Reviewed).

### Task 6 — Athlete delivery / print view (10 min)

1. With any program loaded, click **"Athlete View"** in the mode tabs.
2. Review the athlete-facing layout.
3. Click **"Print Document"** or use Ctrl+P (Cmd+P on Mac).
4. Check the print preview — page breaks, headers, readability.

**What to look for:**
- Debug/engineering content is hidden in Athlete View.
- Session headers break cleanly across pages.
- Exercise rows are readable (sets, reps, rest visible).
- Athlete name, sport, role, and goal appear at the top.

### Task 7 — Edge case: youth athlete (5 min)

1. Load CORE-02 (Youth Athlete, 16yo rugby beginner).
2. Generate and inspect the level — should show "Intermediate",
   not "Advanced" or "Beginner".
3. Verify exercises are age-appropriate.

**What to look for:**
- Youth safety cap activates (teenagers cannot be Advanced).
- Exercise difficulty matches the capped level.

### Task 8 — Edge case: deload (5 min)

1. Load CORE-04 (Deload, days_to_match=0).
2. Generate and inspect the summary — should mention recovery/deload.
3. Sessions should show reduced volume.

**What to look for:**
- Summary or rationale mentions deload/recovery.
- Session volume is noticeably lower than a normal program.

## Scoring rubric

After each task, rate on a 1–5 scale:

| Score | Meaning |
|---|---|
| 5 | Exceeds expectations — ready for athlete delivery |
| 4 | Meets expectations — minor polish needed |
| 3 | Acceptable — functional but rough |
| 2 | Below expectations — needs rework |
| 1 | Broken — unusable |

## Feedback template

```
Task: [Task number / name]
Score: [1–5]
What worked:
- ...
What didn't:
- ...
What I'd change:
- ...
```

Collect all task feedback and the UAT export, then return to the
development team. A full trial session should take 60–90 minutes.
