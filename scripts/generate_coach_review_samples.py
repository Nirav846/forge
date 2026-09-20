"""FORGE Coach Review Sample Pack Generator.

Generates deterministic, full-program sample packs per sport for
external S&C coach review. Each sport gets one consolidated markdown
file with all role × level combinations (2 variants each) plus a
sport-specific review sheet.

Usage:
    python scripts/generate_coach_review_samples.py
    python scripts/generate_coach_review_samples.py --sport cricket
"""

import sys, os, time, datetime, argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase
)
from src.forge.main import generate_program
from src.forge.api_serializers import serialize_program
from src.forge.renderer import render_block_summary, render_coach_program
from src.forge.role_week_planning import (
    get_role_week_profile, get_role_week_notes, render_role_week_summary
)

# ── SPORT CONFIG ─────────────────────────────────────────────────────
# (internal_key, coach_name, roles_internal)
SPORTS_CONFIG: list[tuple[str, str, list[str]]] = [
    ("cricket",   "Cricket",               ["fast_bowler", "spin_bowler", "batter", "wicketkeeper", "all_rounder"]),
    ("rugby",     "Rugby",                 ["prop", "hooker", "lock", "back_row", "scrum_half", "fly_half", "centre", "back_three"]),
    ("tennis",    "Tennis",                ["singles", "doubles"]),
    ("badminton", "Badminton",             ["singles", "doubles"]),
    ("volleyball","Volleyball",            ["middle_blocker", "outside_hitter", "opposite", "setter", "libero"]),
    ("soccer",    "Soccer",                ["goalkeeper", "centre_back", "fullback", "midfielder", "winger", "striker"]),
    ("football",  "Football (American)",   ["goalkeeper", "centre_back", "fullback", "midfielder", "winger", "striker"]),
    ("basketball","Basketball",            ["guard", "wing", "big"]),
]

LEVEL_NAMES = ["BEGINNER", "INTERMEDIATE", "ADVANCED"]
LEVEL_DISPLAY = {"BEGINNER": "Beginner", "INTERMEDIATE": "Intermediate", "ADVANCED": "Advanced"}

# ── DISPLAY HELPERS ──────────────────────────────────────────────────

def _role_display(role: str) -> str:
    return role.replace("_", " ").title()

def _sample_id(sport_key: str, role: str, level: str, variant: str) -> str:
    return f"{sport_key.upper()}_{role.upper()}_{level}_{variant}"

# ── DETERMINISTIC SCENARIO BUILDER ──────────────────────────────────
# Each level has two base templates (A/B). Sport/role tweaks override fields.
# Everything is explicit, deterministic, and documented.

LEVEL_TEMPLATES = {
    "BEGINNER": [
        # (age, training_age, goal, minutes, freq, season, equip, tc, strength_base, cmj, sprint, squat, aerobic, fv_profile)
        (16, 0.5, "general",       45, 2, "off_season",  "Basic Gym",       0.70, False, "",    "",    "",    "",    None),
        (17, 0.8, "strength",      60, 2, "pre_season",  "Basic Gym",       0.70, False, "low","",    "",    "",    None),
    ],
    "INTERMEDIATE": [
        (20, 2.0, "strength",      60, 3, "off_season",  "Commercial Gym",  0.85, True,  "",    "",    "",    "",    None),
        (22, 2.5, "power",         60, 3, "pre_season",  "Commercial Gym",  0.85, True,  "avg", "avg", "",    "",    "balanced"),
    ],
    "ADVANCED": [
        (26, 5.0, "power",         75, 4, "pre_season",  "Commercial Gym",  0.95, True,  "",    "",    "",    "",    None),
        (30, 7.0, "conditioning",  75, 4, "in_season",   "Elite Facility",  0.95, True,  "high","high","high","high","balanced"),
    ],
}

