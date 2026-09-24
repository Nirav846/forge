# FORGE Library Enhancement Plan
## "AI Enhanced, Never AI Dependent" - Full Stack Development Roadmap

> **Re-baseline note (2026-09-24):** The "Current State" below predates later
> library phases. Since then: `/api/v1/exercises` endpoints are implemented in
> `src/forge/api_server.py` (see `docs/API_REFERENCE.md`); the frontend seed
> grew to 537 exercises / 222 complexes (`docs/DATA_MODEL.md`); and library
> enhancement phases through migration 000035 shipped. Items marked done in
> retired phase reports were consolidated into `CHANGELOG.md`. Verify each
> remaining roadmap item against current code before starting work.

**Current State:** *(historical baseline)*
- Backend: 334 exercises in monolithic `exercises_data.py` (7,708 lines)
- Frontend: React/TypeScript app with exercise library page at `/library`
- Data: exercises.json (574KB) in frontend data folder
- API: Calls to `/api/exercises` endpoint (needs implementation)
- Knowledge: Exercises have coaching cues, common errors, contraindications, progressions/regressions

**Goal:** Reorganize, enhance, and build a production-ready offline-first exercise library system with Room database integration.

---

## 🏗️ PHASED APPROACH

### **PHASE 0: Foundation & Audit** ✅ (PRE-REQUISITE)
**Status:** Complete
- [x] Exercise data exists with metadata (coaching cues, faults, contraindications)
- [x] Frontend library page exists
- [x] Basic filtering UI implemented

**Verification Checkpoint 0:**
```bash
# Verify exercise data exists
python3 -c "from src.forge.exercises_data import EXERCISES_DATA; print(f'Exercises: {len(EXERCISES_DATA)}')"
# Expected: 334 exercises
```

---

### **PHASE 1: Backend API Implementation** 
**Goal:** Create REST API endpoints for exercise library access

#### Tasks:
1. **Create API Routes** (`src/forge/api_server.py`)
   - `GET /api/exercises` - List all exercises with filtering
   - `GET /api/exercises/{id}` - Get single exercise details
   - `GET /api/exercises/categories` - List unique categories
   - `GET /api/exercises/search?q=` - Search exercises

2. **Add Serializers** (`src/forge/api_serializers.py`)
   - Exercise serialization to JSON
   - Filter parameter validation

3. **Integrate with FastAPI**
   - Add CORS support for frontend
   - Add request/response models

#### Deliverables:
- Working API endpoints
- Swagger documentation at `/docs`
- Unit tests for API endpoints

#### Verification Checkpoint 1:
```bash
# Test API endpoint
curl http://localhost:8000/api/exercises | jq '. | length'
# Expected: 334

# Test single exercise
curl http://localhost:8000/api/exercises/DLKD-001 | jq '.name'
# Expected: "Air Squat"
```

**Exit Criteria:** All API endpoints return correct data, frontend can fetch exercises

---

### **PHASE 2: Data Reorganization & Modularization**
**Goal:** Break monolithic exercise file into organized modules

#### Tasks:
1. **Create New Directory Structure**
```
src/forge/library/
├── __init__.py
├── base.py              # Base classes, types, enums
├── loader.py            # Data loading API
├── exercises/
│   ├── __init__.py
│   ├── strength.py      # DLKD, DLHD, SLKD, SLHD
│   ├── power.py         # Ball, Plyo, Sprint
│   ├── upper.py         # HPush, HPull, VPush, VPull
│   ├── core.py          # Core, Carry, Rot
│   └── conditioning.py  # Conditioning exercises
├── profiles/
│   ├── __init__.py
│   └── sport_profiles.py # Sport-specific exercise mappings
└── blueprints/
    ├── __init__.py
    └── training_plans.py # Blueprint definitions
```

2. **Migrate Data**
   - Split exercises by family/category
   - Remove duplicate coaching cues (DRY principle)
   - Add validation on load

3. **Create Loader API**
   - `get_exercise(id)` - Single exercise
   - `get_exercises_by_family(family)` - Filter by family
   - `get_all_exercises()` - Full library
   - `search_exercises(query)` - Search functionality

