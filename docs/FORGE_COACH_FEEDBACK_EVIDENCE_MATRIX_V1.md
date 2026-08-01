# FORGE Coach Feedback — Evidence Matrix

**Source of truth**: Raw review files in `sample/`. This matrix maps every distinct
coach observation to a structured evidence row. Each row is grounded in specific
review text, not synthetic inference.

---

## How to Read This

| Column | Meaning |
|---|---|
| ID | `CF-xxx` — stable reference for backlog cross-referencing |
| Sport(s) | Which sport review(s) produced this evidence |
| Role/Level | When the feedback is role- or level-specific |
| Source | Exact file path |
| Evidence | Verbatim or tightly paraphrased coach text |
| Theme | Canonical theme category |
| Scope | Presentation vs. engine vs. exercise vs. periodization vs. trust |
| Severity | Critical / High / Medium / Low |
| Frequency | Isolated / Repeated / Cross-sport Systemic |
| Root Cause | Hypothesis about which FORGE layer is responsible |
| Action | What a fix would entail |

---

## Evidence Rows

### CF-001: Advanced Goblet Squat ceiling
| Field | Value |
|---|---|
| Sport(s) | Badminton, Basketball, Cricket, Football, Rugby, Soccer, Tennis, Volleyball |
| Role/Level | Advanced (Training Age 5+ years) |
| Source | `sample/badminton/badminton_review_sheet.md:80`, `sample/basketball/basketball_review_sheet.md:91`, `sample/cricket/cricket_review_sheet.md:80`, `sample/football/football_review_sheet.md:162`, `sample/rugby/rugby_review_sheet.md:65` |
| Evidence | "No advanced athlete should be performing Goblet Squats. For an athlete with 5+ years training age and a strength base (Strength Base Met = Yes), Goblet Squats are an accessory exercise, not a primary strength stimulus." — Badminton review. Football: "Advanced strikers still doing Goblet Squats and Wall Push-Ups." Cricket: "The system is overly conservative, likely to prioritise safety over adaptation." |
| Theme | Exercise selection ceiling |
| Scope | Programming logic — exercise selection engine |
| Severity | Critical |
| Frequency | Cross-sport systemic (appears in all 8 sports) |
| Root Cause | `exercise_library` has no level-dependent exercise progression rules. The engine selects "safe" exercises and never graduates athletes to barbell variants. Likely a missing `advanced_loading` flag or level-based exercise tier. |
| Action | Add level-to-exercise-tier mapping. Advanced athletes should default to Barbell Squat / Trap Bar Deadlift / Bulgarian Split Squat, not Goblet Squat. |

---

### CF-002: Superficial role differentiation
| Field | Value |
|---|---|
| Sport(s) | Badminton, Basketball, Cricket, Football, Rugby, Soccer, Tennis, Volleyball |
| Role/Level | All roles |
| Source | `sample/badminton/badminton_review_sheet.md:4`, `sample/basketball/basketball_review_sheet.md:4`, `sample/cricket/cricket_review_sheet.md:76`, `sample/rugby/rugby_review_sheet.md:452` |
| Evidence | Cricket: "The system appears to have been designed with a 'one-size-fits-all' strength template that is then cosmetically adapted with different role tags." Badminton: "Exercise selection is nearly identical across roles at the same level." Basketball: "Guard Intermediate A, Wing Intermediate A, and Big Intermediate A all feature Bulgarian Split Squats, Med Ball Slams, and similar conditioning protocols. The Personalization Notes differ but the actual programming does not." |
| Theme | Role specificity |
| Scope | Programming logic — role modelling engine |
| Severity | Critical |
| Frequency | Cross-sport systemic (appears in all 8 sports) |
| Root Cause | `role_profiles` contain bias values (e.g. velocity: 0.8, force: 0.6) but these only influence exposure targets, not exercise selection. The exercise selection tree is shared across roles at the same level. |
| Action | Implement role-specific exercise trees. Each role should have a distinct pool of exercises filtered by the role's biomechanical demands (e.g. Fast Bowlers get eccentric work, Batters get rotational work). |