# Role-specific overrides — these tweak the base template for meaningful variation
ROLE_TWEAKS: dict[tuple[str, str], list[dict]] = {
    # Each entry: (sport, role) -> [variant_A_overrides, variant_B_overrides]
    ("cricket", "fast_bowler"):    [{"goal": "speed",       "minutes": 60}, {"goal": "power",       "minutes": 60, "freq": 3}],
    ("cricket", "spin_bowler"):    [{"goal": "power",       "minutes": 60}, {"goal": "conditioning","minutes": 60}],
    ("cricket", "batter"):         [{"goal": "power",       "minutes": 60}, {"goal": "strength",     "minutes": 75}],
    ("cricket", "wicketkeeper"):   [{"goal": "conditioning","minutes": 45}, {"goal": "strength",     "minutes": 60}],
    ("cricket", "all_rounder"):    [{"goal": "strength",    "minutes": 60}, {"goal": "conditioning","minutes": 75}],
    ("rugby", "prop"):             [{"goal": "strength",    "minutes": 60}, {"goal": "mass",         "minutes": 60}],
    ("rugby", "hooker"):           [{"goal": "strength",    "minutes": 60}, {"goal": "power",        "minutes": 60}],
    ("rugby", "lock"):             [{"goal": "power",       "minutes": 60}, {"goal": "strength",     "minutes": 75}],
    ("rugby", "back_row"):         [{"goal": "conditioning","minutes": 60}, {"goal": "power",        "minutes": 75}],
    ("rugby", "scrum_half"):       [{"goal": "speed",       "minutes": 60}, {"goal": "conditioning","minutes": 60}],
    ("rugby", "fly_half"):         [{"goal": "power",       "minutes": 60}, {"goal": "speed",        "minutes": 60}],
    ("rugby", "centre"):           [{"goal": "power",       "minutes": 60}, {"goal": "conditioning","minutes": 75}],
    ("rugby", "back_three"):       [{"goal": "speed",       "minutes": 60}, {"goal": "power",        "minutes": 60}],
    ("tennis", "singles"):         [{"goal": "conditioning","minutes": 75}, {"goal": "power",        "minutes": 60}],
    ("tennis", "doubles"):         [{"goal": "power",       "minutes": 60}, {"goal": "conditioning","minutes": 60}],
    ("badminton", "singles"):      [{"goal": "conditioning","minutes": 75}, {"goal": "speed",        "minutes": 60}],
    ("badminton", "doubles"):      [{"goal": "power",       "minutes": 60}, {"goal": "conditioning","minutes": 60}],
    ("volleyball", "middle_blocker"):[{"goal": "power",     "minutes": 60}, {"goal": "strength",     "minutes": 75}],
    ("volleyball", "outside_hitter"):[{"goal": "power",     "minutes": 60}, {"goal": "conditioning","minutes": 60}],
    ("volleyball", "opposite"):    [{"goal": "power",       "minutes": 60}, {"goal": "strength",     "minutes": 75}],
    ("volleyball", "setter"):      [{"goal": "conditioning","minutes": 60}, {"goal": "strength",     "minutes": 60}],
    ("volleyball", "libero"):      [{"goal": "conditioning","minutes": 75}, {"goal": "speed",        "minutes": 60}],
    ("soccer", "goalkeeper"):      [{"goal": "power",       "minutes": 60}, {"goal": "strength",     "minutes": 60}],
    ("soccer", "centre_back"):     [{"goal": "strength",    "minutes": 60}, {"goal": "power",        "minutes": 75}],
    ("soccer", "fullback"):        [{"goal": "conditioning","minutes": 60}, {"goal": "speed",        "minutes": 60}],
    ("soccer", "midfielder"):      [{"goal": "conditioning","minutes": 75}, {"goal": "power",        "minutes": 60}],
    ("soccer", "winger"):          [{"goal": "speed",       "minutes": 60}, {"goal": "conditioning","minutes": 60}],
    ("soccer", "striker"):         [{"goal": "power",       "minutes": 60}, {"goal": "speed",        "minutes": 75}],
    ("football", "goalkeeper"):    [{"goal": "power",       "minutes": 60}, {"goal": "strength",     "minutes": 60}],
    ("football", "centre_back"):   [{"goal": "strength",    "minutes": 60}, {"goal": "power",        "minutes": 75}],
    ("football", "fullback"):      [{"goal": "conditioning","minutes": 60}, {"goal": "speed",        "minutes": 60}],
    ("football", "midfielder"):    [{"goal": "conditioning","minutes": 75}, {"goal": "power",        "minutes": 60}],
    ("football", "winger"):        [{"goal": "speed",       "minutes": 60}, {"goal": "conditioning","minutes": 60}],
    ("football", "striker"):       [{"goal": "power",       "minutes": 60}, {"goal": "speed",        "minutes": 75}],
    ("basketball", "guard"):       [{"goal": "conditioning","minutes": 60}, {"goal": "speed",        "minutes": 75}],
    ("basketball", "wing"):        [{"goal": "power",       "minutes": 60}, {"goal": "conditioning","minutes": 60}],
    ("basketball", "big"):         [{"goal": "strength",    "minutes": 60}, {"goal": "power",        "minutes": 75}],
}