#### Deliverables:
- Modular exercise library
- Backward compatible imports
- Data validation layer

#### Verification Checkpoint 2:
```bash
# Verify modular imports work
python3 -c "from src.forge.library.exercises.strength import STRENGTH_EXERCISES; print(len(STRENGTH_EXERCISES))"
python3 -c "from src.forge.library.loader import get_exercise; print(get_exercise('DLKD-001')['name'])"
# Expected: Correct counts and exercise names
```

**Exit Criteria:** All exercises accessible via new modular structure, old imports still work

---

### **PHASE 3: Frontend Integration & Offline Support**
**Goal:** Connect frontend to API and add offline-first capabilities

#### Tasks:
1. **Update Exercise Service** (`src/modules/exercises/exerciseService.ts`)
   - Point to actual API instead of mock data
   - Add error handling
   - Add caching layer

2. **Implement Local Storage/IndexedDB**
   - Cache exercises on first load
   - Serve from cache when offline
   - Background sync when online

3. **Enhance UI Components**
   - Add loading states
   - Add error boundaries
   - Improve mobile responsiveness
   - Add "Click for Details" modal with full exercise knowledge

4. **Add Exercise Detail View**
   - Coaching cues (if available)
   - Common errors
   - Contraindications
   - Progressions/Regressions
   - Equipment alternatives
   - Video/image placeholders (for future)

#### Deliverables:
- Working library page connected to API
- Offline support via IndexedDB
- Detailed exercise modal

#### Verification Checkpoint 3:
```bash
# Start dev server and verify
cd forge_web && npm run dev
# Visit http://localhost:5173/library
# Verify: 
#   - Exercises load from API
#   - Filters work
#   - Click shows detail modal
#   - Works offline after first load
```

**Exit Criteria:** Frontend displays all exercises with details, works offline

---

### **PHASE 4: Room Database Integration (Android)**
**Goal:** Implement local persistence with Room database

#### Tasks:
1. **Create Android Project Structure** (if not exists)
```
app/src/main/java/com/forge/app/
├── data/
│   ├── local/
│   │   ├── dao/
│   │   │   └── ExerciseDao.kt
│   │   ├── entity/
│   │   │   └── ExerciseEntity.kt
│   │   └── ForgeDatabase.kt
│   └── repository/
│       └── ExerciseRepository.kt
├── domain/
│   └── model/
│       └── Exercise.kt
└── ui/
    └── library/
        └── LibraryViewModel.kt
```

2. **Define Room Entities**
   - ExerciseEntity with all fields
   - Type converters for arrays

3. **Create DAO**
   - Query methods matching API
   - Suspend functions for coroutines

4. **Build Repository Layer**
   - Network-first strategy
   - Cache fallback
   - Sync mechanism

#### Deliverables:
- Room database schema
- Repository with offline support
- ViewModel for UI

#### Verification Checkpoint 4:
```kotlin
// Run Android unit tests
./gradlew testDebugUnitTest
// Verify:
//   - Database creates successfully
//   - CRUD operations work
//   - Offline queries return cached data
```

**Exit Criteria:** Android app can store/query exercises offline via Room

---

### **PHASE 5: Content Enrichment**
**Goal:** Enhance exercise knowledge base

#### Tasks:
1. **Audit Existing Content**
   - Identify exercises missing detailed cues
   - Find duplicate/similar exercises
   - Validate progression/regression chains

2. **Add Missing Knowledge**
   - Setup instructions
   - Breathing patterns
   - Tempo prescriptions
   - Common modifications

3. **Add Multimedia Placeholders**
   - Image URL fields
   - Video URL fields
   - 3D model references (future)

4. **Create Validation Tools**
   - Check for broken progression chains
   - Identify orphan exercises
   - Validate difficulty ratings

#### Deliverables:
- Enriched exercise database
- Validation tools
- Content quality report

#### Verification Checkpoint 5:
```bash
# Run content audit
python3 src/forge/audit_library.py
# Expected: Report showing content completeness %
```

**Exit Criteria:** All exercises have complete knowledge fields, validation passes

---