---

### CF-003: In-season volume too high
| Field | Value |
|---|---|
| Sport(s) | Badminton, Basketball, Cricket, Football, Rugby, Soccer, Tennis, Volleyball |
| Role/Level | In-season / Advanced |
| Source | `sample/overall_review.txt:22`, `sample/badminton/badminton_review_sheet.md:26`, `sample/basketball/basketball_review_sheet.md:25`, `sample/soccer/soccer_review_sheet.md:41`, `sample/volleyball/volleyball_review_sheet.md:43`, `sample/tennis/tennis_review_sheet.md:41`, `sample/rugby/rugby_review_sheet.md:325` |
| Evidence | Overall review: "The in-season samples still include 3x/week heavy strength work. A coach would expect reduced volume and increased emphasis on power maintenance and recovery." Rugby: "Reduce in-season volume — 3x/week with 12-15 exercises, not 18-24." Tennis: "In Season but still includes 3x/week heavy strength work (3 sets of 3-5 reps) and conditioning." |
| Theme | In-season / taper logic |
| Scope | Periodization engine |
| Severity | Critical |
| Frequency | Cross-sport systemic (appears in all 8 sports) |
| Root Cause | No in-season programming mode exists. The seasonal context flag is set but does not alter volume/intensity/frequency rules. The engine applies the same block logic regardless of season. |
| Action | Build a distinct in-season rule set: 1-2x/week, 2 sets/exercise, reduce conditioning, add pre-match activation and post-match recovery protocols. Match-day scheduling awareness. |
| Source Classification | **COACH_PROGRAMMING** (from overall_review.txt lines 1–110 coach feedback) |

---

### CF-004: No plyometric / landing progression
| Field | Value |
|---|---|
| Sport(s) | Badminton, Basketball, Cricket, Football, Rugby |
| Role/Level | All levels |
| Source | `sample/badminton/badminton_review_sheet.md:76`, `sample/basketball/basketball_review_sheet.md:81`, `sample/cricket/cricket_review_sheet.md:40`, `sample/football/football_review_sheet.md:49`, `sample/rugby/rugby_review_sheet.md:125` |
| Evidence | Badminton: "The lack of plyometric progression across all levels is a significant deficiency. Beginner: Pogo Jumps. Intermediate: Squat Jumps, Box Jumps. Advanced: Depth Jumps, Single-leg Hops, Lateral Bounds. This progression is entirely absent." Basketball: "Basketball players need extensive jump and landing training to develop power and prevent injury. This progression is entirely absent." Rugby: "Jump/Landing exposure target: High but no plyometric variation — Only basic jumping appears." |
| Theme | Plyometric progression |
| Scope | Programming logic — exercise progression engine |
| Severity | High |
| Frequency | Cross-sport systemic (appears in all 8 sports at some level) |
| Root Cause | The engine has no plyometric progression model. Exercises are selected statically per level rather than following a periodized plyometric development pathway. |
| Action | Build a level-dependent plyometric progression tree: Beginner (Pogo Jumps, Box Step-Downs) -> Intermediate (Box Jumps, Squat Jumps) -> Advanced (Depth Jumps, Single-Leg Hops, Lateral Bounds). Progression should also occur within blocks. |

---

