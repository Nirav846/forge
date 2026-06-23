# FORGE Workflow Reverse Engineering

> Coach workflow analysis across TrainingPeaks, TeamBuildr, Bridge Athletic, Volt Athletics, Mike Boyle CFSC, and Hawkin Dynamics.
> 58-program coaching patterns applied to UX design.

---

## 1. TrainingPeaks

### How a coach creates a workout

**Endurance flow:** Click `+` on calendar day → pick sport type → "Build Workout" tab → drag blocks from palette (Warm Up, Active, Recovery, Cool Down, Ramp, Repeats) → configure duration/intensity per block → Save.

**Strength flow:** Click `+` on calendar day → Strength → "New Strength Builder" → "Add Block +" → Single/Superset/Circuit → **type to search** the exercise library (no browse — text search only) → configure reps/weight/rest → Save.

### How a coach creates a program

Two methods: (A) Training Plan Library → `+` → name → blank calendar → add workouts day-by-day via drag from library or build on calendar. (B) Build on a dummy athlete calendar → Dual Calendar → drag-and-drop weeks into plan.

### How a coach saves templates

**No explicit template concept.** Workouts are saved as individual cards to the Workout Library folder system. Drag a workout from calendar into a Library folder. Reuse by dragging back. No parameterized templates — you save exact workouts.

### How a coach substitutes exercises

**No substitute button exists.** Delete the block → re-add → reconfigure (~5-8 clicks per substitution). This is a documented friction point even by TrainingPeaks' own content team.

### How a coach browses exercises

Endurance: 8 block types visible as drag tiles. Strength: **text search only** — 1000+ exercises with no category tree, no equipment filter, no muscle group filter. "Use a consistent naming convention" is the workaround in TP support articles.

### Click count to build a session

| Session | Clicks |
|---------|--------|
| Simple endurance (steady state) | 8-10 |
| Standard interval | 12-18 |
| Strength (6 exercises) | 25-35 |
| Strength superset (3×2) | 20-30 |

### Workflow friction

| Friction | Severity |
|----------|----------|
| No browsable exercise library — search only | High |
| No parameterized templates — each workout is a fixed structure | High |
| No substitute button — must delete and rebuild | Med |
| No undo on calendar operations | Med |
| Strength builder is desktop-only (no mobile create) | Med |
| Library organization is fully manual | Low-Med |
| No multi-athlete template push | Low |

---

## 2. TeamBuildr

### How a coach creates a workout

"Build" interface (new, ~2024-2025). Calendar-based: click a date → empty session → `Ctrl+N` or click "Add Exercise" → exercise picker modal → browse/filter by **tag** → select → configure sets/reps/RPE/%/tempo inline → repeat → add Session Breaks → add Notes/Warm-ups/Cool-downs → auto-saved.

Keyboard shortcuts: `Ctrl+N` (add), `Ctrl+C/V` (copy/paste exercises), `Ctrl+P` (add property), `Ctrl+D` (delete), `Ctrl+Z` (undo, beta).

### How a coach creates a program

**Date-based:** Build workouts on calendar → copy weeks via "Copy Day Split Patterns" or multi-select → adjust loads per week with comma-separated reps and %1RM. Progression View stacks all "Mondays" side-by-side across weeks.

**Free-form:** Dateless — athletes complete at own pace. Assign as block.

**Time to build a 4-week program:** 45-60 min from scratch, 15-20 min from templates. Users report copy-edit-repeat across weeks is "cumbersome."

### How a coach saves templates

"Save" from Build → named workout → Saved Programs library. Load by navigating to date → "Load Workout" → select. 700 exercises + 100+ pre-built S&C templates on Platinum plan. **Limitation:** recurring items cannot be saved or loaded.

### How a coach substitutes exercises

**Coach-initiated:** Filter by tag → see same-category alternatives → drag replacement over existing or delete + add (~4 clicks). Right-click/multi-select → delete → add.

**Athlete-initiated:** "Opt-Out" button in mobile app → reasons (Injury, Alternate Exercise, Lack of Equipment, Other) → can only substitute from exercises sharing same **tag**. Coach can prescribe a **Tag Select** instead of specific exercise — athlete picks within tag group.