def _map_equip(val: str) -> EquipmentProfile:
    return {"Basic Gym": EquipmentProfile.BASIC_GYM,
            "Commercial Gym": EquipmentProfile.COMMERCIAL_GYM,
            "Elite Facility": EquipmentProfile.ELITE_FACILITY,
            "Field Only": EquipmentProfile.FIELD_ONLY}.get(val, EquipmentProfile.COMMERCIAL_GYM)

def _map_season(val: str) -> SeasonPhase:
    return {"off_season": SeasonPhase.OFF_SEASON,
            "pre_season": SeasonPhase.PRE_SEASON,
            "in_season": SeasonPhase.IN_SEASON,
            "transition": SeasonPhase.TRANSITION}.get(val, SeasonPhase.OFF_SEASON)


def build_athlete_profile(sport_key: str, role: str, level_name: str, variant: str) -> AthleteProfile:
    idx = 0 if variant == "A" else 1
    base = LEVEL_TEMPLATES[level_name][idx]
    age, ta, goal, minutes, freq, season, equip, tc, strength_ok, cmj, sprint_10, squat, aero, fv = base

    tweaks = ROLE_TWEAKS.get((sport_key, role), [{}, {}])
    override = tweaks[idx]
    goal = override.get("goal", goal)
    minutes = override.get("minutes", minutes)
    if "freq" in override:
        freq = override["freq"]

    equip_e = _map_equip(equip)
    season_e = _map_season(season)

    return AthleteProfile(
        sport=sport_key,
        training_age_years=float(ta),
        season_phase=season_e,
        goal=goal,
        equipment_profile=equip_e,
        athlete_level=AthleteLevel[level_name],
        technique_consistency=tc,
        injury_status="none",
        injury_history=[],
        fatigue_level="normal",
        weeks_since_break=0,
        available_minutes=minutes,
        days_to_match=None,
        age=age,
        preferred_families=6,
        strength_base_met=strength_ok,
        position_role=role,
        force_profile=fv or None,
        lumbar_risk=False,
        patellar_tendon_risk=False,
        hamstring_risk=False,
        shoulder_overhead_risk=False,
        groin_adductor_risk=False,
        ankle_foot_risk=False,
        cmj_band=cmj or None,
        sprint_10m_band=sprint_10 or None,
        squat_strength_band=squat or None,
        aerobic_band=aero or None,
    )


# ── RENDERING ────────────────────────────────────────────────────────

def _rationale_bullets(program, serialized, sport_key, role, level_name, variant):
    from src.forge.data import BLUEPRINT_BY_ID
    bp = BLUEPRINT_BY_ID.get(program.blueprint_id)
    bullets = []
    if bp:
        bullets.append(f"**Blueprint**: {bp.name} — {bp.purpose}")
        bullets.append(f"**Best phase**: {', '.join(bp.best_season_phase)} | **Best training age**: {bp.best_training_age}")
    notes = get_role_week_notes(sport_key, role)
    if notes:
        for n in notes:
            bullets.append(f"**Role week note**: {n}")
    if program.personalization_notes:
        for pn in program.personalization_notes[:4]:
            bullets.append(f"**Personalization**: {pn}")
    if serialized:
        for r in serialized.get("rationale", [])[:6]:
            bullets.append(f"**Rationale**: {r}")
        for v in serialized.get("validation", [])[:3]:
            bullets.append(f"**Validation**: {v}")
    return bullets


def _exposure_table(program):
    from src.forge.progression_engine import program_role_exposure_summary
    rows = program_role_exposure_summary(program)
    return rows


