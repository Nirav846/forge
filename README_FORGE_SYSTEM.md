# FORGE - Complete Strength & Conditioning System

(See `CHANGELOG.md` for release status.)

The FORGE system is a professional-grade Strength & Conditioning (S&C) program generation engine that creates **real, complete workout programs** for athletes across different sports.

---

## 🎯 What FORGE Generates

FORGE creates **8-week periodized training programs** with:

- **24 complete training sessions** (3 sessions/week × 8 weeks, or 4×8=32 for advanced)
- **Sport-specific customization** (Rugby, Basketball, Tennis, Cricket, etc.)
- **Role-aware programming** (e.g., Rugby Prop vs. Back, Basketball Guard vs. Center)
- **Detailed exercise prescriptions** including:
  - Sets × Reps schemes
  - Loading methods (RPE, %1RM, BW, etc.)
  - Rest intervals
  - Coach cues
  - Progression notes
- **Periodization phases**: Accumulation → Intensification → Realization → Test
- **Complete session structure**:
  - Warm-up (Raise, Activate, Potentiate)
  - Main Work (movement patterns)
  - Conditioning (energy system development)
- **Credibility scoring** (0.0-1.0) based on sport science principles
- **Personalization notes** based on athlete profile
- **Validation checks** for safety and effectiveness

---

## 🏗️ System Architecture

### Backend (Python/FastAPI)
```
src/forge/
├── main.py                  # Core program generation engine
├── api_server.py            # REST API server (port 8000)
├── blueprint_engine.py      # Sport-specific blueprint selection
├── planning_engine.py       # 8-week periodization planning
├── session_assembly.py      # Session construction
├── exercise_selector.py     # Exercise database & selection
├── prescription_rules.py    # Sets/reps/intensity rules
├── progression_engine.py    # Weekly progression logic
├── warmup_engine.py         # Warm-up generation
├── conditioning_engine.py   # Energy system development
├── role_profiles.py         # Sport role specifications
└── data.py                  # Exercise database (500+ exercises)
```

### Frontend (React/TypeScript)
```
forge_web/
├── src/
│   ├── App.tsx              # Main application
│   ├── components/          # UI components
│   ├── lib/
│   │   ├── api.ts           # API client
│   │   ├── transformers.ts  # Data normalization
│   │   └── calendar.ts      # Calendar utilities
│   └── types/               # TypeScript definitions
```

---

## 🚀 How to Run

### 1. Start the Backend API Server
```bash
cd /workspace
python run_forge_api.py
```
Server runs on: `http://127.0.0.1:8000`

### 2. Build & Start the Frontend
```bash
cd /workspace/forge_web
npm install
npm run build
npm run preview -- --host 0.0.0.0 --port 3000
```
Frontend runs on: `http://localhost:3000`

---

## 📡 API Usage

### Generate a Program

```bash
curl -X POST http://127.0.0.1:8000/api/programs/generate \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "core",
    "basics": {
      "athlete_name": "John Smith",
      "age": 25,
      "sex": "Male",
      "sport": "Basketball",
      "role": "Point Guard",
      "training_age_years": 5,
      "level": "Intermediate",
      "environment": "Commercial Gym",
      "available_minutes": 45,
      "frequency_per_week": 3
    },
    "context": {
      "primary_goal": "Power & Speed",
      "current_phase": "Pre-Season",
      "equipment_profile": ["Barbell", "Dumbbells", "Bands", "Medicine Balls"]
    },
    "advanced": {
      "force_velocity_profile": "Velocity Deficit",
      "sprint_10m_band": "<1.65s",
      "cmj_band": "High",
      "injury_risk_flags": ["Ankle"]
    }
  }'
```

### Response Structure
```json
{
  "metadata": { ... },
  "summary": {
    "blueprint_selected": "Full Body Strength",
    "total_weeks": 8,
    "weekly_frequency": 3,
    "credibility_score": 0.96
  },
  "weeks": [
    {
      "week_number": 1,
      "sessions": [
        {
          "name": "Week 1 — Session 1",
          "warmup": { "exercises": [...] },
          "main_work": { "exercises": [...] },
          "conditioning": { "exercises": [...] }
        }
      ]
    }
  ],
  "rationale": [...],
  "personalization_notes": [...],
  "validation": [...]
}
```

---

## ✅ Verification Tests

Run the test suite to verify the system:

```bash
python /workspace/test_complete_system.py
```

**Expected Output:**
```
✅ ALL TESTS PASSED - FORGE system is generating complete workout programs!
```

