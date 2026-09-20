"""Test data-driven adjustments to program volume and intensity."""
from __future__ import annotations
from typing import Optional, Dict, Any
from .models import AthleteProfile


BENCHMARKS: dict[str, dict[str, dict[str, float]]] = {
    "cricket": {
        "yoyo_ir1": {"academy": 16.0, "pro": 18.0, "elite": 20.0},
        "yoyo_ir2": {"academy": 14.0, "pro": 16.0, "elite": 18.0},
        "bronco": {"academy": 250, "pro": 240, "elite": 230},
        "cmj": {"academy": 45, "pro": 50, "elite": 55},
    },
    "default": {
        "yoyo_ir1": {"academy": 15.0, "pro": 17.0, "elite": 19.0},
        "yoyo_ir2": {"academy": 13.0, "pro": 15.0, "elite": 17.0},
        "bronco": {"academy": 260, "pro": 250, "elite": 240},
        "cmj": {"academy": 40, "pro": 45, "elite": 50},
    },
}


def _benchmarks(sport: str) -> dict[str, dict[str, float]]:
    return BENCHMARKS.get(sport.lower(), BENCHMARKS["default"])


def adjust_conditioning_volume(yoyo_score: Optional[float], sport: str = "default") -> float:
    """Return multiplier for conditioning volume (0.5-1.5). Poor YoYo -> more conditioning."""
    if yoyo_score is None:
        return 1.0
    bm = _benchmarks(sport).get("yoyo_ir1", {"academy": 16.0, "pro": 18.0})
    academy, pro = bm["academy"], bm["pro"]
    if yoyo_score < academy:
        deficit = (academy - yoyo_score) / max(academy, 1)
        return round(max(0.5, min(1.5, 1.0 + deficit * 0.5)), 2)
    elif yoyo_score < pro:
        return round(1.0 + (yoyo_score - academy) / max(pro - academy, 1) * 0.15, 2)
    else:
        excess = min((yoyo_score - pro) / max(pro, 1), 0.3)
        return round(max(0.5, 1.0 - excess * 0.3), 2)


def adjust_sprint_density(bronco_score: Optional[float], sport: str = "default") -> float:
    """Return multiplier for sprint density (0.5-1.5). Better Bronco -> more sprint work."""
    if bronco_score is None:
        return 1.0
    bm = _benchmarks(sport).get("bronco", {"academy": 250, "pro": 240})
    academy, pro = bm["academy"], bm["pro"]
    if bronco_score <= pro:
        excess = max(0, (pro - bronco_score) / max(pro, 1))
        return round(max(0.5, min(1.5, 1.0 + excess * 0.5)), 2)
    elif bronco_score <= academy:
        return round(1.0 + (academy - bronco_score) / max(academy - pro, 1) * 0.15, 2)
    else:
        deficit = min((bronco_score - academy) / max(academy, 1), 0.5)
        return round(max(0.5, 1.0 - deficit * 0.4), 2)


def adjust_power_emphasis(cmj_score: Optional[float], sport: str = "default") -> dict[str, Any]:
    """Return power emphasis adjustment based on CMJ."""
    if cmj_score is None:
        return {"power_emphasis": "medium", "multiplier": 1.0}
    bm = _benchmarks(sport).get("cmj", {"academy": 45, "pro": 50})
    academy, pro = bm["academy"], bm["pro"]
    if cmj_score < academy:
        deficit = max(0, (academy - cmj_score) / max(academy, 1))
        mult = round(max(1.0, min(1.3, 1.0 + deficit * 0.3)), 2)
        return {"power_emphasis": "high", "multiplier": mult}
    elif cmj_score < pro:
        return {"power_emphasis": "medium", "multiplier": 1.1}
    else:
        return {"power_emphasis": "low", "multiplier": 0.9}


def get_adjustments(athlete: AthleteProfile) -> dict[str, Any]:
    """Compute all test-driven adjustments. Returns dict with multipliers and human-readable notes."""
    sport = (athlete.sport or "default").lower()
    notes: list[str] = []
    has = bool(athlete.yoyo_ir1 is not None or athlete.bronco is not None or athlete.cmj is not None)

    cond = adjust_conditioning_volume(athlete.yoyo_ir1, sport)
    if has and cond != 1.0 and athlete.yoyo_ir1 is not None:
        pct = round(abs(cond - 1) * 100)
        notes.append(f"{'Increased' if cond > 1 else 'Reduced'} conditioning volume {pct}% based on YoYo score ({athlete.yoyo_ir1})")

    sprint = adjust_sprint_density(athlete.bronco, sport)
    if has and sprint != 1.0 and athlete.bronco is not None:
        pct = round(abs(sprint - 1) * 100)
        notes.append(f"{'Increased' if sprint > 1 else 'Reduced'} sprint density {pct}% based on Bronco score ({athlete.bronco}s)")

    power = adjust_power_emphasis(athlete.cmj, sport)
    if has and power["multiplier"] != 1.0 and athlete.cmj is not None:
        if power["power_emphasis"] == "high":
            notes.append(f"Biasing power exercises — CMJ ({athlete.cmj}cm) below academy benchmark")
        else:
            notes.append(f"Maintaining power emphasis — CMJ ({athlete.cmj}cm) at or above pro benchmark")

    return {
        "has_data": has,
        "conditioning_multiplier": cond,
        "sprint_multiplier": sprint,
        "power_emphasis": power["power_emphasis"],
        "power_multiplier": power["multiplier"],
        "adjustments": notes,
    }