### CF-005: Validation system is diagnostic only, not corrective
| Field | Value |
|---|---|
| Sport(s) | Badminton, Basketball, Cricket, Football, Rugby |
| Role/Level | Advanced / Intermediate |
| Source | `sample/badminton/badminton_review_sheet.md:62`, `sample/basketball/basketball_review_sheet.md:67`, `sample/cricket/cricket_review_sheet.md:62`, `sample/football/football_review_sheet.md:136`, `sample/rugby/rugby_review_sheet.md:321` |
| Evidence | Cricket: "The system is detecting that the cumulative training load exceeds what is appropriate, but the program proceeds anyway. This suggests a logic gap — it can identify a problem but does not address it." Badminton: "Check volume load match: needs attention warning — system-generated red flag ignored." Basketball: "The validation warnings appearing in 5 advanced programs is a critical failure. The system identifies the problem but does not correct it." |
| Theme | Validation / auto-correction |
| Scope | Programming logic — validation system |
| Severity | Critical |
| Frequency | Repeated (appears in 5/8 sports explicitly, noted by overall reviewer) |
| Root Cause | The `validation` module checks volume-load mismatch and emits a warning but has no corrective feedback loop to the `session_assembly` or `program_builder` modules. Detection exists; correction does not. |
| Action | Wire validation warnings into the program builder as constraint inputs. When "volume load match: needs attention" fires, auto-reduce sets/number of exercises in affected categories. |

---

### CF-006: No deceleration / eccentric work
| Field | Value |
|---|---|
| Sport(s) | Football, Rugby, Badminton, Basketball, Soccer, Tennis, Volleyball |
| Role/Level | All, especially speed roles |
| Source | `sample/football/football_review_sheet.md:140`, `sample/rugby/rugby_review_sheet.md:323`, `sample/badminton/badminton_review_sheet.md:40`, `sample/basketball/basketball_review_sheet.md:17` |
| Evidence | Football: "Week 2-8 all show 0 eccentric exercises — where is the deceleration control work for high-speed running?" Rugby: "Deceleration largely ignored — Injury risk — Add eccentric-focused exercises." Badminton: "No specific landing mechanics training. No lateral bounds, single-leg hops, or depth jumps. This is a significant omission for injury prevention." |
| Theme | Eccentric / deceleration coverage |
| Scope | Exercise selection — missing exercise category |
| Severity | High |
| Frequency | Cross-sport systemic (appears in 7/8 sports) |
| Root Cause | The exercise library lacks a dedicated deceleration/eccentric category. Nordic curls, SL RDLs, deceleration drills, and landing mechanics exercises are not present in the default pool for most sports/roles. |
| Action | Add deceleration/eccentric as a mandatory exercise family across all programs. Include Nordic curls, single-leg RDLs, eccentric step-downs, deceleration drills. Prioritize for speed/agility roles (Wingers, Fullbacks, Back Three, Guards). |

---

### CF-007: No sport-specific drill integration
| Field | Value |
|---|---|
| Sport(s) | Football, Rugby, Badminton, Basketball, Cricket, Soccer, Tennis, Volleyball |
| Role/Level | All roles |
| Source | `sample/football/football_review_sheet.md:22`, `sample/rugby/rugby_review_sheet.md:24`, `sample/cricket/cricket_review_sheet.md:66`, `sample/overall_review.txt:26` |
| Evidence | Football: "The programs lack specific sport drills (e.g., goalkeeper reaction drills, striker finishing work)." Rugby: "No scrum-specific work — Props, Hookers, and Locks lack any sport-specific contact preparation. No lineout jumping drills. No tackle preparation." Cricket: "A cricket-specific exercise library that includes sport-relevant movements across all categories (rotational power, eccentric hamstring work, landing mechanics, reactive agility)." Overall review: Provides detailed sport-specific exercise addition tables for volleyball (7 exercises), tennis (7), soccer (7). |
| Theme | Sport-specific exercise library |
| Scope | Exercise selection — missing library |
| Severity | High |
| Frequency | Cross-sport systemic (appears in all 8 sports) |
| Root Cause | FORGE has no sport-specific drill layer. All exercises are generic S&C movements. There is no mechanism to include sport-specific drills (e.g. block jumps for volleyball, scrum engagement for rugby, goalkeeper dives for football). |
| Action | Create a per-sport drill library mapped to roles. Start with the exercises explicitly recommended by coaches in overall_review.txt. Integrate as optional "role-specific drill" slots per session. |
| Source Classification | **COACH_PRODUCT** (from overall_review.txt lines 1–110 coach feedback) |