def _coach_prompts(sport_key: str, role: str, level_name: str) -> list[str]:
    role_d = _role_display(role)
    level_d = LEVEL_DISPLAY[level_name]
    prompts = [
        f"Does this **{role_d} ({level_d})** program feel role-appropriate?",
        "Is the weekly training frequency appropriate for this athlete archetype?",
        "Are exercise selections and sequencing coach-like and sport-relevant?",
        "Does the conditioning density match the sport's physiological demands?",
        "Is the loading / intensity progression realistic for this level?",
        "What is the single most impactful change you would make?",
        "Would you trust this program with a real athlete at this level?",
    ]
    return prompts


def render_sample(program, serialized, sport_key, coach_name, role, level_name, variant) -> str:
    sid = _sample_id(sport_key, role, level_name, variant)
    role_d = _role_display(role)
    level_d = LEVEL_DISPLAY[level_name]
    idx = 0 if variant == "A" else 1

    base = LEVEL_TEMPLATES[level_name][idx]
    age, ta, goal, minutes, freq, season, equip, tc, strength_ok, *_ = base
    tweaks = ROLE_TWEAKS.get((sport_key, role), [{}, {}])
    override = tweaks[idx]
    goal = override.get("goal", goal)
    minutes = override.get("minutes", minutes)
    freq = override.get("freq", freq)

    lines = []
    lines.append(f"## Sample: {sid}")
    lines.append("")

    # ── Profile header ──
    lines.append("### Athlete Profile")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    lines.append(f"| **Sample ID** | `{sid}` |")
    lines.append(f"| **Sport** | {coach_name} |")
    lines.append(f"| **Role** | {role_d} |")
    lines.append(f"| **Level** | {level_d} |")
    lines.append(f"| **Age** | {age} |")
    lines.append(f"| **Training Age** | {ta} years |")
    lines.append(f"| **Goal** | {goal.replace('_', ' ').title()} |")
    lines.append(f"| **Days/Week** | {freq} |")
    lines.append(f"| **Session Duration** | {minutes} min |")
    lines.append(f"| **Season Phase** | {season.replace('_', ' ').title()} |")
    lines.append(f"| **Equipment** | {equip} |")
    lines.append(f"| **Technique Consistency** | {tc} |")
    lines.append(f"| **Strength Base Met** | {'Yes' if strength_ok else 'No'} |")
    if serialized:
        lines.append(f"| **Blueprint** | {serialized.get('summary', {}).get('blueprint_selected', 'N/A')} |")
        lines.append(f"| **Credibility Score** | {serialized.get('summary', {}).get('credibility_score', 'N/A')} |")
    lines.append("")

    # ── Why this sample ──
    lines.append("### Why This Sample Exists")
    lines.append("")
    archetype_bullets = [
        f"Represents a **{level_d.lower()} {role_d}** athlete in the **{coach_name.lower()}** pathway.",
        f"Training age of {ta} year(s) with {'limited' if ta < 2 else 'solid' if ta < 5 else 'extensive'} gym history.",
        f"Goal emphasis: **{goal.replace('_', ' ').title()}** — drives blueprint selection and session architecture.",
        f"Competition context: **{season.replace('_', ' ').title()}** — affects volume, intensity, and conditioning density.",
        f"Equipment access: **{equip}** — constrains exercise selection and loading options.",
        f"Variant **{variant}** of two — differs in goal emphasis, training load, or seasonal context to show FORGE's range within the same archetype.",
    ]
    for b in archetype_bullets:
        lines.append(f"- {b}")
    lines.append("")

    # ── Role profile summary ──
    lines.append("### Role Profile / Bias Summary")
    lines.append("")
    role_profile = get_role_week_profile(sport_key, role)
    for note in get_role_week_notes(sport_key, role):
        lines.append(f"- {note}")
    lines.append("")
    for rl in render_role_week_summary(role_profile):
        lines.append(f"- {rl}")
    lines.append("")

    # ── Program summary ──
    if serialized:
        summary = serialized.get("summary", {})
        lines.append("### Program Summary")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|---|---|")
        lines.append(f"| **Blueprint** | {summary.get('blueprint_selected', 'N/A')} |")
        lines.append(f"| **Duration** | {summary.get('total_weeks', 'N/A')} weeks |")
        lines.append(f"| **Frequency** | {summary.get('weekly_frequency', 'N/A')}x/week |")
        lines.append(f"| **Conditioning Emphasis** | {summary.get('conditioning_emphasis', 'N/A')} |")
        lines.append(f"| **Competition Window** | {summary.get('competition_window', 'N/A')} |")
        lines.append(f"| **Role Emphasis** | {summary.get('role_emphasis', 'N/A')} |")
        lines.append(f"| **Credibility Score** | {summary.get('credibility_score', 'N/A')} |")
        lines.append("")

    # ── Block summary (week-by-week) ──
    lines.append("### Block Overview (Week-by-Week)")
    lines.append("")
    block_summary = render_block_summary(program)
    lines.append("```")
    for line in block_summary.split("\n"):
        lines.append(line)
    lines.append("```")
    lines.append("")

    # ── Full program ──
    lines.append("### Full Program Output")
    lines.append("")
    lines.append("```")
    full = render_coach_program(program)
    for line in full.split("\n"):
        lines.append(line)
    lines.append("```")
    lines.append("")

    # ── Weekly exposure summary ──
    if serialized and "weeks" in serialized:
        lines.append("### Weekly Exposure Summary")
        lines.append("")
        lines.append("| Week | Sprint | Jump/Landing | Decel | Eccentric | Cond. Density | Type |")
        lines.append("|---|---|---|---|---|---|---|")
        for w in serialized["weeks"]:
            es = w.get("exposure_summary", {})
            lines.append(f"| {w.get('label', '')} | {es.get('sprint_exposure', '-')} | {es.get('jump_landing_exposure', '-')} | {es.get('deceleration_exposure', '-')} | {es.get('eccentric_stress', '-')} | {es.get('conditioning_density', '-')} | {es.get('week_type', '-')} |")
        lines.append("")

    # ── Program rationale ──
    lines.append("### Program Rationale")
    lines.append("")
    for b in _rationale_bullets(program, serialized, sport_key, role, level_name, variant):
        lines.append(f"- {b}")
    lines.append("")

    # ── Validation notes ──
    if serialized and serialized.get("validation"):
        lines.append("### Validation / Credibility Output")
        lines.append("")
        for v in serialized["validation"]:
            lines.append(f"- {v}")
        lines.append("")

    # ── Coach review prompts ──
    lines.append("### Coach Review Prompts")
    lines.append("")
    for prompt in _coach_prompts(sport_key, role, level_name):
        lines.append(f"- [ ] {prompt}")
    lines.append("")
    lines.append("---")
    lines.append("")

    return "\n".join(lines)