### How a coach browses exercises

1000+ exercises in exercise library. **Tag system** for filtering (e.g., "Squat Variations", "Pulls", "Cleans"). Filter icon → select tag → narrowed list not search bar for name lookup. Sidebar shows tag distribution for session (e.g., "50% Lower Body").

**Limitation:** Full video library gated behind Platinum ($200/mo). Lower tiers have restricted video access.

### Click count to build a session

| Scenario | Clicks (mouse) | Clicks (keyboard) |
|----------|:---:|:---:|
| 1 exercise, 3 sets | 6-8 | 3-4 |
| 8-exercise session | 20-28 | 10-14 |
| 8-exercise + breaks + warm-up + notes | 30-40 | 18-24 |
| Full week (4 days, 8 exercises) from scratch | 120-160 | 60-90 |
| Substitute 1 exercise | 4 | 2-3 |

### Workflow friction

| Friction | Severity |
|----------|----------|
| Week-by-week copy-edit tedium — no native phase builder | High |
| Coach-side UI unintuitive per user reviews | High |
| No multiple concurrent programs per athlete | Medium |
| Conditioning programming is notes-only (no structured data) | Med-High |
| Recurring items excluded from save/load/copy | Medium |
| Phase/block builder still in beta | Medium |
| Calendar-locked architecture — workouts tied to dates | Low-Med |
| Learning curve requires 3-hour PowerUser course | Medium |

---

## 3. Bridge Athletic

### How a coach creates a workout

5-level hierarchy: Program → Phase → Week → Workout (Day) → Block → Exercise. Open a Program → click into Phase → Week → "Add Day" → "New Workout" or "Template Workout" → name → "Add Exercise" → search the 3000+ library → configure from 20+ parameters (reps, weight/%1RM/%Difficulty/%BW, RPE, time, distance, velocity, height, power, tempo, RIR, HR) → drag-and-drop reorder.

Builder has **Week View** (structural layout) and **Load Progression View** (edit metrics across multiple weeks simultaneously).

### How a coach creates a program

Navigate to Library → Programs → "New Program" → name → "Add Phase" (New/Template/Copy from Existing) → set duration + training days → build first week → **clone the week** to populate full phase → Load Progression View to adjust load across weeks → add additional phases.

**AI Import (beta):** Import from spreadsheets, PDFs, photos, or pasted text.

### How a coach saves templates

Four template levels:

| Level | Save method | Reuse |
|-------|-------------|-------|
| Program | No native "Save as Template" — must Clone + rename "(TEMPLATE)" manually | Clone the template → assign copy to athletes |
| Phase | Build → auto-saves | Insert via "Template Phase" |
| Workout | `⋮` → Save as Template → name | Add Day → Template Workout → search → Preview → Insert |
| Block | Save from Builder | Insert into any workout |
| Set | Save individual set configurations | Reuse set prescriptions |

### How a coach substitutes exercises

**Coach-initiated (Switch Exercise):** Hover over exercise → double-arrow "switch" icon → search replacement → choose **scope** (single instance / this day / this week / this phase / whole program) → keep same prescription or update → Save. **~5 clicks.**

**Athlete-initiated (Alternatives):** Select exercise → "Add Alternative Exercise" → designate as **Progression/Regression/Alternative** → set separate prescriptions per alternative → athletes see banner in app → can self-select. Coach tracks switches via Activity Report.

### How a coach browses exercises

**Exercise Library** (Library → Exercises): Table view with columns (Name, Edited By, Edited On). Filter by **tags** (left sidebar) and equipment type. Search as-you-type in Builder. 3000+ built-in exercises from ALTIS, Westside Barbell, Luka Hocevar, FMS, Hyperice. Custom exercises: create individually, bulk from spreadsheet, or import from YouTube. **No visual card/grid browsing** — everything is table-based.

### Click count to build a session