---

### CF-008: Conditioning too linear / lacks sport-specific movement
| Field | Value |
|---|---|
| Sport(s) | Soccer, Tennis, Volleyball, Badminton, Basketball, Football, Rugby |
| Role/Level | All |
| Source | `sample/soccer/soccer_review_sheet.md:39`, `sample/tennis/tennis_review_sheet.md:39`, `sample/volleyball/volleyball_review_sheet.md:41`, `sample/football/football_review_sheet.md:119` |
| Evidence | Soccer: "A coach might prefer more game-based conditioning (small-sided games, possession drills) integrated with the technical/tactical work, rather than 'running' sessions." Tennis: "Conditioning is largely linear shuttle work, which is good for aerobic capacity but may not fully prepare the athlete for the court's multidirectional demands." Volleyball: "A coach might expect more volleyball-specific movement patterns, such as block jumps, approach jumps, and defensive shuffles." |
| Theme | Conditioning specificity |
| Scope | Programming logic — conditioning engine |
| Severity | Medium |
| Frequency | Repeated (appears in 6/8 sports) |
| Root Cause | The conditioning engine selects protocols by metabolic demand (MAS, RSA, intervals) without considering movement pattern. A "conditioning" slot always produces linear or shuttle running regardless of sport. |
| Action | Add movement-pattern awareness to conditioning protocol selection. Court sports get multi-directional conditioning (COD, lateral shuffles, sport-specific patterns). Collision sports get repeated-effort conditioning with direction changes. |

---

### CF-009: No injury prevention protocols
| Field | Value |
|---|---|
| Sport(s) | Football, Rugby, Badminton, Basketball, Cricket |
| Role/Level | All |
| Source | `sample/football/football_review_sheet.md:196`, `sample/rugby/rugby_review_sheet.md:335`, `sample/badminton/badminton_review_sheet.md:82`, `sample/basketball/basketball_review_sheet.md:87` |
| Evidence | Football: "No injury prevention work (e.g., ACL prevention, groin strengthening)." Rugby: "No injury prevention work — ACL prevention, hamstring (Nordic curls), shoulder stability." Badminton: "The programs include no specific shoulder external rotation work, no face pulls, no YTWL, and minimal scapular stabilisation. This is a significant injury prevention gap." Basketball: "The shoulder preparation is inadequate. Basketball players have extreme overhead demands for shooting and rebounding — shoulder injuries are common." |
| Theme | Injury prevention |
| Scope | Exercise selection — missing exercise families |
| Severity | High |
| Frequency | Repeated (appears in 6/8 sports) |
| Root Cause | No injury prevention module exists. Exercises for shoulder stability, hamstring injury prevention, and ACL prevention are not systematically included. |
| Action | Add mandatory injury prevention exercise families per sport/role: overhead sports get shoulder external rotation + YTWL; speed/cutting sports get Nordic curls + single-leg landing progressions; collision sports get neck stability + shoulder prehab. |

---

### CF-010: Beginner program exercise stagnation
| Field | Value |
|---|---|
| Sport(s) | Soccer, Tennis, Volleyball, Basketball, Badminton |
| Role/Level | Beginner |
| Source | `sample/soccer/soccer_review_sheet.md:49`, `sample/tennis/tennis_review_sheet.md:53`, `sample/volleyball/volleyball_review_sheet.md:53`, `sample/overall_review.txt:18` |
| Evidence | Overall review: "Beginner programs repeat the same exercises (Air Squat, Wall Push-Up) for 8 weeks with only volume adjustments. A coach would expect a clear progression (e.g., Air Squat → Goblet Squat → Barbell Squat) within a block." Soccer: "The beginner programs feature the same exercises across 8 weeks, with minor volume adjustments." |
| Theme | Beginner exercise progression |
| Scope | Programming logic — progression engine |
| Severity | Medium |
| Frequency | Repeated (appears in 5/8 sports) |
| Root Cause | The progression engine only manipulates sets/reps, not exercise complexity. Within-block exercise substitution (e.g. Air Squat -> Goblet Squat at week 4) is not supported. |
| Action | Add within-block progression rules: after 4 weeks at a given exercise tier, auto-advance to the next exercise variant. Allow coaches to set progression speed. |
| Source Classification | **COACH_PROGRAMMING** (from overall_review.txt lines 1–110 coach feedback) |