# ── REVIEW SHEET TEMPLATES ──────────────────────────────────────────

REVIEW_QUESTIONS: dict[str, list[str]] = {
    "cricket": [
        "Do fast bowler programs reflect realistic bowling-related landing / eccentric / sprint demands?",
        "Are batter programs rotational enough without becoming gimmicky?",
        "Is the difference between fast bowler, spinner, batter, wicketkeeper, and all-rounder meaningful and sport-specific?",
        "Are conditioning and lower-limb exposures appropriate for in-season vs off-season cricket demands?",
        "Does the spin bowler profile appropriately emphasize rotation and core without neglecting general strength?",
        "Is the wicketkeeper program distinct enough from batter?",
        "Do all-rounder programs successfully blend batting and bowling demands without compromising either?",
    ],
    "rugby": [
        "Do prop / hooker / lock / back-row programs feel meaningfully different from each other?",
        "Is collision robustness / force development emphasized appropriately for tight forwards?",
        "Are speed / back-three athletes protected from excessive strength bias?",
        "Does the weekly training density match rugby's physical demands?",
        "Are scrum-half and fly-half differentiated adequately?",
        "Do back-line programs reflect position-specific COD and sprint profiles?",
        "Is the contact readiness / injury prevention logic visible in the programs?",
    ],
    "tennis": [
        "Do singles vs doubles programs diverge in a believable, sport-specific way?",
        "Is COD / elastic / rotational / conditioning work appropriate for court athletes?",
        "Does the lower-body loading (eccentric, landing) fit court movement demands?",
        "Is shoulder / overhead volume managed appropriately?",
        "Do advanced programs reflect higher tennis-specific conditioning requirements?",
        "Is there enough differentiation between off-season and in-season programming?",
    ],
    "badminton": [
        "Do singles vs doubles programs diverge meaningfully?",
        "Is the high sprint / agility exposure appropriate for badminton's repeated explosive demands?",
        "Does landing / jump exposure reflect badminton's unilateral landing patterns?",
        "Is the upper body loading balanced given badminton's overhead dominance?",
        "Do advanced programs reflect the sport's extreme conditioning requirements?",
    ],
    "volleyball": [
        "Is jump / landing exposure appropriately high for middle blockers and outsides?",
        "Is the libero program distinct enough from other volleyball roles?",
        "Does the setter program reflect the unique physical demands of setting?",
        "Are shoulder / overhead volumes managed appropriately for hitters?",
        "Is the difference between middle blocker, outside hitter, and opposite meaningful?",
        "Do beginner programs appropriately limit plyometric volume for young athletes?",
    ],
    "soccer": [
        "Do goalkeeper programs appropriately prioritize plyometric / explosive work?",
        "Are centre-back and fullback programs differentiated in a sport-specific way?",
        "Is the high sprint / deceleration exposure for wide players appropriate?",
        "Does the midfielder program reflect the highest conditioning demands?",
        "Are striker and winger programs differentiated enough?",
        "Is lower body loading balanced with soccer's eccentric / hamstring demands?",
    ],
    "football": [
        "Do goalkeeper programs appropriately prioritize plyometric / landing demands?",
        "Are centre-back and fullback programs differentiated appropriately for American football?",
        "Is the high conditioning / sprint exposure for skill positions appropriate?",
        "Does the midfielder (linebacker) program reflect two-way play demands?",
        "Are striker (receiver / RB) and winger programs differentiated enough?",
        "Is strength / power emphasis appropriately periodized across levels?",
    ],
    "basketball": [
        "Are guard / wing / big programs differentiated in a sport-specific way?",
        "Is jump / landing exposure appropriately high given basketball's plyometric demands?",
        "Does the big program appropriately prioritize strength without losing vertical emphasis?",
        "Is the guard's sprint / agility / change-of-direction work appropriate?",
        "Do advanced programs reflect higher in-season maintenance requirements?",
        "Is the upper/lower body split appropriate for the sport's demands?",
    ],
}