| Step | Clicks |
|------|:------:|
| Navigate to Library → Program → Builder | 3 |
| Add Day → New Workout → name | 3 |
| Add Exercise → search → select | 3 |
| Configure block (sets/reps/weight) | 3-5 |
| Per additional exercise | 6-8 |
| **Total for 3-exercise workout** | **24-30** |
| **From template** | **8-9** |

**Full program (4 weeks × 3 days):** ~288 from scratch, ~96 from templates.

### Workflow friction

| Friction | Severity |
|----------|----------|
| No native program template — must manually clone | High |
| Full builder is web-only (no mobile) | Med |
| Weak visual browsing — flat table, no grid/card view | Med |
| Scope confusion — broad scope can overwrite unrelated weeks | Med |
| No version history or undo | Med |
| Clone discipline required — editing template changes master | Med |
| Tag-dependent search quality | Med |
| Parameters don't auto-switch on exercise change | Low-Med |

---

## 4. Volt Athletics

### How a coach creates a workout

Workouts exist **only inside programs**. Two paths: (A) Pre-built program → click day → Edit (Training Editor slideover) → `+` → "Add Activity" (Warm-Up, Primer, Workout, Finisher, Conditioning, Custom, or Insert Template) → name → choose Workout Mode (Set/Circuit/Freestyle) → `+` Add movements → search/filter library → Edit Scheme → drag reorder → group/ungroup for supersets → "Apply Changes." (B) Blank program → same flow.

### How a coach creates a program

Three program types:

| Type | Duration | Clicks | Notes |
|------|----------|:------:|-------|
| Smart Program | 1-100 weeks | ~12-15 | Multi-phase, includes warm-ups, blend multiple programs |
| Classic Program | 52 weeks | ~8 | One workout/day, no warm-ups |
| Blank Program | 1-52 weeks | ~5 to scaffold | Full custom, then 6+ to populate |

Smart Program flow: Programs → Create Program → Smart Program → choose domain → choose template → customize (days/equipment/goals/duration) → Build My Program. **~12-15 clicks to generate a full program.**

### How a coach saves templates

Four template types in Content Library:

| Type | What it saves | Gate |
|------|---------------|------|
| Program Template | 1+ weeks of full training | Advanced+ |
| Activity Template | Single warm-up, workout, finisher | Advanced+ |
| Scheme Template | Set/rep progression (live-linked) | Advanced+ |
| Custom Movement | New exercise with video, cues, instructions | Advanced+ |

Save from program: `[…]` → "Save as Template" → select weeks → name. Reuse: In Training Editor, `+` → "Insert Template" → search/filter → select.

### How a coach substitutes exercises

**Movement Replacement tool:** Click replace icon (circular arrows) on any movement → choose scope (This Week Only / Entire Block / Forever) → see **6 recommended replacements** (same movement pattern, hand-picked by Volt CSCS coaches) → or search full library → confirm. **~4-5 clicks.**

**Athlete-side:** Athletes can replace movements in their app (toggle off per program). Cortex AI swaps based on available equipment.

### How a coach browses exercises

Content Library → Movements: List view with name, creator, category, subcategory, published status. Filters by category, subcategory, creator. Free-text search (use Volt abbreviations: BB, DB, KB, BW, RFE, FFE). 1500+ exercises with professional videos.

**Friction:** Must learn Volt's specific naming conventions and abbreviations. Help article explicitly tells users to "get familiar with abbreviations."

### Click count to build a session

| Scenario | Clicks |
|----------|:------:|
| Minimum simple session | 15-20 |
| Typical (4 movements + scheme edits) | 25-30 |
| Full week (3-5 sessions) | 75-150 |
| From template | 5-8 |

### Workflow friction

| Friction | Severity |
|----------|----------|
| Training Editor not universally available (team customers only) | High |
| Program creation split across 3 modalities with different features | High |
| Template features gated behind Advanced/Premium | High |
| No standalone workout creation — must live inside a program | Med |
| Exercise search requires learning Volt abbreviations | Med |
| Blank Program start date is irreversible | Med |
| Draft/Apply model adds overhead (changes not live until Applied) | Med |
| No "edit all weeks at once" for cross-program changes | Med |
| Athlete edit permissions only at program level (not per-athlete) | Low-Med |