---

### CF-011: Generic cueing / coaching language
| Field | Value |
|---|---|
| Sport(s) | Soccer, Tennis, Volleyball, Overall review |
| Role/Level | All |
| Source | `sample/overall_review.txt:20`, `sample/soccer/soccer_review_sheet.md:64`, `sample/tennis/tennis_review_sheet.md:47` |
| Evidence | Overall review: "Cues like 'Land soft, stick each rep' are too vague. Sport-specific cues (e.g., 'Load the hips like a spring for the approach jump') would enhance athlete education." Tennis: "A coach might expect cues like 'Absorb the landing through the hips and knees, like a spring' or 'Chest up, stay tall.'" |
| Theme | Cueing / coaching language |
| Scope | Presentation / UX — output serialization |
| Severity | Medium |
| Frequency | Repeated (appears in 5/8 sports) |
| Root Cause | Cues are static strings in the exercise metadata, not dynamically generated based on sport/role/context. No cue templating system exists. |
| Action | Build a sport-specific cue template layer. Cue text should vary by sport context (e.g. volleyball landing cue vs. basketball landing cue). Store as exercise metadata with sport context key. |
| Source Classification | **COACH_PRODUCT** (from overall_review.txt lines 1–110 coach feedback) |

---

### CF-012: Validation flag frequency & trust damage
| Field | Value |
|---|---|
| Sport(s) | Football, Rugby, Badminton, Basketball, Cricket |
| Role/Level | Intermediate / Advanced |
| Source | `sample/football/football_review_sheet.md:191`, `sample/rugby/rugby_review_sheet.md:329`, `sample/soccer/soccer_review_sheet.md:71` |
| Evidence | Football: "8 of 36 samples have validation flags indicating 'check volume load match: needs attention.'" Rugby: "12 of 48 samples have validation flags. This is more prevalent in Rugby Off-Season blueprint (0.96 credibility)." Soccer: "SOCCER_WINGER_INTERMEDIATE_A has a score of 0.89/1.0. A coach might be curious about the specific criteria." |
| Theme | Credibility score transparency / validation flag rate |
| Scope | Trust / credibility |
| Severity | High |
| Frequency | Repeated (appears in 5/8 sports) |
| Root Cause | Validation flags fire but the program is still delivered. Coach perceives this as "the system knows it's wrong but delivers it anyway." Credibility score is not broken down into sub-components. |
| Action | (a) When validation fails, do not output the program — output a corrected version or explicit warning block. (b) Publish credibility score breakdown (volume-load match, exercise appropriateness, progression logic, etc.). |

---

### CF-013: Chaotic week-to-week programming under impact response
| Field | Value |
|---|---|
| Sport(s) | Badminton, Basketball, Cricket |
| Role/Level | Intermediate |
| Source | `sample/badminton/badminton_review_sheet.md:84`, `sample/basketball/basketball_review_sheet.md:89`, `sample/cricket/cricket_review_sheet.md:29` |
| Evidence | Badminton: "The system's response to high impact (reducing families) is too aggressive. It often removes entire exercise categories (sprint, rotation, etc.) rather than intelligently reducing volume or intensity. This creates inconsistent programming and undermines adaptation." Basketball: Same verbatim. Cricket: "Week 2 'reduced families' note unexplained." |
| Theme | Impact response logic |
| Scope | Programming logic — auto-regulation engine |
| Severity | High |
| Frequency | Repeated (appears in 3/8 sports explicitly, pattern visible in more) |
| Root Cause | The auto-regulation logic has a single "reduce families" action that drops entire categories instead of proportionally reducing volume across categories. This creates the chaotic week-to-week variation coaches observed. |
| Action | Replace "reduce families" with proportional volume reduction: reduce sets across all categories by 1, rather than removing sprint/rotation entirely. Implement a smoothing function that prevents >30% week-over-week volume swings. |