def render_review_sheet(sport_key: str, coach_name: str, roles: list[str]) -> str:
    role_display_list = "\n".join(f"  - {_role_display(r)}" for r in roles)
    questions = REVIEW_QUESTIONS.get(sport_key, [])

    scorecard_rows = "\n".join(
        f"| {cat:40s} | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Notes: |"
        for cat in [
            "Role specificity",
            "Level appropriateness",
            "Exercise selection quality",
            "Weekly structure & sequencing",
            "Dose / loading appropriateness",
            "Power-speed-strength balance",
            "Conditioning appropriateness",
            "Overall coach credibility",
            "Would you trust this with a real athlete?",
        ]
    )

    q_rows = "\n".join(f"| {i+1}. {q} | |" for i, q in enumerate(questions))

    now = datetime.date.today().strftime("%Y-%m-%d")

    return f"""# {coach_name} — Coach Review Sheet

**Generated**: {now}
**Sport**: {coach_name}
**Purpose**: External S&C coach evaluation of FORGE sample programs

---

## A) What FORGE Is Trying to Do for {coach_name}

FORGE is an AI-driven program generation engine that produces periodised,
role-specific strength and conditioning programs for athletes across multiple
sports. For {coach_name}, it covers {len(roles)} role profiles:

{role_display_list}

Each role is sampled at three levels (Beginner, Intermediate, Advanced) with
two program variants per level to demonstrate range within an archetype.

---

## B) Scoring Rubric (1–10)

Please score each category on a 1–10 scale where:
- **1–3**: Needs fundamental redesign
- **4–6**: Has promise but needs significant adjustment
- **7–8**: Solid — minor tweaks only
- **9–10**: Coach-ready as-is

| Category | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
{scorecard_rows}

---

## C) Sport-Specific Review Questions

Please add comments for each question:

| Question | Coach Comments |
|---|---|
{q_rows}

---

## D) Sample-by-Sample Feedback

| Sample ID | What Works | What Is Off | Biggest Correction | Coach Confidence (1–10) |
|---|---|---|---|---|
| | | | | |
| | | | | |
| | | | | |

*(Add rows as needed for each sample you review)*

---

## E) Final Summary

**Which sport / role outputs are strongest?**


**Which sport / role outputs need the most work?**


**Would you be willing to trial FORGE on real athletes?**
- [ ] Yes, as-is
- [ ] Yes, after the corrections above
- [ ] No — need to see more
- [ ] No — fundamental concerns (please elaborate):


**Additional comments:**


---

*Thank you for your time and expertise. Your feedback directly shapes the evolution of FORGE.*
"""