---

## 5. Mike Boyle / CFSC Resources

### How a coach creates a workout

Not a software platform — a **methodology with a fixed slot taxonomy.** Workouts follow a template pattern:

| SuperSet | Slot | Monday (Upper Power) | Thursday (Lower Strength) |
|----------|------|---------------------|--------------------------|
| A1 (solo) | Explosive | Snatch GR variant | Clean GR variant |
| B1 | Vertical Pull | Chin-Up | Lat Pulldown |
| B2 | Knee Dominant | Front Squat | Single-Leg RDL |
| C1 | Horizontal Pull | KB Row | DB Row |
| C2 | Knee/Hip (alt) | Reverse Lunge | Hip Thrust |
| D1 | Press | DB Bench | DB Incline |
| D2 | Accessory | Triceps | Rotator Cuff |

**Rules:** Power always first (A1, never paired). Supersets B1+B2 (upper/lower non-interfering). C1+C2 (secondary pair). D1+D2 (isolation finisher). Tri-sets keep sessions under 60 min.

Coach selects the specific exercise for each slot from the correct movement category. No software enforces this — the CFSC manual and progression sheets are the reference.

### How a coach creates a program

1. Choose template (2-day, 3-day, or 4-day split)
2. Fill slots by movement category
3. Apply progression from CFSC sheets (L1-L5 per family)
4. Pair into supersets
5. Add foam rolling → mobility → activation → dynamic warm-up

### How a coach saves templates

Distributed via Excel spreadsheets and MBSC.tv / TrainHeroic. Template IS the program — coaches duplicate and modify the template structure. No save/load UI — it's file-based.

### How a coach substitutes exercises

Substitutions stay **within the same movement category.** CFSC Level 1 provides explicit progression/regression ladders per category. Decisions based on equipment availability, injury status, and skill level (L1-L5). No software automation — coach references the sheet and makes the call.

### How a coach browses exercises

By movement family, difficulty level (L1-L5), and equipment required. CFSC progression sheets are printed or PDF — no search, no filter UI.

### Workflow friction

| Friction | Severity |
|----------|----------|
| Manual slot management — Excel-based | High |
| No built-in exercise library — need separate progression sheet | High |
| Static templates — no auto-progression or loading calc | High |
| Pairing complexity tracked manually | Med |
| No constraint enforcement — can put two knee exercises in same session | Med |
| All weight progression is coach-calculated | High |

---

## 6. Hawkin Dynamics

### How a coach creates a workout

**Hawkin Dynamics does not have program or workout creation.** It is a force plate testing platform only. The workflow is: select test type (CMJ, SJ, DJ, Isometric, etc.) → apply a Tag → select athlete → run test → data flows to cloud → review on tablet or web.

### How a coach creates a program

**Not supported.** Zero program design functionality.

### How a coach saves templates

**Not applicable.** No templates, no workouts, no programs.

### How a coach substitutes exercises

**Not applicable.**

### How a coach browses exercises

9 test types available. That's the full "library." No exercise browsing.

### Workflow friction

| Friction | Severity |
|----------|----------|
| No program design at all — must use separate tool | High (for our context) |
| Static groups — data only flows if group created in advance | Med |
| Single-device limitation (tablet for capture, web for analysis) | Med |
| Metric overload — 50+ metrics with no sport-specific guidance | Low-Med |
| No warm-up integration | Low |

---

## Part A: Universal Coach Workflow Patterns

These patterns appear across **all platforms** that have program design:

### 1. The Slot Taxonomy
Every platform organizes workouts into ordered slots. TrainingPeaks has blocks (Warm Up → Active → Recovery). Bridge has Blocks within Workouts within Weeks within Phases. Boyle has A1, B1/B2, C1/C2, D1/D2. TeamBuildr has exercises + Session Breaks. The pattern is universal: **workouts are sequences of ordered slots, each slot has a purpose.**

### 2. The Template Hierarchy
All platforms use some form of: **template → instance**. Save a template, apply it to a date/athlete, modify the instance. Bridge has the deepest hierarchy (Program → Phase → Week → Workout → Block → Set). TrainingPeaks has flat workout cards. Volt has program-level and activity-level templates. **Deeper hierarchy = more granular reuse.**