---

### CF-014: No warm-up specificity
| Field | Value |
|---|---|
| Sport(s) | Football, Rugby, Volleyball |
| Role/Level | All |
| Source | `sample/football/football_review_sheet.md:198`, `sample/rugby/rugby_review_sheet.md:337` |
| Evidence | Football: "No warm-up specificity — All warm-ups are generic despite role differences." Rugby: "No warm-up specificity — All warm-ups are generic despite role differences." |
| Theme | Warm-up / movement prep |
| Scope | Programming logic — warm-up generation |
| Severity | Medium |
| Frequency | Repeated (appears in 3/8 sports explicitly) |
| Root Cause | Warm-ups are a static template not dynamically generated based on session emphasis, exercise selection, or sport demands. |
| Action | Build a session-aware warm-up generator: Raise/Activate/Potentiate structure with exercises selected based on the session's primary movement patterns and intensity zones. |

---

### CF-015: No integration with sport practice load
| Field | Value |
|---|---|
| Sport(s) | Overall review, Soccer, Tennis, Volleyball |
| Role/Level | All, especially in-season |
| Source | `sample/overall_review.txt:24`, `sample/soccer/soccer_review_sheet.md:57` |
| Evidence | Overall review: "The programs don't account for on-court training load (e.g., volleyball practice, tennis match play). This is a major blind spot." |
| Theme | Sport practice integration |
| Scope | System architecture — missing input |
| Severity | Medium |
| Frequency | Isolated (mentioned explicitly in 1 review but structurally relevant to all) |
| Root Cause | FORGE has no mechanism to accept external load inputs (practice duration/intensity, match load, GPS data). S&C volume is calculated in isolation. |
| Action | Add an external load input API; when practice load is provided, auto-reduce S&C volume proportionally (e.g. high practice load -> reduce strength volume by 1 set, reduce conditioning). |
| Source Classification | **COACH_PRODUCT** (from overall_review.txt lines 1–110 coach feedback) |

---

### CF-016: Lack of unilateral variation
| Field | Value |
|---|---|
| Sport(s) | Soccer, Tennis, Volleyball, Badminton, Basketball |
| Role/Level | All |
| Source | `sample/soccer/soccer_review_sheet.md:53`, `sample/tennis/tennis_review_sheet.md:53`, `sample/badminton/badminton_review_sheet.md:78` |
| Evidence | Soccer: "For a sport as asymmetrical as soccer, the lower-body exercises are primarily bilateral (Air Squat, Goblet Squat, RDL). More emphasis on single-leg work (lunges, single-leg RDLs) might be expected." Tennis: "Incorporating more single-leg work and rotational core/plyometric exercises would make the programs more specific." |
| Theme | Unilateral / bilateral balance |
| Scope | Exercise selection — library diversity |
| Severity | Medium |
| Frequency | Repeated (appears in 5/8 sports) |
| Root Cause | The exercise library is biased toward bilateral movements. Unilateral variants (split squats, single-leg RDLs, lunges) are under-represented in the selection pool. |
| Action | Increase unilateral exercise density in the library. Add a "unilateral ratio" target per sport: court/field sports target 40%+ unilateral work. |

---