# ── MAIN GENERATION ──────────────────────────────────────────────────

def generate_sport_pack(sport_key: str, coach_name: str, roles: list[str], out_dir: str):
    """Generate sample pack + review sheet for one sport."""
    sport_dir = os.path.join(out_dir, sport_key)
    os.makedirs(sport_dir, exist_ok=True)

    pack_path = os.path.join(sport_dir, f"{sport_key}_sample_pack.md")
    review_path = os.path.join(sport_dir, f"{sport_key}_review_sheet.md")

    print(f"\n{'='*60}")
    print(f"  {coach_name} ({sport_key}) — {len(roles)} roles × 3 levels × 2 variants = {len(roles) * 3 * 2} programs")
    print(f"{'='*60}")

    # ── Build coverage matrix ──
    all_samples = []  # [(sample_id, program, serialized, role, level_name, variant)]

    total = len(roles) * len(LEVEL_NAMES) * 2
    count = 0
    t0 = time.time()

    for role in roles:
        for level_name in LEVEL_NAMES:
            for variant in ("A", "B"):
                count += 1
                sid = _sample_id(sport_key, role, level_name, variant)
                print(f"  [{count}/{total}] Generating {sid}...", end="", flush=True)

                try:
                    profile = build_athlete_profile(sport_key, role, level_name, variant)
                    program = generate_program(profile)
                    serialized = serialize_program(program)
                    all_samples.append((sid, program, serialized, role, level_name, variant))
                    print(" OK")
                except Exception as e:
                    print(f" FAIL: {e}")
                    all_samples.append((sid, None, None, role, level_name, variant))

    elapsed = time.time() - t0
    print(f"  Generated {count} programs in {elapsed:.0f}s ({elapsed/count:.1f}s avg)")

    # ── Write sample pack ──
    print(f"  Writing sample pack...", end="", flush=True)
    with open(pack_path, "w", encoding="utf-8") as f:
        f.write(f"# FORGE {coach_name} Coach Review Sample Pack\n\n")
        f.write(f"**Generated**: {datetime.date.today().strftime('%Y-%m-%d')}  \n")
        f.write(f"**Generator**: `scripts/generate_coach_review_samples.py`  \n")
        f.write(f"**Purpose**: External S&C coach review — {len(all_samples)} samples across {len(roles)} roles × {len(LEVEL_NAMES)} levels\n\n")

        f.write("## How to Use This Pack\n\n")
        f.write("1. Review the **Coverage Matrix** below to understand the scope.\n")
        f.write("2. Each **role × level** section contains two samples (A and B).\n")
        f.write("3. Each sample includes: athlete profile, rationale, full program, exposure summary.\n")
        f.write("4. At the end of each sample, use the **Coach Review Prompts** to guide your feedback.\n")
        f.write("5. Record your overall feedback in the separate **Review Sheet** (`*_review_sheet.md`).\n\n")

        f.write("## Coverage Matrix\n\n")
        f.write("| Role | Level | Variant A | Variant B |\n")
        f.write("|---|---|---|---|\n")

        for role in roles:
            for level_name in LEVEL_NAMES:
                sid_a = _sample_id(sport_key, role, level_name, "A")
                sid_b = _sample_id(sport_key, role, level_name, "B")
                f.write(f"| {_role_display(role)} | {LEVEL_DISPLAY[level_name]} | `{sid_a}` | `{sid_b}` |\n")

        f.write("\n---\n\n")

        # ── Write each sample ──
        prev_role_level = None
        for sid, program, serialized, role, level_name, variant in all_samples:
            rl_key = (role, level_name)
            if rl_key != prev_role_level:
                role_d = _role_display(role)
                level_d = LEVEL_DISPLAY[level_name]
                f.write(f"\n# {role_d} — {level_d}\n\n")
                prev_role_level = rl_key

            if program is None:
                f.write(f"## Sample: {sid}\n\n")
                f.write(f"**Generation failed.** See error above.\n\n---\n\n")
            else:
                f.write(render_sample(program, serialized, sport_key, coach_name, role, level_name, variant))

        f.write("\n---\n\n")
        f.write(f"*End of {coach_name} sample pack — {len(all_samples)} samples*\n")

    print(" OK")

    # ── Write review sheet ──
    print(f"  Writing review sheet...", end="", flush=True)
    with open(review_path, "w", encoding="utf-8") as f:
        f.write(render_review_sheet(sport_key, coach_name, roles))
    print(" OK")

    return len(all_samples)