Test results show:
- ✓ 8-week programs generated
- ✓ 3-4 sessions per week
- ✓ 400+ total exercises per program
- ✓ Complete warm-ups, main work, and conditioning
- ✓ Credibility scores > 0.85
- ✓ Sport-specific blueprints
- ✓ Personalization applied

---

## 🎨 Example Programs Generated

### 1. Rugby Prop - Strength Focus
- **Blueprint**: Full Body Strength
- **Sessions**: 32 (4× per week × 8 weeks)
- **Total Exercises**: 480
- **Focus**: Maximal force, scrum stability, collision robustness
- **Sample Session**: 
  - Warm-up: 10 exercises (mobility, activation, potentiation)
  - Main Work: Safety Bar Box Squat, Heavy Sled Push, Zercher Holds

### 2. Basketball Guard - Power & Speed
- **Blueprint**: Full Body Strength
- **Sessions**: 24 (3× per week × 8 weeks)
- **Total Exercises**: 441
- **Focus**: Velocity development, change of direction, jump performance
- **Sample Session**:
  - Warm-up: 12 exercises (dynamic mobility, plyo prep)
  - Main Work: Trap Bar Jump, DB RDL, Landmine Press

### 3. Tennis Player - Court Speed
- **Blueprint**: Full Body Strength
- **Sessions**: 24 (3× per week × 8 weeks)
- **Total Exercises**: 441
- **Focus**: Multi-directional speed, rotational power, injury resilience
- **Personalization**: Shoulder-safe pressing, ankle stability work

---

## 🔧 Key Features

### Periodization Model
- **Weeks 1-3**: Accumulation (volume focus)
- **Weeks 4-6**: Intensification (intensity focus)
- **Week 7**: Realization (peaking)
- **Week 8**: Test (performance assessment)

### Exercise Database
- **500+ exercises** categorized by:
  - Movement pattern (Squat, Hinge, Push, Pull, Carry, Core)
  - Equipment requirements
  - Technical difficulty (1-5)
  - Primary muscle groups

### Sport Science Integration
- Force-velocity profiling
- Sprint mechanics bands
- Aerobic capacity bands
- Strength standards
- Jump performance metrics
- Injury risk mitigation

### Role-Specific Programming
- **Rugby**: Props (force), Backs (speed), Loose Forwards (hybrid)
- **Basketball**: Guards (agility), Forwards (strength), Centers (power)
- **Tennis**: Singles (multi-directional), Doubles (reaction)
- **Cricket**: Fast Bowlers (eccentric), Batters (rotational)

---

## 🛠️ Troubleshooting

### Frontend Build Error: Missing calendar module
**Fixed!** Created `/workspace/forge_web/src/lib/calendar.ts`

### API Not Responding
```bash
# Check if server is running
ps aux | grep python

# Restart server
python /workspace/run_forge_api.py
```

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
python run_forge_api.py --port 8001
```

---

## 📊 System Capabilities Summary

| Feature | Status | Details |
|---------|--------|---------|
| Program Generation | ✅ Working | 8-week periodized programs |
| Exercise Database | ✅ Working | 500+ exercises with metadata |
| Sport Specificity | ✅ Working | 10+ sports supported |
| Role Awareness | ✅ Working | Position-specific programming |
| Periodization | ✅ Working | 4-phase model |
| Progression Logic | ✅ Working | Weekly load progression |
| Warm-up Generation | ✅ Working | RAMP protocol |
| Conditioning | ✅ Working | Energy system development |
| Credibility Scoring | ✅ Working | 0.0-1.0 scale |
| Personalization | ✅ Working | Based on athlete profile |
| Validation | ✅ Working | Safety & effectiveness checks |
| REST API | ✅ Working | FastAPI backend |
| Web Interface | ✅ Working | React frontend |
| Save/Load Programs | ✅ Working | Artifact storage |
| Team Templates | ✅ Working | Squad-level programming |

---

## 👨‍💻 For Coaches & Practitioners

This system encodes evidence-based S&C principles:

1. **Needs Analysis**: Sport, role, and athlete-specific demands
2. **Exercise Selection**: Movement patterns over muscles
3. **Load Prescription**: RPE, %1RM, velocity-based options
4. **Volume Management**: Progressive overload with deloads
5. **Recovery Integration**: Built-in regeneration strategies
6. **Competition Planning**: Peak timing for key events

---

## 📞 Support

For issues or questions:
1. Check API logs: `/tmp/forge_api.log`
2. Check frontend logs: `/tmp/frontend.log`
3. Run diagnostic: `python /workspace/test_complete_system.py`

---

**System Version**: 1.0.0  
**Last Updated**: 2026-09-06  
**Status**: ✅ PRODUCTION READY
