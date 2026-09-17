"""
Forge Library Content Audit Tool
Phase 1F: Data Integrity & Quality Assurance

Scans exercises_data.py for missing critical fields and generates a detailed report.
Philosophy: "AI Enhanced, Never AI Dependent" - ensuring high-quality local data.
"""

import sys
import os
from typing import List, Dict, Any, Optional

# Add src to path to import forge modules
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from forge.exercises_data import EXERCISES_DATA as EXERCISES
except ImportError as e:
    print(f"ERROR: Could not import EXERCISES_DATA from forge.exercises_data: {e}")
    print("Please ensure you are running this from the src/forge/utils directory.")
    sys.exit(1)

# Critical fields that MUST exist for safety and coaching quality
CRITICAL_FIELDS = [
    'coaching_cues',
    'common_faults',  # Note: exercises_data uses 'common_faults' not 'common_errors'
    'contraindications'
]

# Important fields for progression and scaling
IMPORTANT_FIELDS = [
    'progression',    # Note: exercises_data uses singular 'progression' not 'progressions'
    'regression',     # Note: exercises_data uses singular 'regression' not 'regressions'
    'equipment_alternatives'
]

ALL_CHECKED_FIELDS = CRITICAL_FIELDS + IMPORTANT_FIELDS

class ExerciseAuditResult:
    def __init__(self, exercise_id: str, name: str, category: str):
        self.id = exercise_id
        self.name = name
        self.category = category
        self.missing_critical: List[str] = []
        self.missing_important: List[str] = []
        self.has_all_data = True

    def add_missing(self, field: str, is_critical: bool):
        self.has_all_data = False
        if is_critical:
            self.missing_critical.append(field)
        else:
            self.missing_important.append(field)

    def __str__(self):
        status = "✅ PASS" if self.has_all_data else "❌ FAIL"
        output = f"[{status}] {self.name} ({self.category})\n"
        
        if self.missing_critical:
            output += f"   ⚠️  MISSING CRITICAL: {', '.join(self.missing_critical)}\n"
        if self.missing_important:
            output += f"   ℹ️  MISSING IMPORTANT: {', '.join(self.missing_important)}\n"
        
        return output

def audit_exercises(exercises: List[Dict[str, Any]]) -> List[ExerciseAuditResult]:
    results = []
    
    for ex in exercises:
        # Handle both dict objects and objects with .to_dict() if applicable
        if hasattr(ex, 'to_dict'):
            data = ex.to_dict()
        else:
            data = ex
            
        ex_id = data.get('id', 'UNKNOWN')
        name = data.get('name', 'Unnamed Exercise')
        # exercises_data uses 'family' as primary category, fallback to 'category' if exists
        category = data.get('category') or data.get('family', 'Uncategorized')
        
        result = ExerciseAuditResult(ex_id, name, category)
        
        # Check Critical Fields
        for field in CRITICAL_FIELDS:
            value = data.get(field)
            if not value or (isinstance(value, list) and len(value) == 0):
                result.add_missing(field, is_critical=True)
        
        # Check Important Fields
        for field in IMPORTANT_FIELDS:
            value = data.get(field)
            if not value or (isinstance(value, list) and len(value) == 0):
                result.add_missing(field, is_critical=False)
        
        results.append(result)
    
    return results

def generate_report(results: List[ExerciseAuditResult]):
    total = len(results)
    passed = sum(1 for r in results if r.has_all_data)
    failed = total - passed
    
    print("\n" + "="*60)
    print("FORGE LIBRARY CONTENT AUDIT REPORT")
    print("="*60)
    print(f"Total Exercises Scanned: {total}")
    print(f"✅ Complete Data: {passed} ({(passed/total)*100:.1f}%)")
    print(f"❌ Missing Data: {failed} ({(failed/total)*100:.1f}%)")
    print("="*60 + "\n")

    # Aggregate Stats
    missing_counts = {field: 0 for field in ALL_CHECKED_FIELDS}
    category_stats = {}

    for r in results:
        for field in r.missing_critical + r.missing_important:
            missing_counts[field] += 1
        
        cat = r.category
        if cat not in category_stats:
            category_stats[cat] = {'total': 0, 'failed': 0}
        category_stats[cat]['total'] += 1
        if not r.has_all_data:
            category_stats[cat]['failed'] += 1

    print("📊 FIELD COVERAGE ISSUES:")
    print("-" * 40)
    for field, count in missing_counts.items():
        pct = (count / total) * 100
        bar = "█" * int(pct / 2)
        print(f"{field:<25}: {count:>3} ({pct:5.1f}%) {bar}")
    
    print("\n📂 CATEGORY BREAKDOWN (Sorted by % Incomplete):")
    print("-" * 40)
    sorted_cats = sorted(
        category_stats.items(), 
        key=lambda x: (x[1]['failed'] / x[1]['total']) if x[1]['total'] > 0 else 0,
        reverse=True
    )
    
    for cat, stats in sorted_cats:
        pct = (stats['failed'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"{cat:<20}: {stats['failed']:>3}/{stats['total']} incomplete ({pct:.1f}%)")

    print("\n🔴 TOP 20 EXERCISES NEEDING ATTENTION:")
    print("-" * 40)
    # Sort by number of missing fields (critical weighted higher)
    failed_results = [r for r in results if not r.has_all_data]
    failed_results.sort(key=lambda x: (len(x.missing_critical) * 2 + len(x.missing_important)), reverse=True)
    
    for i, r in enumerate(failed_results[:20], 1):
        critical_count = len(r.missing_critical)
        important_count = len(r.missing_important)
        print(f"{i:2}. {r.name}")
        print(f"    Category: {r.category}")
        print(f"    Missing: {', '.join(r.missing_critical + r.missing_important)}")

    print("\n" + "="*60)
    print("RECOMMENDATION:")
    if any(r.missing_critical for r in results):
        print("⚠️  CRITICAL: Some exercises lack safety/coaching data.")
        print("   Priority: Fill 'contraindications' and 'coaching_cues' first.")
    else:
        print("✅ Library data integrity is high.")
    print("="*60 + "\n")

def save_json_report(results: List[ExerciseAuditResult], filename: str = "audit_report.json"):
    import json
    report_data = {
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r.has_all_data),
            "failed": sum(1 for r in results if not r.has_all_data)
        },
        "exercises_needing_work": [
            {
                "id": r.id,
                "name": r.name,
                "category": r.category,
                "missing_critical": r.missing_critical,
                "missing_important": r.missing_important
            }
            for r in results if not r.has_all_data
        ]
    }
    
    with open(filename, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"💾 Detailed JSON report saved to: {filename}")

if __name__ == "__main__":
    print("🔍 Starting Forge Library Audit...")
    results = audit_exercises(EXERCISES)
    generate_report(results)
    save_json_report(results)