def main():
    parser = argparse.ArgumentParser(description="Generate FORGE coach review sample packs")
    parser.add_argument("--sport", type=str, default=None, help="Sport key to generate (default: all)")
    args = parser.parse_args()

    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample")
    os.makedirs(out_dir, exist_ok=True)

    total_samples = 0
    total_sports = 0

    for sport_key, coach_name, roles in SPORTS_CONFIG:
        if args.sport and sport_key != args.sport:
            continue
        total_sports += 1
        n = generate_sport_pack(sport_key, coach_name, roles, out_dir)
        total_samples += n

    # Write README
    readme_path = os.path.join(out_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# FORGE Coach Review Sample Packs\n\n")
        f.write(f"**Generated**: {datetime.date.today().strftime('%Y-%m-%d')}\n\n")
        f.write(f"This folder contains sample program packs generated by FORGE for\n")
        f.write(f"external S&C coach review. Each sport has its own subfolder with:\n\n")
        f.write(f"- `*_sample_pack.md` — Consolidated markdown with all samples\n")
        f.write(f"- `*_review_sheet.md` — Sport-specific coach feedback sheet\n\n")
        f.write(f"## Coverage\n\n")
        f.write(f"| Sport | Roles | Levels | Samples |\n")
        f.write(f"|---|---|---|---|\n")
        for sport_key, coach_name, roles in SPORTS_CONFIG:
            if args.sport and sport_key != args.sport:
                continue
            total_for_sport = len(roles) * len(LEVEL_NAMES) * 2
            f.write(f"| {coach_name} | {len(roles)} | {len(LEVEL_NAMES)} | {total_for_sport} |\n")
        f.write(f"\n**Total samples generated**: {total_samples}\n\n")
        f.write(f"## Level Buckets\n\n")
        f.write(f"| Level | Training Age | Age Range | Technique Consistency | Description |\n")
        f.write(f"|---|---|---|---|---|\n")
        f.write(f"| Beginner | < 1 year | 15–18 | < 0.80 | Limited gym history, youth athletes |\n")
        f.write(f"| Intermediate | 1–3 years | 19–25 | >= 0.85 | Some training base, developing |\n")
        f.write(f"| Advanced | 3+ years | 24–35 | >= 0.95 | Extensive training history |\n\n")
        f.write(f"## Regeneration\n\n")
        f.write(f"To regenerate all sample packs:\n\n")
        f.write(f"```bash\npython scripts/generate_coach_review_samples.py\n```\n\n")
        f.write(f"To regenerate a single sport:\n\n")
        f.write(f"```bash\npython scripts/generate_coach_review_samples.py --sport cricket\n```\n\n")
        f.write(f"The generator is fully deterministic — same inputs produce identical outputs.\n")
        f.write(f"Scenario parameters are defined explicitly in the generator script.\n")
        f.write(f"Programs are generated via the real FORGE engine (`generate_program()`).\n")

    print(f"\n{'='*60}")
    print(f"  Generated {total_samples} samples across {total_sports} sports")
    print(f"  Output: {out_dir}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
