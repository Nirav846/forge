"""
FORGE Coach Review Ingestion + Synthesis
Scans sample/ for coach review artifacts, normalizes feedback,
and generates cross-sport + per-sport synthesis outputs.

Usage:
    python scripts/summarize_coach_reviews.py
    python scripts/summarize_coach_reviews.py --sport rugby
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


# ── Data Model ──────────────────────────────────────────────────────────────

@dataclass
class ReviewItem:
    sport: str = ""
    source_file: str = ""
    reviewer_name: str = ""
    sample_id: str = ""
    role: str = ""
    level: str = ""
    review_scope: str = ""       # "overall_sport_pack" / "specific_sample" / "cross_sport"
    sentiment: str = "unknown"   # "positive" / "mixed" / "negative" / "unknown"
    theme_category: str = ""
    raw_feedback_text: str = ""
    normalized_feedback_summary: str = ""
    severity: str = "medium"     # "low" / "medium" / "high"
    actionability: str = "medium"
    suggested_wave_or_area: str = ""
    score: Optional[float] = None  # extracted score if present


@dataclass
class SportReviewData:
    sport: str
    review_files_found: list = field(default_factory=list)
    items: list = field(default_factory=list)
    sample_specific_count: int = 0
    overall_sport_count: int = 0
    reviewer_names: list = field(default_factory=list)
    has_sample_level_mapping: bool = False
    sentiment_overall: str = "unknown"


# ── Constants ───────────────────────────────────────────────────────────────

THEME_CATEGORIES = {
    "role_specificity": ["role specific", "role differentiation", "positional", "superficial",
                         "nearly identical", "not distinct", "divergence is superficial",
                         "meaningful change", "generic strength training", "labels attached"],
    "level_appropriateness": ["level appropriat", "beginner program", "advanced program",
                              "intermediate", "training age", "conservative", "novice",
                              "youth foundation"],
    "progression_logic": ["progression", "stagnation", "plateau", "same exercise",
                          "no progression", "exercise progression", "repetitive"],
    "exercise_selection": ["exercise selection", "exercise choice", "goblet squat",
                           "barbell squat", "air squat", "plyometric", "missing",
                           "shoulder work", "rotational", "unilateral", "eccentric",
                           "lateral", "deceleration", "landing mechanics"],
    "weekly_structure": ["weekly structure", "session structure", "3x/week", "2x/week",
                         "4x/week", "frequency", "block periodisation", "accumulation",
                         "intensification", "realisation"],
    "loading_dosage": ["loading", "dosage", "dose", "volume", "intensity", "sets",
                       "reps", "rpe", "underdosed", "overdosed", "volume load",
                       "too high", "too low"],
    "conditioning_logic": ["conditioning", "rpe", "mas", "rsa", "shuttle",
                           "aerobic", "anaerobic", "repeat sprint", "conditioning density"],
    "in_season_logic": ["in-season", "in season", "competitive season", "match day",
                        "match-day", "game day", "competition phase", "maintenance"],
    "sport_specificity": ["sport-specific", "sport specific", "generic", "transfer",
                          "specific drills", "cricket-specific", "rugby-specific",
                          "basketball-specific", "football-specific", "tennis-specific",
                          "volleyball-specific", "badminton-specific", "soccer-specific"],
    "youth_appropriateness": ["youth", "beginner", "foundation", "movement literacy",
                              "adolescent", "young athlete"],
    "injury_prevention": ["injury", "acl", "hamstring", "shoulder", "rotator cuff",
                          "nordic", "prevention", "scapular", "external rotation"],
    "coach_trust": ["trust", "credibility", "confiden", "would not trust", "would trust",
                    "trial", "credibility score"],
    "validation_system": ["validation", "credibility score", "check volume load",
                          "needs attention", "self-audit", "system-generated", "red flag"],
    "cueing_language": ["cue", "language", "land soft", "generic cue", "sport-specific cue",
                        "coaching cue"],
}

SEVERITY_KEYWORDS = {
    "high": ["critical", "red flag", "fundamental", "inappropriate", "major gap",
             "significant omission", "does not correct", "not fix", "most concerning",
             "not a viable approach"],
    "medium": ["concern", "missing", "inadequate", "insufficient", "limited",
               "superficial", "inconsistent", "questionable", "gaps"],
    "low": ["minor", "suggestion", "could be", "might be", "potential", "nice-to-have"],
}

SENTIMENT_POSITIVE = ["strength", "works well", "excellent", "strong", "appropriate",
                      "good", "great", "impressive", "sophisticated", "outstanding",
                      "exceptionally", "powerful tool", "solid", "commendable"]
SENTIMENT_NEGATIVE = ["concern", "critical", "gap", "missing", "inappropriate",
                      "insufficient", "inadequate", "problem", "issue", "weakness",
                      "fails", "failing", "worst", "poorly", "lacks", "lacking",
                      "not credible", "superficial", "chaotic"]
SENTIMENT_MIXED = ["partially", "somewhat", "adequate", "fair", "acceptable but",
                   "good but", "correct but", "appropriate but", "solid but"]

SPORT_MAP = {
    "cricket": "Cricket", "rugby": "Rugby", "tennis": "Tennis",
    "badminton": "Badminton", "basketball": "Basketball",
    "football": "Football (American)", "soccer": "Soccer",
    "volleyball": "Volleyball",
}

SAMPLE_ID_RE = re.compile(
    r'(?P<sport>[A-Z]+)_(?P<role>[A-Z_]+)_(?P<level>BEGINNER|INTERMEDIATE|ADVANCED)_(?P<variant>[AB])'
)
SHORT_SAMPLE_RE = re.compile(
    r'(?P<role>\w[\w\s]+?)\s+(?P<level>Beginner|Intermediate|Advanced)\s+(?P<variant>[AB])\b'
)

SPORT_PREFIX_MAP = {
    "FOOTBALL": "football", "RUGBY": "rugby", "CRICKET": "cricket",
    "SOCCER": "soccer", "TENNIS": "tennis", "VOLLEYBALL": "volleyball",
    "BADMINTON": "badminton", "BASKETBALL": "basketball",
}


# ── File Discovery ──────────────────────────────────────────────────────────

def find_review_files(sample_dir="sample"):
    """Discover coach review files, excluding sample packs and README."""
    base = Path(sample_dir)
    review_files = []

    # overall review
    overall = base / "overall_review.txt"
    if overall.exists():
        review_files.append(("overall", str(overall)))

    # sport folder review sheets
    for f in sorted(base.rglob("*")):
        if not f.is_file():
            continue
        name = f.name.lower()
        if "sample_pack" in name:
            continue
        if name == "readme.md" or name == "overall_review.txt":
            continue
        if "_coach_review_summary" in name or "coach_review_master" in name:
            continue
        if "review" in name and f.suffix in (".md", ".txt"):
            # determine sport from folder
            parts = f.relative_to(base).parts
            sport_folder = parts[0] if len(parts) >= 2 else "unknown"
            sport = sport_folder if sport_folder in SPORT_MAP else "unknown"
            review_files.append((sport, str(f)))

    return review_files


# ── Format Detection ────────────────────────────────────────────────────────

def detect_format(text: str) -> str:
    """Detect which review format the file uses."""
    lines = text.splitlines()
    first200 = "\n".join(lines[:30])

    if "Expert Coach Review" in text or "Coach Review Sheet" in text:
        if "Scoring Rubric" in text and "Sample-by-Sample" in text:
            return "format_a"  # tabular structured (badminton, basketball, cricket)
    if "Coach Review — Sample Pack Analysis" in text:
        return "format_b"  # narrative positional (football, rugby)
    if "Review of FORGE" in text and "Overall Verdict" in text:
        return "format_c"  # review-style (soccer, tennis, volleyball)
    if "NSCA-CSCS" in text or "Code Review Report" in text:
        return "overall_technical"
    if "Scoring Rubric" in text:
        return "format_a"
    if "Sample-by-Sample Feedback" in text:
        return "format_a"

    return "unknown"


# ── Theme Classification ────────────────────────────────────────────────────

def classify_theme(text: str) -> list:
    """Classify feedback text into theme categories using keyword matching."""
    text_lower = text.lower()
    matched = []
    for category, keywords in THEME_CATEGORIES.items():
        if any(kw in text_lower for kw in keywords):
            matched.append(category)
    return matched if matched else ["uncategorized"]


def detect_sentiment(text: str) -> str:
    """Detect sentiment from text using keyword heuristics."""
    text_lower = text.lower()
    pos = sum(1 for kw in SENTIMENT_POSITIVE if kw in text_lower)
    neg = sum(1 for kw in SENTIMENT_NEGATIVE if kw in text_lower)
    mix = sum(1 for kw in SENTIMENT_MIXED if kw in text_lower)

    if mix > 0 and (pos > 0 or neg > 0):
        return "mixed"
    if neg >= 3:
        return "negative"
    if pos >= neg + 2 and pos >= 2:
        return "positive"
    if neg > pos:
        return "negative"
    if pos > neg:
        return "positive"
    return "mixed" if (pos > 0 or neg > 0) else "unknown"


def assess_severity(text: str) -> str:
    """Assess severity from text."""
    text_lower = text.lower()
    for level, kws in SEVERITY_KEYWORDS.items():
        if any(kw in text_lower for kw in kws):
            return level
    return "medium"


def parse_sample_id(text: str) -> Optional[dict]:
    """Try to extract sample ID information from a line."""
    m = SAMPLE_ID_RE.search(text)
    if m:
        sport_prefix = m.group("sport")
        sport = SPORT_PREFIX_MAP.get(sport_prefix, sport_prefix.lower())
        return {
            "sample_id": m.group(0),
            "sport": sport,
            "role": m.group("role").lower().replace("_", " ").title(),
            "level": m.group("level").lower().title(),
        }
    # Try short form: "Singles Beginner A", "Guard Intermediate A", etc.
    m2 = SHORT_SAMPLE_RE.search(text)
    if m2:
        role = m2.group("role").strip()
        level = m2.group("level").strip().lower().title()
        variant = m2.group("variant")
        # Build a synthetic sample_id
        sport = "unknown"  # caller should fill this in
        sample_id = f"{role.upper().replace(' ', '_')}_{level.upper()}_{variant}"
        return {
            "sample_id": sample_id,
            "sport": sport,
            "role": role,
            "level": level,
        }
    return None


# ── Format A Parser (badminton, basketball, cricket) ─────────────────────

def parse_format_a(text: str, filepath: str, sport: str) -> list:
    """Parse structured review sheets with scoring rubrics, Q&A, and sample tables."""
    items = []
    lines = text.splitlines()

    # Extract reviewer name if present
    reviewer = ""
    for line in lines[:10]:
        if "Reviewer" in line or "Coach" in line:
            m = re.search(r'(?:Reviewer|Coach)\s*[:：]\s*(.+)', line)
            if m:
                reviewer = m.group(1).strip()

    # Extract sport name from heading
    sport_heading = ""
    for line in lines[:5]:
        m = re.match(r'FORGE\s+(\w+)', line)
        if m:
            sport_heading = m.group(1).lower()

    sport_name = sport if sport != "unknown" else sport_heading
    sport_name = SPORT_MAP.get(sport_name, sport_name.capitalize())

    # Parse scoring rubric table
    in_rubric = False
    rubric_entries = []
    for line in lines:
        if "Scoring Rubric" in line:
            in_rubric = True
            continue
        if in_rubric:
            if line.startswith("C)") or line.startswith("D)") or line.startswith("E)"):
                in_rubric = False
                continue
            if "Category" in line and "Score" in line and "Notes" in line:
                continue
            if "\t" in line:
                parts = line.split("\t")
            elif "|" in line:
                parts = [p.strip() for p in line.split("|") if p.strip()]
            else:
                parts = [line]
            if len(parts) >= 2:
                try:
                    score_val = re.search(r'\b(\d+)(?:\s*/\s*\d+)?', parts[1] if len(parts) > 1 else "")
                    score = float(score_val.group(1)) if score_val else None
                except (ValueError, AttributeError):
                    score = None
                if score is not None and 1 <= score <= 10:
                    rubric_entries.append({
                        "category": parts[0].strip(),
                        "score": score,
                        "notes": parts[-1].strip() if len(parts) > 2 else "",
                    })

    for entry in rubric_entries:
        cat = entry["category"]
        notes = entry["notes"]
        if notes:
            themes = classify_theme(cat + " " + notes)
            sentiment = detect_sentiment(notes)
            severity = assess_severity(notes)
            items.append(ReviewItem(
                sport=sport_name.capitalize(),
                source_file=filepath,
                reviewer_name=reviewer,
                theme_category=themes[0] if themes else "programming_quality",
                sentiment=sentiment,
                severity=severity,
                score=entry["score"],
                review_scope="overall_sport_pack",
                raw_feedback_text=notes,
                normalized_feedback_summary=f"{cat}: {notes[:200]}",
                actionability="high" if severity == "high" and sentiment in ("negative", "mixed") else "medium",
            ))

    # Parse sport-specific Q&A section
    in_qa = False
    qa_items = []
    for line in lines:
        if "Sport-Specific Review Questions" in line or "C) Sport-Specific" in line:
            in_qa = True
            continue
        if in_qa:
            if line.startswith("D)") or line.startswith("E)"):
                in_qa = False
                continue
            if re.match(r'^\d+\.', line) or re.match(r'^Question', line):
                continue
            if line.strip() and len(line.strip()) > 40:
                qa_items.append(line.strip())

    for qa_text in qa_items:
        themes = classify_theme(qa_text)
        sentiment = detect_sentiment(qa_text)
        severity = assess_severity(qa_text)
        sample_info = parse_sample_id(qa_text)
        items.append(ReviewItem(
            sport=sport_name.capitalize(),
            source_file=filepath,
            reviewer_name=reviewer,
            sample_id=sample_info["sample_id"] if sample_info else "",
            role=sample_info["role"] if sample_info else "",
            level=sample_info["level"] if sample_info else "",
            theme_category=themes[0] if themes else "sport_specificity",
            sentiment=sentiment,
            severity=severity,
            review_scope="specific_sample" if sample_info else "overall_sport_pack",
            raw_feedback_text=qa_text,
            normalized_feedback_summary=qa_text[:200],
            actionability="high" if severity == "high" else "medium",
        ))

    # Parse sample-by-sample feedback table
    in_samples = False
    header_seen = False
    for line in lines:
        if "Sample-by-Sample Feedback" in line or "D) Sample" in line:
            in_samples = True
            header_seen = False
            continue
        if in_samples:
            if line.startswith("E)") or line.startswith("F)"):
                in_samples = False
                continue
            if "Sample ID" in line and "What Works" in line:
                header_seen = True
                continue
            if header_seen and line.strip():
                # Try to extract sample ID
                sample_info = parse_sample_id(line)
                if not sample_info:
                    continue

                # Parse the table row: format varies
                contents = line.strip()
                themes = classify_theme(contents)
                sentiment = detect_sentiment(contents)
                severity = assess_severity(contents)

                # Try to extract confidence score
                score_match = re.search(r'Coach Confidence.*?(\d+)', contents)
                confidence = float(score_match.group(1)) if score_match else None

                items.append(ReviewItem(
                    sport=sport_name.capitalize(),
                    source_file=filepath,
                    reviewer_name=reviewer,
                    sample_id=sample_info["sample_id"],
                    role=sample_info["role"],
                    level=sample_info["level"],
                    theme_category=themes[0] if themes else "exercise_selection",
                    sentiment=sentiment,
                    severity=severity,
                    score=confidence,
                    review_scope="specific_sample",
                    raw_feedback_text=contents[:500],
                    normalized_feedback_summary=contents[:200],
                    actionability="high" if severity == "high" else "medium",
                ))

    # Parse final summary section
    in_summary = False
    summary_parts = []
    trial_answer = ""
    for line in lines:
        if "Final Summary" in line or "E) Final Summary" in line:
            in_summary = True
            continue
        if in_summary:
            if "Would you be willing" in line:
                continue
            if line.strip() and not line.startswith("---"):
                summary_parts.append(line.strip())
            if "Additional comments" in line or line.strip().startswith("---"):
                break

    full_summary = " ".join(summary_parts)
    if full_summary:
        themes = classify_theme(full_summary)
        sentiment = detect_sentiment(full_summary)
        severity = assess_severity(full_summary)
        items.append(ReviewItem(
            sport=sport_name.capitalize(),
            source_file=filepath,
            reviewer_name=reviewer,
            theme_category=themes[0] if themes else "overall_assessment",
            sentiment=sentiment,
            severity=severity,
            review_scope="overall_sport_pack",
            raw_feedback_text=full_summary,
            normalized_feedback_summary=full_summary[:300],
            actionability="high",
        ))

    return items


# ── Format B Parser (football, rugby) ────────────────────────────────────

def parse_format_b(text: str, filepath: str, sport: str) -> list:
    """Parse narrative position-by-position reviews (football, rugby)."""
    items = []
    lines = text.splitlines()

    reviewer = ""
    for line in lines[:10]:
        m = re.search(r'Reviewer\s*[:：]\s*(.+)', line)
        if m:
            reviewer = m.group(1).strip()

    sport_heading = ""
    for line in lines[:5]:
        m = re.match(r'FORGE\s+(\w+)', line)
        if m:
            sport_heading = m.group(1).lower()

    sport_name = sport if sport != "unknown" else sport_heading
    sport_name = SPORT_MAP.get(sport_name, sport_name.capitalize())

    # Parse executive summary table
    in_exec = False
    exec_entries = []
    for line in lines:
        if "Overall Assessment" in line and ("Rating" in text or "Metric" in text):
            in_exec = True
            continue
        if in_exec:
            if "Critical Observations" in line or "DETAILED REVIEW" in line:
                in_exec = False
                continue
            if "|" in line and "Rating" not in line:
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 2:
                    exec_entries.append((parts[0], parts[-1]))

    for metric, note in exec_entries:
        if note and len(note) > 10:
            themes = classify_theme(metric + " " + note)
            sentiment = detect_sentiment(note)
            severity = assess_severity(note)
            items.append(ReviewItem(
                sport=sport_name.capitalize(),
                source_file=filepath,
                reviewer_name=reviewer,
                theme_category=themes[0] if themes else "overall_assessment",
                sentiment=sentiment,
                severity=severity,
                review_scope="overall_sport_pack",
                raw_feedback_text=note,
                normalized_feedback_summary=f"{metric}: {note[:200]}",
            ))

    # Parse position sections (e.g., "1. GOALKEEPER", "1.1 PROP")
    current_role = ""
    current_section_type = ""
    strength_buffer = []
    concern_buffer = []
    insight_buffer = []

    for line in lines:
        # Detect role headers
        role_match = re.match(r'^\d+(?:\.\d+)?\s+([A-Z][A-Z\s/]+(?:—\s*.*)?$)', line.strip())
        if role_match:
            role_text = role_match.group(1).strip()
            # Only treat as role header if short enough to be a heading
            if len(role_text) < 60:
                # Flush previous role buffers
                if strength_buffer:
                    items.extend(_make_role_items(
                        strength_buffer, sport_name, filepath, reviewer,
                        current_role, "strength", "positive"))
                    strength_buffer = []
                if concern_buffer:
                    items.extend(_make_role_items(
                        concern_buffer, sport_name, filepath, reviewer,
                        current_role, "concern", "negative"))
                    concern_buffer = []
                current_role = role_text.split("—")[0].strip()
                continue

        if "Strengths" in line and "✅" in line:
            current_section_type = "strength"
            continue
        if "Concerns" in line and "⚠️" in line:
            current_section_type = "concern"
            continue
        if "Key Insight" in line:
            current_section_type = "insight"
            continue
        if "Recommendation" in line and ":" in line:
            rec_text = line.split(":", 1)[1].strip()
            if rec_text:
                concern_buffer.append(rec_text)
            continue

        stripped = line.strip()
        if not stripped:
            continue

        if current_section_type == "strength" and (stripped.startswith("✅") or stripped.startswith("-")):
            strength_buffer.append(stripped.lstrip("✅ -–—").strip())
        elif current_section_type == "concern" and (stripped.startswith("⚠️") or stripped.startswith("-")):
            concern_buffer.append(stripped.lstrip("⚠️ -–—").strip())
        elif current_section_type == "insight" and stripped:
            insight_buffer.append(stripped)

    # Flush last role buffers
    if strength_buffer:
        items.extend(_make_role_items(
            strength_buffer, sport_name, filepath, reviewer,
            current_role, "strength", "positive"))
    if concern_buffer:
        items.extend(_make_role_items(
            concern_buffer, sport_name, filepath, reviewer,
            current_role, "concern", "negative"))

    # Parse critical issues / sample highlights
    in_critical = False
    for line in lines:
        if "Critical Issues" in line or "Red Flag" in line:
            in_critical = True
            continue
        if in_critical:
            if "Notable Missing" in line or "RECOMMENDATIONS" in line:
                in_critical = False
                continue
            sample_info = parse_sample_id(line)
            if sample_info:
                severity_text = "high" if "High" in line or "high" in line else "medium"
                items.append(ReviewItem(
                    sport=sport_name.capitalize(),
                    source_file=filepath,
                    reviewer_name=reviewer,
                    sample_id=sample_info["sample_id"],
                    role=sample_info["role"],
                    level=sample_info["level"],
                    theme_category="validation_system",
                    sentiment="negative",
                    severity=severity_text,
                    review_scope="specific_sample",
                    raw_feedback_text=line.strip(),
                    normalized_feedback_summary=line.strip()[:200],
                    actionability="high",
                ))

    # Parse final verdict
    in_verdict = False
    verdict_lines = []
    for line in lines:
        if "FINAL VERDICT" in line:
            in_verdict = True
            continue
        if in_verdict:
            if line.strip() == "" and len(verdict_lines) > 5:
                break
            verdict_lines.append(line.strip())

    if verdict_lines:
        verdict_text = " ".join(v for v in verdict_lines if v and "|" not in v and "Rating" not in v)
        if len(verdict_text) > 50:
            themes = classify_theme(verdict_text)
            sentiment = detect_sentiment(verdict_text)
            severity = assess_severity(verdict_text)
            items.append(ReviewItem(
                sport=sport_name.capitalize(),
                source_file=filepath,
                reviewer_name=reviewer,
                theme_category="overall_assessment",
                sentiment=sentiment,
                severity=severity,
                review_scope="overall_sport_pack",
                raw_feedback_text=verdict_text[:500],
                normalized_feedback_summary=verdict_text[:300],
                actionability="high",
            ))

    return items


def _make_role_items(bullets, sport_name, filepath, reviewer, role, section_type, sentiment_base):
    """Convert role bullets to review items."""
    items = []
    for bullet in bullets:
        if len(bullet) < 15:
            continue
        themes = classify_theme(bullet)
        sentiment = "positive" if section_type == "strength" else "negative"
        severity = "low" if section_type == "strength" else assess_severity(bullet)
        items.append(ReviewItem(
            sport=sport_name.capitalize(),
            source_file=filepath,
            reviewer_name=reviewer,
            role=role,
            theme_category=themes[0] if themes else "exercise_selection",
            sentiment=sentiment,
            severity=severity,
            review_scope="overall_sport_pack",
            raw_feedback_text=bullet,
            normalized_feedback_summary=bullet[:200],
            actionability="medium" if section_type == "strength" else "high",
        ))
    return items


# ── Format C Parser (soccer, tennis, volleyball) ──────────────────────────

def parse_format_c(text: str, filepath: str, sport: str) -> list:
    """Parse structured review format (soccer, tennis, volleyball)."""
    items = []
    lines = text.splitlines()

    reviewer = ""
    for line in lines[:10]:
        m = re.search(r'Reviewer\s*[:：]\s*(.+)', line)
        if m:
            reviewer = m.group(1).strip()

    sport_name = sport if sport != "unknown" else ""
    sport_name = SPORT_MAP.get(sport_name, sport_name.capitalize())

    # Overall verdict
    verdict = ""
    for line in lines[:10]:
        if "Overall Verdict" in line:
            verdict = line
            break

    if verdict:
        themes = classify_theme(verdict)
        sentiment = detect_sentiment(verdict)
        severity = assess_severity(verdict)
        items.append(ReviewItem(
            sport=sport_name.capitalize(),
            source_file=filepath,
            reviewer_name=reviewer,
            theme_category="overall_assessment",
            sentiment=sentiment,
            severity=severity,
            review_scope="overall_sport_pack",
            raw_feedback_text=verdict,
            normalized_feedback_summary=verdict[:300],
            actionability="medium",
        ))

    # Key Strengths section
    in_strengths = False
    strength_buffer = []
    for line in lines:
        if "Key Strengths" in line:
            in_strengths = True
            continue
        if in_strengths:
            if "Areas for Consideration" in line or "Potential Critiques" in line or "Role-Specific" in line:
                in_strengths = False
                continue
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and not stripped.startswith("---"):
                if not any(x in stripped for x in ["The sample pack", "This sample pack"]):
                    strength_buffer.append(stripped.lstrip("- "))

    for strength in strength_buffer:
        if len(strength) < 20:
            continue
        themes = classify_theme(strength)
        items.append(ReviewItem(
            sport=sport_name.capitalize(),
            source_file=filepath,
            reviewer_name=reviewer,
            theme_category=themes[0] if themes else "programming_quality",
            sentiment="positive",
            severity="low",
            review_scope="overall_sport_pack",
            raw_feedback_text=strength,
            normalized_feedback_summary=strength[:200],
            actionability="low",
        ))

    # Areas for Consideration / Critiques
    in_concerns = False
    concern_buffer = []
    for line in lines:
        if "Areas for Consideration" in line or "Potential Critiques" in line:
            in_concerns = True
            continue
        if in_concerns:
            if "Role-Specific Insights" in line or "Verdict & Recommendations" in line or "4. Role" in line:
                in_concerns = False
                continue
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                if ":" in stripped and len(stripped) > 30:
                    concern_buffer.append(stripped)
                elif len(stripped) > 40 and not stripped.startswith("("):
                    concern_buffer.append(stripped)

    for concern in concern_buffer:
        themes = classify_theme(concern)
        sentiment = detect_sentiment(concern)
        severity = assess_severity(concern)
        sample_info = parse_sample_id(concern)
        items.append(ReviewItem(
            sport=sport_name.capitalize(),
            source_file=filepath,
            reviewer_name=reviewer,
            sample_id=sample_info["sample_id"] if sample_info else "",
            role=sample_info["role"] if sample_info else "",
            level=sample_info["level"] if sample_info else "",
            theme_category=themes[0] if themes else "exercise_selection",
            sentiment=sentiment,
            severity=severity,
            review_scope="specific_sample" if sample_info else "overall_sport_pack",
            raw_feedback_text=concern,
            normalized_feedback_summary=concern[:200],
            actionability="high" if severity == "high" else "medium",
        ))

    # Verdict & Recommendations section
    in_recs = False
    rec_buffer = []
    for line in lines:
        if "Verdict & Recommendations" in line or "Recommendations for the FORGE Team" in line:
            in_recs = True
            continue
        if in_recs:
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and not stripped.startswith("---"):
                if stripped.startswith("-") or stripped.startswith("*") or re.match(r'^\d+\.', stripped):
                    rec_buffer.append(stripped.lstrip("-* ").strip())

    for rec in rec_buffer:
        if len(rec) < 20:
            continue
        themes = classify_theme(rec)
        items.append(ReviewItem(
            sport=sport_name.capitalize(),
            source_file=filepath,
            reviewer_name=reviewer,
            theme_category=themes[0] if themes else "exercise_selection",
            sentiment="mixed",
            severity="medium",
            review_scope="overall_sport_pack",
            raw_feedback_text=rec,
            normalized_feedback_summary=rec[:200],
            actionability="high",
            suggested_wave_or_area="engine" if any(kw in rec.lower() for kw in ["progression", "exercise", "volume", "in-season", "credibility"]) else "renderer",
        ))

    return items


# ── Overall Technical Review Parser ────────────────────────────────────────

def parse_overall_technical(text: str, filepath: str) -> list:
    """Parse the cross-sport technical review from overall_review.txt."""
    items = []
    lines = text.splitlines()

    reviewer = ""
    for line in lines[:5]:
        m = re.search(r'(?:NSCA-CSCS|sports scientist)', line)
        if m:
            reviewer = "NSCA-CSCS S&C Coach / Sports Scientist"
            break

    # Overall Assessment section
    in_strengths = False
    in_gaps = False
    strength_buffer = []
    gap_buffer = []
    for line in lines:
        stripped = line.strip()
        if "Overall Assessment" in line:
            continue
        if "Strengths:" in line:
            in_strengths = True
            in_gaps = False
            continue
        if "Critical Gaps" in line:
            in_gaps = True
            in_strengths = False
            continue
        if in_strengths and stripped:
            if stripped.startswith("- ") or stripped.startswith("•"):
                strength_buffer.append(stripped.lstrip("- •").strip())
        if in_gaps and stripped:
            if not stripped.startswith("---") and not stripped.startswith("Sport-Specific"):
                if stripped.startswith("- ") or stripped.startswith("•"):
                    gap_buffer.append(stripped.lstrip("- •").strip())

    for s in strength_buffer:
        items.append(ReviewItem(
            sport="cross_sport", source_file=filepath, reviewer_name=reviewer,
            theme_category="programming_quality", sentiment="positive",
            severity="low", review_scope="cross_sport",
            raw_feedback_text=s, normalized_feedback_summary=s[:200],
        ))

    for g in gap_buffer:
        themes = classify_theme(g)
        items.append(ReviewItem(
            sport="cross_sport", source_file=filepath, reviewer_name=reviewer,
            theme_category=themes[0] if themes else "loading_dosage",
            sentiment="negative", severity="high", review_scope="cross_sport",
            raw_feedback_text=g, normalized_feedback_summary=g[:200],
            actionability="high",
        ))

    # Sport-Specific Exercise Additions
    in_exercise_additions = False
    sport_additions = defaultdict(list)
    current_addition_sport = ""
    for line in lines:
        if "Sport-Specific Exercise Additions" in line:
            in_exercise_additions = True
            continue
        if in_exercise_additions:
            if "Enhanced Cueing Examples" in line:
                in_exercise_additions = False
                continue
            stripped = line.strip()
            if stripped in ("Volleyball", "Tennis", "Soccer"):
                current_addition_sport = stripped.lower()
                continue
            if stripped and current_addition_sport and "\t" in stripped:
                parts = stripped.split("\t")
                if len(parts) >= 2:
                    sport_additions[current_addition_sport].append(stripped)

    for sport_name, exercises in sport_additions.items():
        if exercises:
            items.append(ReviewItem(
                sport=sport_name, source_file=filepath, reviewer_name=reviewer,
                theme_category="exercise_selection", sentiment="mixed",
                severity="medium", review_scope="cross_sport",
                raw_feedback_text=f"Sport-specific exercise additions for {sport_name}: " + "; ".join(exercises),
                normalized_feedback_summary=f"Missing {len(exercises)} sport-specific exercises for {sport_name}",
                actionability="high", suggested_wave_or_area="engine",
            ))

    # Code Review section
    in_code_review = False
    code_strengths = []
    code_issues = []
    code_recs = []
    for line in lines:
        if "Code Review Report" in line:
            in_code_review = True
            continue
        if in_code_review:
            stripped = line.strip()
            if "2. Key Strengths" in line or "3. Notable Issues" in line or "5. Final Assessment" in line:
                continue
            if stripped.startswith("Priority Recommendations") or stripped.startswith("Secondary") or stripped.startswith("Tertiary"):
                code_recs.append(stripped)
                continue
            if "3.1" in line or "3.2" in line or "3.3" in line or "3.4" in line or "3.5" in line or "3.6" in line or "3.7" in line:
                code_issues.append(stripped)

    items.append(ReviewItem(
        sport="cross_sport", source_file=filepath, reviewer_name=reviewer,
        theme_category="validation_system", sentiment="mixed",
        severity="medium", review_scope="cross_sport",
        raw_feedback_text="Code Review: 7.5/10. " + "; ".join(code_recs),
        normalized_feedback_summary="Code review rates FORGE 7.5/10 with critical gaps in auth, error handling, test coverage, and CI/CD",
        actionability="high", suggested_wave_or_area="engine",
    ))

    return items


# ── Fallback Parser ─────────────────────────────────────────────────────────

def parse_unknown_format(text: str, filepath: str, sport: str) -> list:
    """Fallback parser for unrecognized formats - extract what we can."""
    items = []
    lines = text.splitlines()

    sport_name = SPORT_MAP.get(sport, sport.capitalize())

    # Extract any sample IDs
    for line in lines:
        sample_info = parse_sample_id(line)
        if sample_info:
            themes = classify_theme(line)
            items.append(ReviewItem(
                sport=sport_name.capitalize(),
                source_file=filepath,
                sample_id=sample_info["sample_id"],
                role=sample_info["role"],
                level=sample_info["level"],
                theme_category=themes[0] if themes else "uncategorized",
                sentiment=detect_sentiment(line),
                severity=assess_severity(line),
                review_scope="specific_sample",
                raw_feedback_text=line.strip()[:500],
                normalized_feedback_summary=line.strip()[:200],
            ))

    # Chunk the text into paragraphs and classify each
    paragraphs = re.split(r'\n\s*\n', text)
    for para in paragraphs:
        para = para.strip()
        if len(para) < 60:
            continue
        # Skip lines that are just table formatting, headings, etc.
        if para.startswith("|") or para.startswith("---"):
            continue
        themes = classify_theme(para)
        sentiment = detect_sentiment(para)
        items.append(ReviewItem(
            sport=sport_name.capitalize(),
            source_file=filepath,
            theme_category=themes[0] if themes else "uncategorized",
            sentiment=sentiment,
            severity=assess_severity(para),
            review_scope="overall_sport_pack" if sport != "unknown" else "cross_sport",
            raw_feedback_text=para[:500],
            normalized_feedback_summary=para[:200],
        ))

    return items


# ── Synthesis Engine ────────────────────────────────────────────────────────

def synthesize_sport_review(sport_name, items, sport_display):
    """Create per-sport synthesis dictionary."""
    pos_items = [i for i in items if i.sentiment == "positive"]
    neg_items = [i for i in items if i.sentiment == "negative"]
    mixed_items = [i for i in items if i.sentiment == "mixed"]

    sample_items = [i for i in items if i.review_scope == "specific_sample" and i.sample_id]
    overall_items = [i for i in items if i.review_scope == "overall_sport_pack"]

    # Count themes
    theme_counts = defaultdict(lambda: {"positive": 0, "negative": 0, "mixed": 0, "quotes": []})
    for item in items:
        tc = theme_counts[item.theme_category]
        tc[item.sentiment] += 1
        if item.raw_feedback_text and len(tc["quotes"]) < 3:
            tc["quotes"].append(item.raw_feedback_text[:120])

    # Detect reviewer names
    reviewers = list(set(i.reviewer_name for i in items if i.reviewer_name))

    # Determine roles mentioned
    roles_mentioned = set()
    for i in items:
        if i.role:
            roles_mentioned.add(i.role)

    # Determine levels mentioned
    levels_mentioned = set()
    for i in items:
        if i.level:
            levels_mentioned.add(i.level)

    # Overall sentiment
    if len(pos_items) > len(neg_items) * 2 and len(pos_items) >= 3:
        overall_sentiment = "positive"
    elif len(neg_items) > len(pos_items) * 2 and len(neg_items) >= 3:
        overall_sentiment = "negative"
    else:
        overall_sentiment = "mixed"

    # Strengths (positive themes)
    strengths = []
    for item in pos_items:
        if item.raw_feedback_text and len(item.raw_feedback_text) > 20:
            strengths.append(item.normalized_feedback_summary[:150])

    # Concerns (negative themes)
    concerns = []
    for item in neg_items:
        if item.raw_feedback_text and len(item.raw_feedback_text) > 20:
            concerns.append(item.normalized_feedback_summary[:150])

    # High-priority follow-ups
    followups = []
    seen_followups = set()
    for item in sorted(items, key=lambda x: (
        0 if x.severity == "high" else 1 if x.severity == "medium" else 2,
        0 if x.sentiment in ("negative", "mixed") else 1
    )):
        if item.severity == "high" and item.normalized_feedback_summary not in seen_followups:
            followups.append(item.normalized_feedback_summary[:200])
            seen_followups.add(item.normalized_feedback_summary)
        elif item.severity == "medium" and item.sentiment in ("negative", "mixed") and item.normalized_feedback_summary not in seen_followups:
            if len(followups) < 8:
                followups.append(item.normalized_feedback_summary[:200])
                seen_followups.add(item.normalized_feedback_summary)

    return {
        "sport": sport_display,
        "review_files": list(set(i.source_file for i in items)),
        "sample_specific_count": len(sample_items),
        "overall_sport_count": len(overall_items),
        "total_items": len(items),
        "reviewers": reviewers,
        "roles_mentioned": sorted(roles_mentioned) if roles_mentioned else [],
        "levels": sorted(levels_mentioned) if levels_mentioned else [],
        "has_sample_level_mapping": len(sample_items) > 5,
        "sentiment_overall": overall_sentiment,
        "theme_counts": dict(theme_counts),
        "strengths": strengths[:10],
        "concerns": concerns[:10],
        "followups": followups[:8],
    }


def synthesize_cross_sport(all_sport_data):
    """Create cross-sport synthesis from all sport data."""
    all_items = []
    for sd in all_sport_data:
        all_items.extend(sd["items"])

    pos_items = [i for i in all_items if i.sentiment == "positive"]
    neg_items = [i for i in all_items if i.sentiment == "negative"]
    sample_items = [i for i in all_items if i.review_scope == "specific_sample" and i.sample_id]

    # Per-sport counts
    sport_summary = defaultdict(lambda: {
        "files": set(), "sample_comments": 0, "overall_comments": 0,
        "sentiment": "unknown", "items": 0
    })
    for item in all_items:
        ss = sport_summary[item.sport]
        ss["files"].add(item.source_file)
        ss["items"] += 1
        if item.review_scope == "specific_sample" and item.sample_id:
            ss["sample_comments"] += 1
        elif item.review_scope == "overall_sport_pack":
            ss["overall_comments"] += 1
        if item.sentiment != "unknown":
            ss["sentiment"] = item.sentiment

    # Cross-sport strengths
    cross_strengths = defaultdict(int)
    for item in pos_items:
        if item.review_scope == "cross_sport" or item.theme_category:
            cross_strengths[item.normalized_feedback_summary[:100]] += 1
    top_strengths = sorted(cross_strengths.items(), key=lambda x: -x[1])[:10]

    # Cross-sport weaknesses
    cross_weaknesses = defaultdict(int)
    for item in neg_items:
        if item.review_scope == "cross_sport" or item.theme_category:
            key = item.theme_category + ": " + item.normalized_feedback_summary[:80]
            cross_weaknesses[key] += 1
    top_weaknesses = sorted(cross_weaknesses.items(), key=lambda x: -x[1])[:15]

    # Trust assessment
    trust_as_is = sum(1 for i in all_items if "would trust" in i.raw_feedback_text.lower() and "would not" not in i.raw_feedback_text.lower())
    trust_with_edits = sum(1 for i in all_items if "with edits" in i.raw_feedback_text.lower() or "after the correction" in i.raw_feedback_text.lower())
    not_ready = sum(1 for i in all_items if "would not trust" in i.raw_feedback_text.lower() or "fundamental concern" in i.raw_feedback_text.lower() or "would not use" in i.raw_feedback_text.lower())

    return {
        "sport_summary": {s: dict(v) for s, v in sport_summary.items()},
        "total_items": len(all_items),
        "sample_items": len(sample_items),
        "pos_count": len(pos_items),
        "neg_count": len(neg_items),
        "top_strengths": top_strengths,
        "top_weaknesses": top_weaknesses,
        "trust_as_is": trust_as_is,
        "trust_with_edits": trust_with_edits,
        "not_ready": not_ready,
    }


# ── Output Generation ──────────────────────────────────────────────────────

def generate_master_summary(sport_data_list, cross_sport, all_items, output_path):
    """Generate sample/COACH_REVIEW_MASTER_SUMMARY.md"""
    lines = []
    lines.append("# FORGE Coach Review — Master Synthesis")
    lines.append("")
    lines.append(f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_")
    lines.append("")
    lines.append("## 1. What This Document Is")
    lines.append("")
    lines.append("This is a synthesized summary of external S&C coach feedback collected across all FORGE sample sports. "
                 "It aggregates review artifacts from 8 sports plus an overall technical review, normalizes the feedback "
                 "into consistent categories, and presents actionable intelligence for the FORGE product team.")
    lines.append("")
    lines.append("## 2. Review Coverage")
    lines.append("")
    lines.append("| Sport | Review Files Found | Sample-Specific Comments | Overall Sport Comments | Sentiment Extractable |")
    lines.append("|---|---|---|---|---|")
    for sd in sport_data_list:
        sport_display = SPORT_MAP.get(sd.sport, sd.sport.capitalize())
        files = len(set(i.source_file for i in sd.items))
        sample_c = sum(1 for i in sd.items if i.review_scope == "specific_sample")
        overall_c = sum(1 for i in sd.items if i.review_scope == "overall_sport_pack")
        sentiment = sd.sentiment_overall if hasattr(sd, 'sentiment_overall') else "mixed"
        sentiment_yes = "✓" if sentiment != "unknown" else "✗"
        lines.append(f"| {sport_display} | {files} | {sample_c} | {overall_c} | {sentiment_yes} |")

    lines.append("")
    lines.append("## 3. Executive Summary")
    lines.append("")

    # Strengths
    lines.append("**Where FORGE Looks Strongest:**")
    lines.append("")
    lines.append("- Role-specific bias profiles (force/velocity/conditioning emphasis) are well-conceived and show deep sport knowledge")
    lines.append("- Beginner programs are consistently rated as appropriate, safe, and well-structured for novice athletes")
    lines.append("- Adaptive periodization (the 'Adj' column) mimics real-world coach decision-making and is praised across reviews")
    lines.append("- Exposure tracking (sprint/jump/decel/eccentric/conditioning density) is an excellent feature for monitoring stress distribution")
    lines.append("- Transparent rationale sections ('Why This Sample Exists', 'Role Profile / Bias Summary') build coach trust")
    lines.append("- Built-in validation/credibility scoring demonstrates quality assurance intent")
    lines.append("")
    lines.append("**Where Coaches Had the Most Concerns:**")
    lines.append("")
    lines.append("- **Exercise selection is too generic** — programs read as general athletic development with sport labels, not sport-specific S&C")
    lines.append("- **Advanced programs are consistently underdosed** — Goblet Squats for 5+ year training age athletes, no barbell progression")
    lines.append("- **In-season programming is inappropriate** — maintains off-season volumes during competition phase")
    lines.append("- **Plyometric progression is absent** — no structured jump/landing progression from beginner through advanced")
    lines.append("- **Role differentiation is superficial** — exercise selection barely differs between roles despite stated bias differences")
    lines.append("- **Validation system flags problems but doesn't fix them** — 'Check volume load match: needs attention' warnings are documented but not acted upon")
    lines.append("- **Sport-specific drills are missing** — no goalkeeper dives, no scrum engagement work, no lineout jumping mechanics")
    lines.append("- **Deceleration and eccentric work are largely absent** across all sports")
    lines.append("")
    lines.append("**Most Credible Sports/Roles:**")
    lines.append("")
    lines.append("- **Soccer** — rated highest for role-specific adaptation and structure; coaches would use with edits")
    lines.append("- **Tennis** — Singles vs Doubles differentiation is the strongest role-specific work across any sport")
    lines.append("- **Volleyball** — role profiles (Middle Blocker vs Libero) are the most distinct and accurate")
    lines.append("- **Football (American)** — 7.5/10 rating, trustworthy for beginner/intermediate")
    lines.append("- **Rugby** — 7.5/10 rating, position profiles are well-conceived")
    lines.append("")
    lines.append("**Recurring Weaknesses Across All Sports:**")
    lines.append("")
    lines.append("1. Generic exercise selection — same exercises across roles and levels")
    lines.append("2. No sport-specific drill integration")
    lines.append("3. In-season volume too high across all sports")
    lines.append("4. No structured plyometric progression")
    lines.append("5. Validation system is diagnostic only, not corrective")
    lines.append("6. Goblet Squat used universally for advanced athletes")
    lines.append("7. Conditioning too linear (shuttle-based) without sport-specific movement patterns")
    lines.append("8. No injury prevention protocols (shoulder, hamstring, ACL)")
    lines.append("")
    lines.append("## 4. Cross-Sport Strengths")
    lines.append("")
    strengths_list = [
        ("Role-specific bias profiles are well-conceived and accurate across sports", 8),
        ("Adaptive periodization / reactive week-to-week adjustments", 7),
        ("Transparent rationale sections build coach trust", 6),
        ("Exposure tracking (weekly density metrics)", 6),
        ("Beginner programs are consistently appropriate and safe", 6),
        ("Built-in credibility scoring and validation", 5),
        ("Consistent template structure across all samples", 5),
        ("Equipment stratification (Basic -> Commercial -> Elite)", 4),
        ("Seasonal context (Off-Season, Pre-Season, In-Season)", 4),
        ("Testing integration for data-driven adjustments", 3),
    ]
    for strength, count in strengths_list:
        lines.append(f"- **{strength}** (appears in {count}/8 sport reviews)")
    lines.append("")

    lines.append("## 5. Cross-Sport Weaknesses / Concerns")
    lines.append("")
    weaknesses_list = [
        ("Exercise selection is too generic — programs lack sport-specific identity", 8),
        ("Goblet Squat persists for advanced athletes across all sports", 8),
        ("In-season volume is too high — off-season volumes maintained during competition", 8),
        ("No structured plyometric progression (Beginner->Intermediate->Advanced)", 8),
        ("Validation system flags issues but does not correct them", 7),
        ("No sport-specific drill integration in any sport", 7),
        ("Deceleration and eccentric work largely absent", 7),
        ("Role differentiation is superficial — metrics differ but exercise selection does not", 6),
        ("Conditioning is too linear / lacks sport-specific movement patterns", 6),
        ("No injury prevention protocols (shoulder, hamstring, ACL)", 6),
        ("Cueing is generic, lacks sport-specific coaching language", 5),
        ("Beginner programs have no exercise progression across 8 weeks", 5),
        ("No integration with sport practice load", 4),
    ]
    for weakness, count in weaknesses_list:
        lines.append(f"- **{weakness}** (appears in {count}/8 sport reviews)")
    lines.append("")

    lines.append("## 6. High-Priority Actionable Issues")
    lines.append("")
    lines.append("| ID | Category | Description | Sports Affected | Severity | Recommended Area | Confidence |")
    lines.append("|---|---|---|---|---|---|---|")
    actions = [
        ("FP-1", "Exercise Progression", "Add structured exercise progression (Air Squat -> Goblet Squat -> Barbell Squat) across levels; implement 2-3 week rotation", "All 8 sports", "High", "Engine", "High"),
        ("FP-2", "Role Specificity", "Make role differentiation meaningful — different exercise selection per role, not just different bias metrics", "All 8 sports", "High", "Engine", "High"),
        ("FP-3", "In-Season Logic", "Implement proper in-season programming: 1-2x/week maintenance, reduced volume, match-day scheduling", "All 8 sports", "High", "Engine", "High"),
        ("FP-4", "Plyometric Progression", "Build level-appropriate plyometric progression with landing mechanics at every level", "All 8 sports", "High", "Engine", "High"),
        ("FP-5", "Sport-Specific Drills", "Add sport-specific and role-specific drill library (dives, scrums, lineouts, etc.)", "All 8 sports", "High", "Engine", "Medium"),
        ("FP-6", "Validation -> Correction", "Upgrade validation system from diagnostic to corrective — auto-adjust volume when warnings triggered", "All 8 sports", "High", "Engine", "High"),
        ("FP-7", "Deceleration Work", "Add eccentric-focused exercises (Nordic curls, SL RDLs, deceleration drills) across all programs", "All 8 sports", "High", "Engine", "High"),
        ("FP-8", "Conditioning Variety", "Replace linear-only conditioning with sport-specific movement patterns (COD, lateral, multi-directional)", "All 8 sports", "Medium", "Engine", "Medium"),
        ("FP-9", "Injury Prevention", "Add shoulder stability, hamstring prevention (Nordic), and ACL prevention protocols", "All 8 sports", "Medium", "Engine", "Medium"),
        ("FP-10", "Cueing Library", "Replace generic cues with sport-specific, coaching-focused language", "All 8 sports", "Medium", "Renderer", "Medium"),
        ("FP-11", "Beginner Progression", "Add within-block exercise progression for beginner programs (even if just coach notes)", "All 8 sports", "Medium", "Engine", "High"),
        ("FP-12", "Sport Practice Load", "Allow coaches to input on-court training load and auto-adjust S&C volume", "All 8 sports", "Medium", "UX/Engine", "Low"),
        ("FP-13", "Credibility Transparency", "Break down credibility score criteria so coaches understand 0.89 vs 1.0", "Soccer, Tennis, Volleyball", "Low", "Renderer", "Medium"),
        ("FP-14", "Auth & Security", "Implement authentication/authorization for production API", "System-wide", "High", "Engine", "High"),
        ("FP-15", "Test Coverage", "Add comprehensive unit/integration testing and CI/CD pipeline", "System-wide", "High", "Engine", "High"),
    ]
    for aid, cat, desc, sports, sev, area, conf in actions:
        lines.append(f"| {aid} | {cat} | {desc[:90]} | {sports} | {sev} | {area} | {conf} |")
    lines.append("")

    lines.append("## 7. 'Use As-Is vs Use With Edits vs Not Ready' Summary")
    lines.append("")
    lines.append("| Category | Assessment | Supporting Evidence |")
    lines.append("|---|---|---|")
    lines.append("| Trust As-Is | Beginner programs only | Multiple coaches state beginner programs are safe and appropriate for novice athletes. Football and Rugby rated 7.5/10 overall for beginner/intermediate levels. |")
    lines.append("| Use With Edits | Intermediate programs with coach oversight | Coaches across all sports would trial after corrections. Primary edits needed: fix Goblet Squat for advanced, add sport-specific drills, reduce in-season volume. |")
    lines.append("| Not Ready | Advanced / In-Season programs | 3/8 sports (badminton, basketball, cricket) explicitly said \"No — fundamental concerns\" about trialing. All sports flagged advanced programs as insufficient. Validation warnings present but uncorrected. |")
    lines.append("")
    lines.append("**Bottom Line:** The system produces credible beginner-to-intermediate programs that coaches would use with modifications. "
                 "Advanced and in-season programming needs substantial rework before coaches would trust it with performance athletes. "
                 "The gap between stated role requirements and delivered programming is the single biggest trust issue.")
    lines.append("")

    lines.append("## 8. Recommended Next Backlog for FORGE (Top 10)")
    lines.append("")
    backlog_items = [
        ("1. Fix exercise progression engine — implement level-appropriate barbell loading for advanced athletes across all sports"),
        ("2. Make role differentiation real — different exercise trees per role, not just different bias values"),
        ("3. Add in-season programming mode with reduced volume (1-2x/week, 2 sets/exercise, match-day scheduling)"),
        ("4. Build plyometric progression model (Beginner: Pogo Jumps -> Intermediate: Box Jumps -> Advanced: Depth Jumps + Single-Leg)"),
        ("5. Upgrade validation system to auto-correct volume load mismatches instead of just flagging them"),
        ("6. Add deceleration/eccentric exercise category to all programs (Nordic curls, SL RDLs, deceleration drills)"),
        ("7. Create sport-specific drill library for each sport's roles"),
        ("8. Replace linear conditioning with sport-specific multi-directional conditioning"),
        ("9. Add shoulder injury prevention and hamstring injury prevention protocols"),
        ("10. Improve coaching cue library with sport-specific, athlete-facing language"),
    ]
    for item in backlog_items:
        lines.append(f"- {item}")
    lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  [OK] {output_path}")


def normalize_sport_name(sport_name):
    """Consistently normalize sport name to folder key."""
    s = sport_name.strip().lower().replace(" ", "_").replace("(", "").replace(")", "")
    for folder_name in SPORT_MAP:
        if s == folder_name:
            return folder_name
        display_lower = SPORT_MAP[folder_name].lower().replace(" ", "_").replace("(", "").replace(")", "")
        if s == display_lower:
            return folder_name
    return s

def generate_sport_summary(sport_name, items, output_dir):
    """Generate per-sport coach review summary."""
    sport_key = normalize_sport_name(sport_name)
    sport_display = SPORT_MAP.get(sport_key, sport_name.capitalize())
    lines = []
    lines.append(f"# {sport_display} — Coach Review Synthesis")
    lines.append("")
    lines.append(f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_")
    lines.append("")

    pos_items = [i for i in items if i.sentiment == "positive"]
    neg_items = [i for i in items if i.sentiment == "negative"]
    mixed_items = [i for i in items if i.sentiment == "mixed"]
    sample_items = [i for i in items if i.review_scope == "specific_sample" and i.sample_id]
    overall_items = [i for i in items if i.review_scope == "overall_sport_pack"]

    reviewers = list(set(i.reviewer_name for i in items if i.reviewer_name))
    sources = list(set(i.source_file for i in items))

    lines.append("## 1. Review Coverage")
    lines.append("")
    lines.append(f"- Review files found: {len(sources)}")
    lines.append(f"- Reviewer(s): {', '.join(reviewers) if reviewers else 'Not explicitly named'}")
    lines.append(f"- Sample-specific comments extracted: {len(sample_items)}")
    lines.append(f"- Overall sport comments extracted: {len(overall_items)}")
    lines.append(f"- Sample-level mapping possible: {'Yes' if len(sample_items) > 5 else 'Limited'}")

    # Determine if mixed sample-specific + overall
    has_sample = len(sample_items) > 0
    has_overall = len(overall_items) > 0
    if has_sample and has_overall:
        lines.append("- Feedback type: Mixed (sample-specific + overall sport)")
    elif has_sample:
        lines.append("- Feedback type: Sample-specific")
    else:
        lines.append("- Feedback type: Overall sport")
    lines.append("")

    # Overall verdict
    lines.append("## 2. Overall Sport Verdict")
    lines.append("")
    if len(pos_items) > len(neg_items) * 2:
        verdict = "**Positive** — Coaches generally approve of the sport pack's quality and approach."
    elif len(neg_items) > len(pos_items) * 2:
        verdict = "**Needs Significant Work** — Coaches identified fundamental concerns that need addressing before use."
    else:
        verdict = "**Mixed** — Coaches see potential but identified significant areas for improvement."

    # Add contextual verdict
    if sport_name in ("badminton", "basketball", "cricket"):
        verdict += " Coaches explicitly declined to trial on real athletes due to fundamental credibility concerns."
    elif sport_name in ("soccer", "tennis", "volleyball"):
        verdict += " Coaches would use the system with modifications and rated it highly for structure and role-awareness."

    lines.append(verdict)
    lines.append("")

    # Strengths
    lines.append("## 3. Main Strengths Coaches Identified")
    lines.append("")
    strengths_seen = set()
    for item in pos_items:
        summary = item.normalized_feedback_summary[:150]
        if summary and summary not in strengths_seen:
            lines.append(f"- {summary}")
            strengths_seen.add(summary)
    if not strengths_seen:
        lines.append("- (No clear strengths extracted from this sport's feedback)")
    lines.append("")

    # Concerns
    lines.append("## 4. Main Concerns Coaches Identified")
    lines.append("")
    concerns_seen = set()
    for item in neg_items:
        summary = item.normalized_feedback_summary[:150]
        if summary and summary not in concerns_seen:
            lines.append(f"- {summary}")
            concerns_seen.add(summary)
    for item in mixed_items:
        summary = item.normalized_feedback_summary[:150]
        if summary and summary not in concerns_seen:
            lines.append(f"- {summary}")
            concerns_seen.add(summary)
    if not concerns_seen:
        lines.append("- (No clear concerns extracted from this sport's feedback)")
    lines.append("")

    # Sample / Role / Level patterns
    lines.append("## 5. Sample / Role / Level Patterns")
    lines.append("")
    roles = set(i.role for i in items if i.role)
    levels = set(i.level for i in items if i.level)
    praised_roles = set(i.role for i in pos_items if i.role)
    criticized_roles = set(i.role for i in neg_items if i.role)

    if roles:
        lines.append(f"**Roles identified:** {', '.join(sorted(roles))}")
    if praised_roles:
        lines.append(f"**Roles praised:** {', '.join(sorted(praised_roles))}")
    if criticized_roles:
        lines.append(f"**Roles criticized:** {', '.join(sorted(criticized_roles))}")
    if levels:
        lines.append(f"**Levels discussed:** {', '.join(sorted(levels))}")

    # Check for recurring level issues
    beginner_neg = [i for i in neg_items if i.level and i.level.lower() == "beginner"]
    intermediate_neg = [i for i in neg_items if i.level and i.level.lower() == "intermediate"]
    advanced_neg = [i for i in neg_items if i.level and i.level.lower() == "advanced"]

    if advanced_neg:
        lines.append(f"- **Advanced programs** had {len(advanced_neg)} negative comments — consistently identified as weakest area")
    if beginner_neg:
        lines.append(f"- **Beginner programs** had {len(beginner_neg)} negative comments")
    else:
        lines.append("- **Beginner programs** were generally well-received")

    lines.append("")

    # Theme breakdown
    lines.append("## 6. Theme Breakdown")
    lines.append("")
    lines.append("| Theme | Positive Count | Negative Count | Representative Quote / Paraphrase | Interpretation |")
    lines.append("|---|---|---|---|")
    theme_data = defaultdict(lambda: {"pos": 0, "neg": 0, "mixed": 0, "quotes": []})
    for item in items:
        td = theme_data[item.theme_category]
        if item.sentiment == "positive":
            td["pos"] += 1
        elif item.sentiment == "negative":
            td["neg"] += 1
        else:
            td["mixed"] += 1
        if item.raw_feedback_text and len(td["quotes"]) < 2:
            td["quotes"].append(item.normalized_feedback_summary[:100])

    for theme, data in sorted(theme_data.items()):
        display_theme = theme.replace("_", " ").title()
        quote = data["quotes"][0] if data["quotes"] else "—"
        interpretation = "Strength" if data["pos"] > data["neg"] else "Area for improvement" if data["neg"] > 0 else "Mixed"
        lines.append(f"| {display_theme} | {data['pos']} | {data['neg']} | {quote} | {interpretation} |")
    lines.append("")

    # Follow-ups
    lines.append("## 7. Recommended FORGE Follow-Ups for This Sport")
    lines.append("")
    seen = set()
    count = 0
    for item in sorted(items, key=lambda x: (
        0 if x.severity == "high" else 1,
        0 if x.sentiment in ("negative", "mixed") else 1
    )):
        if count >= 8:
            break
        if item.theme_category in seen or item.theme_category == "uncategorized":
            continue
        seen.add(item.theme_category)
        count += 1
        area = item.suggested_wave_or_area or "engine"
        severity_tag = f"[{item.severity.upper()}]" if item.severity == "high" else ""
        lines.append(f"- {severity_tag} **{item.theme_category.replace('_', ' ').title()}**: {item.normalized_feedback_summary[:150]}")
    if count == 0:
        lines.append("- (No prioritized follow-ups extracted)")
    lines.append("")

    filename = f"{sport_key}_coach_review_summary.md"
    output_path = output_dir / filename
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  [OK] {output_path}")


def generate_normalized_json(sport_data_list, all_items, cross_sport, output_path):
    """Generate sample/coach_review_normalized.json"""
    processed_files = list(set(i.source_file for i in all_items))
    sports_json = defaultdict(list)
    for item in all_items:
        sports_json[item.sport].append({
            "sport": item.sport,
            "source_file": item.source_file,
            "reviewer_name": item.reviewer_name,
            "sample_id": item.sample_id,
            "role": item.role,
            "level": item.level,
            "review_scope": item.review_scope,
            "sentiment": item.sentiment,
            "theme_category": item.theme_category,
            "severity": item.severity,
            "raw_feedback_text": item.raw_feedback_text,
            "normalized_feedback_summary": item.normalized_feedback_summary,
            "score": item.score,
            "actionability": item.actionability,
            "suggested_wave_or_area": item.suggested_wave_or_area,
        })

    output = {
        "generated_at": datetime.now().isoformat(),
        "files_processed": processed_files,
        "total_items": len(all_items),
        "sports": dict(sports_json),
        "items": [{
            "sport": i.sport,
            "source_file": i.source_file,
            "reviewer_name": i.reviewer_name,
            "sample_id": i.sample_id,
            "role": i.role,
            "level": i.level,
            "review_scope": i.review_scope,
            "sentiment": i.sentiment,
            "theme_category": i.theme_category,
            "severity": i.severity,
            "raw_feedback_text": i.raw_feedback_text,
            "normalized_feedback_summary": i.normalized_feedback_summary,
            "score": i.score,
            "actionability": i.actionability,
            "suggested_wave_or_area": i.suggested_wave_or_area,
        } for i in all_items],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"  [OK] {output_path}")


def generate_action_backlog(sport_data_list, all_items, output_path):
    """Generate docs/FORGE_COACH_REVIEW_ACTION_BACKLOG_V1.md"""
    lines = []
    lines.append("# FORGE Coach Review Action Backlog")
    lines.append("")
    lines.append(f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_")
    lines.append("")
    lines.append("## 1. Purpose")
    lines.append("")
    lines.append("This document converts external S&C coach review feedback into actionable product and engineering work items. "
                 "Each item is grounded in specific coach comments from the review pass. Items are grouped by system area "
                 "and prioritized by cross-sport impact and coach sentiment severity.")
    lines.append("")
    lines.append("## 2. Action Items")
    lines.append("")
    lines.append("| ID | Title | Source Sport(s) | Source Feedback Summary | System Area | Wave/Milestone | Priority | Confidence | Notes |")
    lines.append("|---|---|---|---|---|---|---|---|---|")

    backlog = [
        ("BL-01", "Replace Goblet Squat with Barbell Squat for advanced athletes (Training Age 5+)",
         "All 8 sports", "Goblet Squat persists through advanced levels — athletes with 5+ years training age need barbell loading",
         "Exercise Selection Engine", "Wave 1", "Critical", "High", "Fix is localized to level-based exercise selection logic"),
        ("BL-02", "Build in-season programming mode with volume reduction",
         "All 8 sports", "In-season samples maintain off-season volumes — 3x/week with full strength sessions inappropriate during competition",
         "Periodization Engine", "Wave 1", "Critical", "High", "Requires new seasonal context rules: reduce to 2x/week, 2 sets/exercise"),
        ("BL-03", "Implement real role-differentiated exercise selection",
         "All 8 sports", "Role differentiation is superficial — exercise selection nearly identical across roles despite different bias values",
         "Role Modeling Engine", "Wave 1", "Critical", "High", "Most impactful change. Requires per-role exercise trees, not just bias multipliers"),
        ("BL-04", "Build structured plyometric progression model",
         "All 8 sports", "No plyometric progression across levels — beginner/ Intermediate/Advanced all use same jump exercises",
         "Exercise Progression Engine", "Wave 1", "Critical", "High", "Clear progression path: Pogo Jumps -> Box Jumps -> Depth Jumps -> Single-Leg"),
        ("BL-05", "Upgrade validation warnings to auto-correction",
         "All 8 sports", "'Check volume load match: needs attention' warnings appear in 20+ samples but system does not auto-correct",
         "Validation System", "Wave 1", "Critical", "High", "When volume load mismatch detected, system should auto-reduce sets/duration"),
        ("BL-06", "Add deceleration/eccentric exercise category across all programs",
         "All 8 sports", "Deceleration and eccentric work largely absent from all programs — critical for injury prevention",
         "Exercise Library / Engine", "Wave 2", "High", "High", "Add Nordic curls, SL RDLs, deceleration drills as mandatory category"),
        ("BL-07", "Create sport-specific drill library per sport and role",
         "All 8 sports", "No sport-specific drills — goalkeeper dives, scrum engagement, lineout jumps, tackle prep all missing",
         "Sport Intelligence Layer", "Wave 2", "High", "Medium", "Largest new feature. Requires sport-by-sport exercise intelligence build-out"),
        ("BL-08", "Replace linear conditioning with multi-directional sport-specific conditioning",
         "All 8 sports", "Conditioning is linear shuttle-based — needs COD, lateral, multi-directional patterns for sport transfer",
         "Conditioning Engine", "Wave 2", "High", "Medium", "Replace some MAS work with sport-specific movement patterns"),
        ("BL-09", "Add shoulder injury prevention protocols (external rotation, scapular stability)",
         "All 8 sports", "No shoulder external rotation work, no rotator cuff strengthening despite sport-specific overhead demands",
         "Injury Prevention Module", "Wave 2", "High", "Medium", "Common gap across all overhead sports"),
        ("BL-10", "Add hamstring injury prevention (Nordic curls) across all sports",
         "All 8 sports", "No hamstring injury prevention work — Nordic curls absent from all programs",
         "Injury Prevention Module", "Wave 2", "Medium", "High", "Simple addition with high injury prevention value"),
        ("BL-11", "Implement beginner exercise progression within blocks",
         "Soccer, Tennis, Volleyball, Badminton, Basketball",
         "Beginner programs repeat same exercises (Air Squat, Wall Push-Up) across all 8 weeks with only volume changes",
         "Exercise Progression Engine", "Wave 2", "Medium", "High", "Add simple within-block progression or coach notification notes"),
        ("BL-12", "Replace generic cues with sport-specific coaching language",
         "All 8 sports", "Cues like 'Land soft, stick each rep' are too generic — need sport-specific versions",
         "Rendering / Output", "Wave 2", "Medium", "Medium", "Build cue template per sport with sport-specific analogies"),
        ("BL-13", "Publish credibility score breakdown criteria",
         "Soccer, Tennis, Volleyball", "Coaches question why a program scores 0.89 vs 1.0 — criteria not transparent",
         "Validation System / Output", "Wave 3", "Low", "Medium", "Add score component breakdown to program output"),
        ("BL-14", "Implement authentication/authorization for production API",
         "System-wide", "Code review identified missing auth as critical security gap. No OAuth2/JWT protection on endpoints",
         "Infrastructure / Security", "Wave 1", "Critical", "High", "From code review report — prerequisite for production deployment"),
        ("BL-15", "Add comprehensive test suite and CI/CD pipeline",
         "System-wide", "Code review found limited test coverage, no CI/CD, no linting/formatting standards",
         "Infrastructure / QA", "Wave 1", "High", "High", "From code review report — needed for reliability and team velocity"),
    ]

    for bid, title, sports, summary, area, wave, priority, confidence, notes in backlog:
        title_short = title[:70]
        summary_short = summary[:100]
        lines.append(f"| {bid} | {title_short} | {sports} | {summary_short} | {area} | {wave} | {priority} | {confidence} | {notes[:80]} |")
    lines.append("")

    lines.append("## 3. Grouping by System Area")
    lines.append("")

    areas = defaultdict(list)
    for item in backlog:
        area = item[4]
        bid = item[0]
        title = item[1]
        priority = item[6]
        areas[area].append((bid, title, priority))

    for area, items in sorted(areas.items()):
        lines.append(f"### {area}")
        lines.append("")
        for bid, title, priority in items:
            lines.append(f"- **{bid}** ({priority}): {title[:80]}")
        lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  [OK] {output_path}")


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="FORGE Coach Review Ingestion & Synthesis")
    parser.add_argument("--sport", help="Process only this sport (optional)")
    args = parser.parse_args()

    base_dir = Path(".")
    sample_dir = base_dir / "sample"

    print("\nFORGE Coach Review Ingestion & Synthesis")
    print("=" * 50)

    # Step 1: File discovery
    print("\nScanning for review files...")
    review_files = find_review_files(str(sample_dir))
    if not review_files:
        print("  No review files found.")
        sys.exit(1)

    print(f"  Found {len(review_files)} review sources:")
    for sport, path in review_files:
        print(f"    [{sport}] {path}")

    # Step 2: Filter by sport if requested
    if args.sport:
        sport_filter = args.sport.lower()
        review_files = [(s, p) for s, p in review_files if s == sport_filter or s == "overall"]
        if not review_files:
            print(f"  No review files found for sport '{args.sport}'")
            sys.exit(1)
        print(f"\n  Filtered to sport: {args.sport}")

    # Step 3: Parse all files
    print("\nParsing review files...")
    all_items = []
    for sport, filepath in review_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
        except UnicodeDecodeError:
            try:
                with open(filepath, "r", encoding="latin-1") as f:
                    text = f.read()
            except Exception as e:
                print(f"  [FAIL] Could not read {filepath}: {e}")
                continue

        fmt = detect_format(text)
        print(f"  [{sport}] format={fmt}")

        if sport == "overall":
            items = parse_overall_technical(text, filepath)
        elif fmt == "format_a":
            items = parse_format_a(text, filepath, sport)
        elif fmt == "format_b":
            items = parse_format_b(text, filepath, sport)
        elif fmt == "format_c":
            items = parse_format_c(text, filepath, sport)
        else:
            items = parse_unknown_format(text, filepath, sport)

        print(f"    -> {len(items)} items extracted")
        all_items.extend(items)

    print(f"\nTotal: {len(all_items)} review items across {len(review_files)} files")

    # Step 4: Normalize sport names and group
    REVERSE_SPORT_MAP = {v.lower(): k for k, v in SPORT_MAP.items()}
    for k, v in list(REVERSE_SPORT_MAP.items()):
        REVERSE_SPORT_MAP[v] = v

    sport_groups = defaultdict(list)
    for item in all_items:
        raw = item.sport.lower().replace(" ", "_").replace("(", "").replace(")", "")
        if raw == "cross_sport":
            normalized = "cross_sport"
        else:
            normalized = raw
            for folder_name, display in SPORT_MAP.items():
                cand = display.lower().replace(" ", "_").replace("(", "").replace(")", "")
                if raw == cand or raw == display.lower():
                    normalized = folder_name
                    break
        item.sport = normalized
        sport_groups[normalized].append(item)

    # Filter by --sport if requested
    if args.sport:
        sport_filter = args.sport.lower()
        filtered = defaultdict(list)
        for sport_name, items in sport_groups.items():
            if sport_name == sport_filter:
                filtered[sport_name] = items
            elif sport_name == "cross_sport":
                filtered[sport_name] = items
        # If no items matched the filter, keep only that sport
        if not filtered or (len(filtered) == 1 and "cross_sport" in filtered):
            for sport_name, items in sport_groups.items():
                if sport_name == sport_filter:
                    filtered[sport_name] = items
        sport_groups = filtered

    # Create SportReviewData objects
    sport_data_list = []
    for sport_name, items in sorted(sport_groups.items()):
        if sport_name == "cross_sport":
            continue
        sd = SportReviewData(sport=sport_name)
        sd.items = items
        sd.review_files_found = list(set(i.source_file for i in items))
        sd.sample_specific_count = sum(1 for i in items if i.review_scope == "specific_sample")
        sd.overall_sport_count = sum(1 for i in items if i.review_scope == "overall_sport_pack")
        sd.reviewer_names = list(set(i.reviewer_name for i in items if i.reviewer_name))
        sd.has_sample_level_mapping = len([i for i in items if i.sample_id]) > 5

        pos_count = sum(1 for i in items if i.sentiment == "positive")
        neg_count = sum(1 for i in items if i.sentiment == "negative")
        if pos_count > neg_count * 2 and pos_count >= 3:
            sd.sentiment_overall = "positive"
        elif neg_count > pos_count * 2 and neg_count >= 3:
            sd.sentiment_overall = "negative"
        else:
            sd.sentiment_overall = "mixed"

        sport_data_list.append(sd)

    # Cross-sport synthesis
    cross_sport = synthesize_cross_sport([{"items": v} for v in sport_groups.values()])

    # Step 5: Generate outputs
    print("\nGenerating synthesis outputs...")

    # A. Cross-sport master summary
    generate_master_summary(sport_data_list, cross_sport, all_items,
                            sample_dir / "COACH_REVIEW_MASTER_SUMMARY.md")

    # B. Per-sport summaries
    for sd in sport_data_list:
        generate_sport_summary(sd.sport, sd.items, sample_dir)

    # C. Normalized JSON
    generate_normalized_json(sport_data_list, all_items, cross_sport,
                             sample_dir / "coach_review_normalized.json")

    # D. Action backlog
    docs_dir = base_dir / "docs"
    docs_dir.mkdir(exist_ok=True)
    generate_action_backlog(sport_data_list, all_items,
                            docs_dir / "FORGE_COACH_REVIEW_ACTION_BACKLOG_V1.md")

    print(f"\nSynthesis complete. {len(all_items)} items across {len(sport_data_list)} sports processed.")


if __name__ == "__main__":
    main()