### 3. The Search-Select-Configure Loop
Every exercise addition follows: **search/browse → select → configure parameters.** This loop repeats for every exercise. Platforms with tag-based browsing (TeamBuildr, Bridge) reduce friction vs search-only (TrainingPeaks). **The loop is the bottleneck.**

### 4. The Copy-Edit-Replicate Pattern
Every program building workflow is: build one unit (exercise/day/week) → copy it → edit the copy → replicate. Bridge clones weeks. TeamBuildr copies day patterns. Volt copies from previous week. TrainingPeaks uses Dual Calendar drag. **No platform auto-generates program structure from coaching intent.**

### 5. Power Always First
Every platform that supports Ballistic/Olympic exercises places them first in the slot order. Boyle's A1 rule. TrainingPeaks places power in the early-session "prime" zone. This is universal and non-negotiable.

### 6. Templates Reduce Build Time by 3-5×
All platforms show template users build 3-5× faster. Bridge: 288 clicks from scratch → 96 from templates. TeamBuildr: 45-60 min → 15-20 min. Volt: 75-150 clicks/week → 5-8 per session. **Template systems are the single highest-leverage UX investment.**

### 7. Substitution Is Distinct From Creation
Every platform has a different mental model for substitution:
- TrainingPeaks: no substitute concept (delete + rebuild)
- TeamBuildr: tag-based same-category replacement
- Bridge: scope-aware switch (instance/day/week/phase/program)
- Volt: recommended alternatives (6 same-pattern picks)
- Boyle: within-category ladders
The winning pattern is Bridge's scope control + Volt's recommended alternatives.

### 8. Exercise Libraries Are the Foundation
Every platform maintains a library of 700-3000+ exercises. None of them have a built-in ontology of movement families, difficulty levels, or progression ladders. Libraries are flat lists with tags. **No platform has a coaching knowledge base built into the library.**

---

## Part B: Common UX Mistakes