### CF-017: All-rounder / dual-role athlete gap
| Field | Value |
|---|---|
| Sport(s) | Cricket |
| Role/Level | All-rounder |
| Source | `sample/cricket/cricket_review_sheet.md:21` |
| Evidence | "All-rounder programs are generic full-body strength programs with no emphasis on the unique demands of dual-role athletes. An all-rounder needs a balance of fast-bowler eccentric work and batter rotational power — this is not reflected." |
| Theme | Dual-role programming |
| Scope | Programming logic — role modelling |
| Severity | Medium |
| Frequency | Isolated (specific to cricket all-rounder) |
| Root Cause | The role model does not support compound roles. An all-rounder would need alternating session profiles (Session A: bowling focus, Session B: batting focus) rather than a single blended profile. |
| Action | Add a "compound role" type that alternates emphasis across sessions within the week, rather than blending into a generic average. |

---

### CF-018: Code quality and production readiness gaps
| Field | Value |
|---|---|
| Sport(s) | System-wide |
| Role/Level | N/A |
| Source | `sample/overall_review.txt:112-377` |
| Evidence | Code review report: Overall rating 7.5/10. "No authentication/authorization — critical security concern. Inconsistent import styles. Magic numbers and hardcoded values. Long functions (calculate_reps_and_intensity >40 lines). Insufficient error handling. Limited test coverage. No CI/CD pipeline. No caching strategy. Scattered configuration." |
| Theme | Code quality / production readiness |
| Scope | System architecture — engineering |
| Severity | High |
| Frequency | Isolated (1 code review) but impacts all development velocity |
| Root Cause | Engineering debt accumulated during rapid feature development. Not a coach-facing issue but blocks production deployment. |
| Action | Implement auth, CI/CD, test coverage targets, config centralization, error handling refinement. |
| Source Classification | **PLATFORM_ENGINEERING** (from overall_review.txt lines 112–377 code review) |

---

### CF-019: Credibility score opacity
| Field | Value |
|---|---|
| Sport(s) | Soccer, Tennis, Volleyball |
| Role/Level | All |
| Source | `sample/soccer/soccer_review_sheet.md:71`, `sample/tennis/tennis_review_sheet.md:57`, `sample/volleyball/volleyball_review_sheet.md:57` |
| Evidence | Soccer: "SOCCER_WINGER_INTERMEDIATE_A has a score of 0.89/1.0. A coach might be curious about the specific criteria that led to the score being lower than 1.0." Volleyball: "A coach might be curious about the specific criteria that led to the score being lower than 1.0." |
| Theme | Credibility score transparency |
| Scope | Presentation / UX |
| Severity | Low |
| Frequency | Repeated (appears in 3/8 sports) |
| Root Cause | The credibility score is output as a single number with no sub-component breakdown. Coaches cannot see whether the deduction was for volume-load mismatch, exercise appropriateness, or progression logic. |
| Action | Publish score breakdown: volume-load match / exercise appropriateness / progression logic / role-specificity alignment. Each as a sub-score with brief explanation. |

---

### CF-020: Over-aggressive category removal / "reduced families"
| Field | Value |
|---|---|
| Sport(s) | Badminton, Basketball, Cricket, Rugby |
| Role/Level | Intermediate |
| Source | `sample/badminton/badminton_review_sheet.md:84`, `sample/basketball/basketball_review_sheet.md:89`, `sample/rugby/rugby_review_sheet.md:166` |
| Evidence | Badminton: "When the system identifies 'high impact' or 'high sprint volume,' it often removes entire exercise categories (sprint, rotation, etc.) rather than intelligently reducing volume or intensity." Rugby: "[Multiple samples show] 'High exercise count; reduced families' appears repeatedly." |
| Theme | Auto-regulation granularity |
| Scope | Programming logic — session assembly |
| Severity | High |
| Frequency | Repeated (appears in 4/8 sports) |
| Root Cause | The "reduced families" logic is binary: either a category is present or it's removed. No proportional reduction mechanism exists. |
| Action | Implement proportional volume reduction: reduce sets per category rather than removing categories. Set a minimum floor (e.g. each category must have at least 1 session/week). Log the rationale. |
