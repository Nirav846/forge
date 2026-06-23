"""Program renderer — outputs human-readable + structured program text."""
from .models import Session, SessionBlock, GeneratedProgram, Exercise, WarmupProtocol, RecoveryProtocol
from .validator import verify_credibility, calculate_credibility_score
from .progression_engine import (
    TESTING_CATEGORIES, program_exposure_summary, program_role_exposure_summary,
    plan_weeks, plan_testing,
)
from .role_week_planning import get_role_week_profile, get_role_week_notes, render_role_week_summary


def render_program(program: GeneratedProgram) -> str:
    lines = []
    lines.append(f"FORGE Generated Program")
    lines.append(f"{'=' * 60}")
    lines.append(f"Athlete: {program.athlete}")
    lines.append(f"Blueprint: {program.blueprint_name} (ID: {program.blueprint_id})")
    lines.append(f"Level: {program.level}")
    lines.append(f"Duration: {program.duration} weeks, {program.frequency}x/week")
    lines.append(f"Goal: {program.goal}")
    lines.append(f"Equipment: {program.equipment_profile}")
    lines.append(f"Credibility: {program.credibility_score:.1f}/1.0 ({program.credibility_score * 100:.0f}%)")

    total_cred = 0.0
    for i, session in enumerate(program.sessions):
        check = verify_credibility(session, program.athlete_profile)
        score = calculate_credibility_score(check)
        total_cred += score
        week_num = (i // program.frequency) + 1
        wt = getattr(session, 'week_type', '')
        lines.append("")
        session_label = f"Session {i + 1}" if program.frequency <= 1 else f"Week {week_num} / Session {i + 1}"
        if wt:
            session_label += f" ({wt})"
        lines.append(render_session(session, session_label, score))

    avg_cred = round(total_cred / len(program.sessions), 2) if program.sessions else 0
    lines.append("")
    lines.append(f"{'=' * 60}")
    lines.append(f"Average Session Credibility: {avg_cred:.1f}/1.0 ({avg_cred * 100:.0f}%)")
    return "\n".join(lines)


def render_coach_program(program: GeneratedProgram) -> str:
    lines = []
    lines.append(f"{program.athlete}")
    lines.append(f"{'=' * 50}")
    lines.append(f"Level: {program.level} | {program.frequency}x/week | {program.duration} weeks")
    lines.append(f"Goal: {program.goal} | Equipment: {program.equipment_profile}")
    if program.personalization_notes:
        lines.append("")
        lines.append("Personalization Notes:")
        for note in program.personalization_notes:
            lines.append(f"  {note}")

    if hasattr(program, 'warmup') and program.warmup:
        lines.append("")
        lines.append(render_warmup(program.warmup))

    for i, session in enumerate(program.sessions):
        week_num = (i // program.frequency) + 1
        wt = getattr(session, 'week_type', '')
        header = f"--- W{week_num} S{i + 1}" + (f" ({wt})" if wt else "") + " ---"
        lines.append("")
        lines.append(header)
        lines.append(render_coach_session(session))

    if hasattr(program, 'recovery') and program.recovery:
        lines.append("")
        lines.append(render_recovery(program.recovery))

    lines.append("")
    lines.append(f"{'=' * 50}")
    return "\n".join(lines)


def render_warmup(warmup: 'WarmupProtocol') -> str:
    lines = ["WARMUP", "-" * 30]
    for phase in warmup.phases:
        if not phase.drills:
            continue
        lines.append(f"  {phase.name} ({phase.duration_sec // 60} min)")
        for drill in phase.drills:
            lines.append(f"    - {drill.name} ({drill.duration_sec // 60} min)")
            if drill.coaching_cue:
                lines.append(f"      Cue: {drill.coaching_cue}")
    return "\n".join(lines)


def render_coach_session(session: Session) -> str:
    lines = []
    if session.testing_categories:
        labels = [TESTING_CATEGORIES.get(c, {}).get("label", c) for c in session.testing_categories]
        lines.append(f"  [TEST] {' | '.join(labels)}")
    for block in session.blocks:
        lines.append(f"  [{block.family.value}] {block.family_name}")
        for ex in block.exercises:
            if block.prescription:
                p = block.prescription
                rest_str = f"{p.rest_seconds // 60}:{p.rest_seconds % 60:02d} min" if p.rest_seconds >= 120 else f"{p.rest_seconds}s"
                lines.append(f"    - {ex.name}  {p.sets} x {p.reps}  |  {p.intensity_note}  |  rest: {rest_str}")
            else:
                lines.append(f"    - {ex.name}")
    if session.conditioning:
        cond = session.conditioning
        lines.append(f"  Conditioning: {cond.name}")
        lines.append(f"    {cond.work_description}")
    if session.adjustment_note:
        lines.append(f"  [Adj] {session.adjustment_note}")
    lines.append(f"  Est. time: {session.total_duration_min} min")
    return "\n".join(lines)


def render_block_summary(program: GeneratedProgram) -> str:
    lines = []
    lines.append("BLOCK SUMMARY")
    lines.append("=" * 60)
    lines.append(f"{program.athlete}")
    lines.append(f"Blueprint: {program.blueprint_name} | Level: {program.level} | {program.frequency}x/week | {program.duration} weeks")
    lines.append(f"Goal: {program.goal} | Equipment: {program.equipment_profile}")
    lines.append(f"Program Score: {program.credibility_score:.1f}/1.0 ({program.credibility_score * 100:.0f}%)")
    if program.personalization_notes:
        lines.append("")
        lines.append("Personalization:")
        for note in program.personalization_notes:
            lines.append(f"  {note}")
    lines.append("")

    # Week-by-week table
    header = f"{'Wk':>3} | {'Intent':<18} | {'Tests':<30} | Adj | Notes"
    lines.append(header)
    lines.append("-" * len(header))

    sessions = program.sessions
    freq = program.frequency
    for week in range(1, program.duration + 1):
        start = (week - 1) * freq
        end = min(start + freq, len(sessions))
        week_sessions = sessions[start:end]
        if not week_sessions:
            continue

        wt = week_sessions[0].week_type
        tests = set()
        adjustments = set()
        for s in week_sessions:
            tests.update(s.testing_categories)
            if s.adjustment_note:
                adjustments.add(s.adjustment_note)

        test_str = ", ".join(TESTING_CATEGORIES.get(t, {}).get("label", t).replace(" Test", "") for t in tests) if tests else ""
        adj_flag = "Y" if adjustments else ""
        notes = "; ".join(adjustments)
        test_trunc = test_str[:30] if len(test_str) > 30 else test_str

        lines.append(f"W{week:>2} | {wt:<18} | {test_trunc:<30} | {adj_flag:>3} | {notes}")

    lines.append("")

    # Exposure summary
    lines.append("Exposure by Week:")
    for exp_line in program_role_exposure_summary(program):
        lines.append(exp_line)

    # Wave 8: Role week bias summary
    ap = program.athlete_profile
    if ap and ap.position_role:
        role_profile = get_role_week_profile(ap.sport, ap.position_role)
        lines.append("")
        lines.append("Role Week Bias:")
        for note in get_role_week_notes(ap.sport, ap.position_role):
            lines.append(f"  {note}")
        lines.append("")
        lines.append("Role Weekly Emphasis Targets:")
        for target_line in render_role_week_summary(role_profile):
            lines.append(target_line)

    # Testing summary
    testing_weeks = [(w, s.testing_categories) for w in range(1, program.duration + 1)
                     for s in sessions[(w - 1) * freq:min(w * freq, len(sessions))]
                     if s.testing_categories]
    if testing_weeks:
        lines.append("")
        lines.append("Testing / Benchmarking:")
        seen_weeks = set()
        for w, cats in testing_weeks:
            if w not in seen_weeks:
                cat_labels = [TESTING_CATEGORIES.get(c, {}).get("label", c) for c in cats]
                lines.append(f"  Week {w}: {', '.join(cat_labels)}")
                seen_weeks.add(w)

    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)


def render_recovery(recovery: 'RecoveryProtocol') -> str:
    lines = ["RECOVERY", "-" * 30]
    lines.append(f"  {recovery.name} (L{recovery.level}) — {recovery.duration_min} min")
    for drill in recovery.drills:
        lines.append(f"  - {drill.name} ({drill.duration_sec // 60} min)")
    return "\n".join(lines)


def render_session(session: Session, label: str, credibility: float) -> str:
    lines = [f"--- {label} (Credit: {credibility}/1.0) ---"]

    if session.testing_categories:
        labels = [TESTING_CATEGORIES.get(c, {}).get("label", c) for c in session.testing_categories]
        lines.append(f"  [TEST] {' | '.join(labels)}")

    if session.adjustment_note:
        lines.append(f"  [Adj] {session.adjustment_note}")

    for block in session.blocks:
        lines.append(render_block(block))

    if session.conditioning:
        cond = session.conditioning
        lines.append(f"  Conditioning: {cond.name} ({cond.system})")
        lines.append(f"    {cond.work_description}")
        lines.append(f"    Duration: {cond.duration} | Sets: {cond.sets} | Rest: {cond.rest}")

    lines.append(f"  Total estimated time: {session.total_duration_min} min")
    return "\n".join(lines)


def render_block(block: SessionBlock) -> str:
    lines = [f"  [{block.family.value}] {block.family_name}"]
    for ex in block.exercises:
        if block.prescription:
            p = block.prescription
            rest_str = f"{p.rest_seconds // 60}:{p.rest_seconds % 60:02d} min" if p.rest_seconds >= 120 else f"{p.rest_seconds}s"
            lines.append(f"    - {ex.name} (d:{ex.difficulty}, eq: {', '.join(ex.equipment)})")
            lines.append(f"      {p.sets} x {p.reps} | {p.loading_method} | {p.intensity_note} | rest: {rest_str}")
        else:
            lines.append(f"    - {ex.name} (d:{ex.difficulty}, eq: {', '.join(ex.equipment)})")
    return "\n".join(lines)