### Mistake 1: Search-Only Exercise Discovery
TrainingPeaks makes coaches type to find exercises. Volt requires learning abbreviations. TeamBuildr buries the filter behind an icon. **The fix:** browse-by-family as primary mode (FORGE's 15 families), search as secondary. A coach should see "Double Leg Knee Dominant" as a section, not a tag.

### Mistake 2: No Parameterized Templates
TrainingPeaks saves exact workouts. TeamBuildr saves date-tethered sessions. Bridge has no program-level template save. **The fix:** templates with variables — "3×5 @ RPE 8" as a scheme template, not an instance. Volt's Scheme Template (live-linked) is the closest, but gated behind Premium.

### Mistake 3: Calendar-First Architecture
TeamBuildr and TrainingPeaks anchor everything to dates. This forces coaches into copy-edit-replicate rather than phase-block-design. Bridge and Volt abstract above the calendar (Programs → Phases → Weeks → Days). **The fix:** abstract coaching first, calendar second. "Design the program" then "assign to dates."

### Mistake 4: No Constraint Awareness
None of these platforms know that "Horizontal Push + Vertical Push in the same slot" creates interference, or that "Knee Dominant + Ballistic" should precede "Hip Dominant" in slot order. Boyle's system has the knowledge but no enforcement. **The fix:** embed the coaching knowledge base into the builder. The ontology should guide slot order, not just tag exercises.

### Mistake 5: Templates Gated Behind Paywalls
Volt locks templates behind Advanced/Premium. TeamBuildr gates video library behind Platinum ($200/mo). **The fix:** templates are the core value proposition. They should be the free/default tier, not premium.

### Mistake 6: No True Substitution Gesture
TrainingPeaks has none. TeamBuildr's is multi-click. Bridge's has scope confusion. Volt's is buried behind an icon. **The fix:** a single gesture — right-click (or long-press) → "Replace with..." → pick from same-family alternatives. The ontology already knows which exercises are in the same family.

### Mistake 7: Web-Only Builder
Bridge is web-only for full program creation. TrainingPeaks strength builder is desktop-only. Volt's Training Editor is team-only. **The fix:** the builder should work on tablet (where coaches coach) as a progressive web app. Full capability on mobile, parity with desktop.

### Mistake 8: No "Auto-Fill From Blueprint"
No platform lets a coach say "I want a Full Body Strength program for 4 weeks, 3 days/week" and auto-populate the mandatory families. Every platform makes coaches build from a flat exercise list. **The fix:** this is FORGE's killer feature — the blueprints already define mandatory families. One click to populate a session skeleton.

---

## Part C: Minimum Viable FORGE Workflow

### Design Principles

1. **Blueprint-first, not calendar-first.** Coach picks a goal, not a date.
2. **Families before exercises.** Coach fills movement categories, then picks specific lifts.
3. **Substitution is a right-click.** Same-family alternatives always one gesture away.
4. **Templates are free and infinite.** Every session, day, week, phase, and program can be saved as a template.
5. **Tablet-native.** The builder must work on a 10" screen in portrait mode while standing in a weight room.

### The 3-Minute Draft Program Workflow

```
Step 1: Pick Blueprint
────────────────────────
Screen: Blueprint grid (14 cards, visual)
Coach taps: "Full Body Strength"
System sets: mandatory families (1 DLKD, 1 DLHD, 1 HPush, 1 HPull, 1 Core)
           : slot order (Power → Knee → Push → Hip → Pull → Core)
           : default frequency (3×/week)
Clicks so far: 1
Time so far: ~5 seconds

Step 2: Set Parameters
───────────────────────
Screen: Parameter sheet (slide-up)
Coach sets: duration (4 weeks), days/week (3), athlete level (Intermediate)
System calculates: 12 sessions → auto-populates weekly structure
           : maps difficulty to L3 default
           : shows week 1 on screen
Clicks so far: 4 (blueprint + 3 parameter fields)
Time so far: ~20 seconds

Step 3: Assign Exercises to Slots
──────────────────────────────────
Screen: Session skeleton with mandatory family slots
         Each slot shows: [Family name] → "Tap to choose"
Coach taps slot: "DLKD"
System shows: 12 DLKD exercises, sorted by difficulty L3, with video thumbnails
Coach taps: "Barbell Back Squat" (sets auto-default to 3×5)
System fills slot. Moves to next unfilled slot.

Coach taps: "DLHD" → "RDL"
Coach taps: "HPush" → "Barbell Bench Press"
Coach taps: "HPull" → "Barbell Row"
Coach taps: "Core" → "Dead Bug" (core goes last automatically)

Clicks so far: ~10 (5 slots × 2 clicks each)
Time so far: ~60 seconds (assuming coach knows their exercises)

Step 4: Review & Customize
───────────────────────────
Screen: Full session view with all 5 exercises
         Each shows: name, sets × reps, rest
Coach can: tap any exercise → adjust sets/reps/rest
          : tap "Swap" icon → see 6 same-family alternatives (Volt pattern)
          : tap "Add Slot" → add optional family (Vertical Push, etc.)
          : tap "Copy to Tuesday" → duplicate session to next training day
          : tap "Progression View" → see load across weeks (Bridge pattern)

Coach taps: "Copy to Tuesday" → auto-adjusts (may change exercises per blueprint rules)
Coach taps: "Copy to Thursday" → auto-adjusts
Coach adjusts: Thursday's DLKD → "Front Squat" for variation

Clicks so far: ~16
Time so far: ~90 seconds

Step 5: Name, Save, Assign
───────────────────────────
Coach names: "Pre-Season Foundation"
Coach taps: "Save as Template" (auto-saves to library)
Coach taps: "Assign" → select athletes/groups
Coach confirms: assign as "Start Next Monday" with auto-progression

Clicks so far: ~20
Time so far: ~120 seconds (2 minutes)
Full 4-week draft program complete.
```

### Click Comparison

| Platform | 4-week program (from scratch) | 1 session (from scratch) |
|----------|:---:|:---:|
| TrainingPeaks | 300+ (strength) | 25-35 |
| TeamBuildr | 480-640 | 20-28 |
| Bridge Athletic | ~288 | 24-30 |
| Volt Athletics | ~200 (Smart Program auto-gen) | 25-30 |
| **FORGE (blueprint-first)** | **~20** | **~10** |

### The Click Reduction Drivers

| Feature | Clicks Saved vs Bridge | Why |
|---------|:---:|-----|
| Blueprint selection instead of blank program | -15 | No scaffold creation, no Add Phase, no Add Day. One tap sets structure. |
| Family-first exercise selection | -8 per session | Coach selects a family, not a flat search. Family narrows to ~12 exercises automatically. |
| Auto-populated progression | -12 per program | No manual Load Progression View editing across weeks. System applies periodization from blueprint logic. |
| Session copy with auto-variation | -6 per week | No manual "clone week → edit each day" Bridge pattern. System varies exercises within blueprint constraints. |
| Right-click substitute | -4 per substitution | No search → replace → re-scope Bridge flow. One gesture + pick from 6 same-family alternatives (Volt pattern). |

### What FORGE Should Copy

| From | Copy |
|------|------|
| Bridge Athletic | Scope-aware substitution (this instance / this week / this phase) |
| Bridge Athletic | Alternative exercises with Progression/Regression/Alternative designation |
| Volt Athletics | Recommended replacements (6 same-pattern picks) |
| Volt Athletics | Scheme Templates (live-linked set/rep progressions) |
| Volt Athletics | Smart Program (answer goal questions → generate structure) |
| TeamBuildr | Tag-based substitution prevention (can't swap across families) |
| TeamBuildr | Progression View (stacked days across weeks) |
| Boyle / CFSC | Fixed slot taxonomy (A1, B1/B2 pattern) |
| Boyle / CFSC | Tri-set structure for time-efficient sessions |
| TrainingPeaks | Dual Calendar (dummy athlete → plan) pattern for edge cases |

### What FORGE Should Avoid

| From | Avoid |
|------|-------|
| TrainingPeaks | Search-only exercise library. Must have browse-by-family. |
| TrainingPeaks | No substitute button. Must have one-click replacement. |
| TeamBuildr | Calendar-first architecture. Programs should be calendar-agnostic. |
| TeamBuildr | Conditioning as free-text notes. Must be structured data. |
| Bridge Athletic | No native program template. Must have explicit "Save as Template" for all levels. |
| Bridge Athletic | Table-only exercise library. Must have visual card/grid mode. |
| Volt Athletics | Templates gated behind paywall. All template types are free. |
| Volt Athletics | Irreversible Blank Program start date. Must be editable. |
| Boyle / CFSC | Manual weight progression. Must auto-calculate from %1RM. |
| Boyle / CFSC | No constraint enforcement. System must guide slot order. |

---

## Appendix: The Killer Feature Gap

**No existing platform connects session slot order to coaching knowledge.**

TrainingPeaks knows you added a "Warm Up" block but won't stop you adding it mid-session. TeamBuildr knows you tagged "Squat" but won't tell you it should precede "Deadlift" in slot order. Bridge knows you made a phase but won't suggest which movement families belong in it.

**FORGE's advantage** is that the coaching reference database (191 exercises, 15 families, 14 blueprints, substitution matrices, progression ladders, session flow rules) already exists as structured knowledge. The UX question is not "how to design a workout builder" — it's "how to make the knowledge base the interface."

The minimum viable FORGE workflow answers the success criterion:

> **"How can a coach create a credible draft program in under 3 minutes with fewer clicks than TeamBuildr or Bridge Athletic?"**

**Answer:** Blueprint-first selection (1 click → 5 mandatory families auto-populated), family-first exercise browsing (2 clicks per slot → session skeleton in 10 clicks), session copy with auto-variation (1 click → program fills), and right-click same-family substitution (2 clicks per swap). Total: ~20 clicks for a 4-week program vs Bridge's ~288 or TeamBuildr's ~480-640. Draft time: ~2 minutes vs 45-60 minutes.

The knowledge base isn't content — it's the shortest path to done.
