# FORGE UAT Runner Guide

## What is the UAT Runner?

The UAT Runner is a built-in testing tool inside the FORGE Coach Console.
It loads structured test scenarios so a tester or coach can systematically
verify that FORGE behaves correctly across many athlete profiles.

## How to open the UAT Runner

1. Start FORGE (backend + frontend running).
2. In the top-left header of the Coach Console, click the **UAT** button
   (green, next to the Library button).
3. The UAT Runner opens as a modal overlay.

## How to load a scenario into the form

1. In the UAT Runner, click a scenario name in the left sidebar.
2. The right panel shows the scenario details and checklist.
3. Click **"Load into Form"** — this populates the left panel input fields
   with the scenario's athlete parameters.
4. Close the UAT Runner and click **Generate** to run the scenario.
5. The generated program appears in the center panel.

## How to mark pass/fail

1. Generate the program and inspect the output (Coach Summary view,
   Block Builder view, Athlete Delivery view, Right Panel).
2. Open the UAT Runner again if closed.
3. For each checklist item, click **Pass** (green) or **Fail** (red).
4. Results are saved immediately to your browser's local storage.

## How results are stored

- Results stay in your browser (`localStorage`).
- They survive page reloads but **not** clearing browser data or switching
  browsers/machines.
- Results are **not** sent to any server — they stay on your machine.

## How to export results

1. Open the UAT Runner.
2. In the top-right of the header, click **"Export JSON"**.
3. A JSON file downloads containing all scenarios, their checklists, and
   pass/fail states.
4. Share this file with your team or attach it to trial feedback.

The export includes:
- Scenario ID and name
- Each checklist item and its pass/fail state
- Completion timestamp
- Summary statistics (total checks, passed, failed)

## How to reset results

1. Open the UAT Runner.
2. Click **"Reset"** (red text button in the top-right header).
3. All stored results are cleared immediately.
4. This cannot be undone.

## How to use it during a live trial session

**Before the session:**
- Open the UAT Runner and reset any old results.
- Have the Export file ready for recording at the end.

**During the session:**
- For each scenario the coach wants to test, load it into the form,
  generate, inspect, and mark pass/fail.
- Let the coach explore the output freely — the runner is a checklist,
  not a straitjacket.

**After the session:**
- Export the JSON results.
- Attach the export to your trial feedback.

**16 scenarios available:**

| ID | Tier | Description |
|---|---|---|
| CORE-01 | Core | General Fitness Adult |
| CORE-02 | Core | Youth Athlete (16yo rugby) |
| CORE-03 | Core | No Sport / Minimal Inputs |
| CORE-04 | Core | Deload / Maintenance |
| PREM-01 | Premium | Rugby Prop (force deficit) |
| PREM-02 | Premium | Rugby Backline (velocity deficit) |
| PREM-03 | Premium | Cricket Fast Bowler |
| PREM-04 | Premium | Cricket Batter |
| PREM-05 | Premium | Tennis Singles |
| PREM-06 | Premium | Volleyball Middle Blocker |
| PREM-07 | Premium | Basketball Guard |
| PREM-08 | Premium | Soccer Midfielder |
| EDGE-01 | Edge | Very Short Session (20 min) |
| EDGE-02 | Edge | Competition Taper (D2M=3) |
| EDGE-03 | Edge | Multiple Injury Flags |
| EDGE-04 | Edge | Missing Optional Fields |