### **PHASE 6: Advanced Features**
**Goal:** Add power-user features for coaches

#### Tasks:
1. **Exercise Comparison Tool**
   - Side-by-side comparison
   - Similar exercises suggestions
   - Substitution recommendations

2. **Custom Exercise Builder**
   - Create custom exercises
   - Save to local database
   - Share/export functionality

3. **Workout Integration**
   - Drag-drop to workout builder
   - Auto-populate prescriptions
   - Track exercise usage

4. **Analytics Dashboard**
   - Most used exercises
   - Category distribution
   - Athlete progression tracking

#### Deliverables:
- Comparison tool
- Custom exercise creator
- Analytics dashboard

#### Verification Checkpoint 6:
```bash
# Feature testing checklist
# - Compare 2 exercises side-by-side
# - Create custom exercise, save, retrieve
# - Add exercise to workout
# - View analytics dashboard
```

**Exit Criteria:** All advanced features functional and tested

---

## 📊 CURRENT STATUS CHECK ✅

**VERIFICATION CHECKPOINT 0 - COMPLETE:**

```bash
# Backend Exercise Data
python3 -c "from src.forge.exercises_data import EXERCISES_DATA; print(f'Exercises: {len(EXERCISES_DATA)}')"
# Result: 334 exercises ✅

# Frontend Exercise Data  
python3 -c "import json; data=json.load(open('/workspace/forge_web/src/data/exercises.json')); print(f'Frontend exercises: {len(data)}')"
# Result: 537 exercises ✅

# Exercise Knowledge Fields Present:
- coaching_cues ✅
- common_errors ✅
- contraindications ✅
- progressions/regressions ✅
- equipment_alternatives ✅
```

**Key Findings:**
1. ✅ Exercise knowledge EXISTS in both backend (334) and frontend (537)
2. ✅ Frontend already has offline-first service using local JSON
3. ⚠️ API endpoints exist but require PostgreSQL (not offline-first)
4. ✅ Frontend library page exists at `/library` with detail modal
5. ⚠️ Need to sync backend Python data with frontend JSON

**ADJUSTED STRATEGY:**
Following "AI Enhanced, Never AI Dependent" philosophy:
- Keep frontend working with local JSON (already offline-first)
- Add OPTIONAL Python API for sync/export features
- Focus Phase 1 on enhancing the existing frontend library experience
- Add missing knowledge fields where needed

---

## 🎯 REVISED PHASE 1A: Frontend Library Enhancement

**Goal:** Enhance the existing offline-first library homepage with better UX and complete exercise knowledge display

### Tasks:

1. **Verify Current Library Page Functionality**
   - Check if detail modal shows all knowledge fields
   - Verify filtering works correctly
   - Test mobile responsiveness

2. **Enhance Exercise Detail Modal**
   - Add "How to Perform" section from coaching cues
   - Show contraindications prominently (safety first)
   - Display progression/regression chain visually
   - Add equipment alternatives section

3. **Add Quick Actions**
   - "Add to Workout" button (future integration)
   - "Favorite" exercise toggle
   - Share/copy exercise ID

4. **Improve Search & Filter**
   - Add multi-select filters
   - Save filter presets
   - Add recently viewed exercises

### Deliverables:
- Enhanced library homepage
- Complete exercise detail view with all knowledge
- Better UX for coaches browsing exercises

### Verification Checkpoint 1A:
```bash
# Start dev server
cd forge_web && npm run dev

# Manual Testing Checklist:
# [ ] Library page loads with all 537 exercises
# [ ] Click any exercise shows detail modal
# [ ] Modal displays: coaching cues, common errors, contraindications
# [ ] Modal displays: progressions, regressions, equipment alternatives
# [ ] Filters work (category, difficulty, equipment, etc.)
# [ ] Search finds exercises by name
# [ ] Mobile view is usable
# [ ] Works offline (no network dependency)
```

**Exit Criteria:** Library homepage provides complete exercise knowledge at user's fingertips, fully offline

---

## 🔍 PHASE 0 VERIFICATION COMPLETE

Before proceeding to Phase 1A, let me verify the current state of the library page:
