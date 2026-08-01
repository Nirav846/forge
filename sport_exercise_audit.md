# Sport-Specific Exercise Coverage Audit

Generated: auto-audit

Analyzes sport-specific exercise coverage by comparing existing exercises tagged with `secondary_family=<sport>` against the movement families needed by each role in that sport.

## Coverage Summary

Sport            Roles    Existing   Needed   Families covered   Families gapped   
-----------------------------------------------------------------------------------
cricket          5        12         11       DLKD,SLKD,SLHD,Sprint,Ball,Landing,Rot,HPush,HPull,Core,Acc -                 
badminton        2        10         9        SLKD,SLHD,Sprint,Plyo,Ball,Landing,VPush,VPull,Core -                 
tennis           2        15         10       SLKD,SLHD,Sprint,Plyo,Ball,Landing,Rot,VPush,VPull,Core -                 
volleyball       5        15         12       DLKD,SLKD,SLHD,Sprint,Plyo,Landing,Rot,HPush,HPull,VPush,VPull,Core -                 
rugby            8        17         13       DLKD,DLHD,SLKD,SLHD,Sprint,Plyo,Ball,Landing,Rot,Carry,HPush,HPull,Core -                 
soccer           6        15         10       DLKD,DLHD,SLKD,SLHD,Sprint,Plyo,Ball,Landing,Carry,Core -                 
football         6        10         10       DLKD,DLHD,SLKD,SLHD,Sprint,Plyo,Ball,Landing,Carry,Core -                 
basketball       3        13         11       DLKD,DLHD,SLKD,SLHD,Sprint,Plyo,Ball,Landing,HPush,HPull,Core -                 

---
## Cricket

**Sport defaults:** force=0.5 velocity=0.5 conditioning=0.5 rotation=0.5 landing=0.5 upper_body=0.5

**Existing sport-specific exercises (12 total):**

ID             Name                                     Family     Diff   Objective
-----------------------------------------------------------------------------------
Acc-200        Shoulder Prehab (rotator cuff)           Acc        2      STAB  
AGI-106        Reactive Agility Drill                   Agility    3      POW   
Ball-200       Fielding Throw Drill                     Ball       2      POW   
Core-022       Cable Chop                               Core       3      STAB  
DLKD-200       Cricket Squat (stance)                   DLKD       3      STR   
HPull-200      Cricket Row (sustained pull)             HPull      3      STR   
HPush-200      Cricket Push (follow-through)            HPush      2      POW   
Landing-200    Pace Bowler Landing (absorb)             Landing    3      STAB  
Rot-018        Landmine Rotation                        Rot        2      POW   
SLHD-200       Single-Leg Hamstring Catch               SLHD       3      STR   
SLKD-102       Box Step-Down                            SLKD       2      STAB  
Sprint-200     Cricket Sprint Start                     Sprint     3      POW   

### Role-by-Role Gap Analysis

**Batter** - Rotational power, sprint between wickets, throwing
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
Sprint       Sprint / Acceleration        2        1          partial    Cricket Sprint Start (first-step acceleration)
Ball         Ball / Implement             1        1          full       (sufficient)                            
Rot          Rotation                     2        1          partial    Cricket-Specific Rotation (med ball / cable)
HPush        Horizontal Push              1        1          full       (sufficient)                            
HPull        Horizontal Pull              1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Rotation Cricket Stance Hold       

**Fast Bowler** - Repeated high-velocity bowling, eccentric hamstring, landing
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Lateral Lunge for Fielding              
SLHD         Single-Leg Hinge (SLHD)      3        1          gap        Single-Leg Hamstring Catch (eccentric)  
Sprint       Sprint / Acceleration        2        1          partial    Cricket Sprint Start (first-step acceleration)
Landing      Landing Mechanics            2        1          partial    Pace Bowler Landing (single-leg absorption)
Core         Core Stability               2        1          partial    Anti-Rotation Cricket Stance Hold       
Acc          Accessory / Prehab           2        1          partial    Shoulder Prehab (rotator cuff + scap)   

**Spin Bowler** - Rotation-dominant, trunk control, shoulder stability
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
Rot          Rotation                     2        1          partial    Cricket-Specific Rotation (med ball / cable)
HPush        Horizontal Push              1        1          full       (sufficient)                            
HPull        Horizontal Pull              1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Rotation Cricket Stance Hold       

**Wicketkeeper** - Agility, crouched stability, explosive diving
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
DLKD         Squat (DLKD)                 1        1          full       (sufficient)                            
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Lateral Lunge for Fielding              
Landing      Landing Mechanics            1        1          full       (sufficient)                            
Rot          Rotation                     1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Rotation Cricket Stance Hold       

**All Rounder** - Balanced batting + bowling demands
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
DLKD         Squat (DLKD)                 1        1          full       (sufficient)                            
SLKD         Single-Leg Squat (SLKD)      1        1          full       (sufficient)                            
Sprint       Sprint / Acceleration        2        1          partial    Cricket Sprint Start (first-step acceleration)
Rot          Rotation                     2        1          partial    Cricket-Specific Rotation (med ball / cable)
Core         Core Stability               2        1          partial    Anti-Rotation Cricket Stance Hold       


---
## Badminton

**Sport defaults:** force=0.4 velocity=0.6 conditioning=0.6 rotation=0.5 landing=0.5 upper_body=0.5

**Existing sport-specific exercises (10 total):**

ID             Name                                     Family     Diff   Objective
-----------------------------------------------------------------------------------
Acc-029        External Rotation (band)                 Acc        2      STAB  
Ball-201       Shuttle Cock Drill (manipulation)        Ball       2      STAB  
Core-200       Rotational Core Hold (racking)           Core       2      STAB  
Landing-201    Lunge Landing (deep recovery)            Landing    3      STAB  
Plyo-200       Net Kill Jump (explosive)                Plyo       3      POW   
SLHD-201       Split-Stance Hamstring (rear)            SLHD       3      STR   
SLKD-200       Deep Lunge Hold (rack leg)               SLKD       2      STAB  
Sprint-201     Badminton Multi-Directional Sprint       Sprint     3      POW   
VPull-200      Lat Pulldown (racket arm)                VPull      3      STR   
VPush-200      Overhead Press (smash follow)            VPush      3      POW   

### Role-by-Role Gap Analysis

**Singles** - High-volume court coverage, endurance, power
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Deep Lunge Hold (rack leg)              
SLHD         Single-Leg Hinge (SLHD)      2        1          partial    Split-Stance Hamstring (rear leg)       
Sprint       Sprint / Acceleration        3        1          gap        Badminton Multi-Directional Sprint      
Landing      Landing Mechanics            2        1          partial    Lunge Landing (deep court recovery)     
Core         Core Stability               2        1          partial    Rotational Core Hold (racking stance)   
Agility      Agility / COD                2        0          gap        Hexagonal Footwork Drill                
Cond         Conditioning                 1        0          gap        Shadow Court Movement (interval)        

**Doubles** - Net play, overhead power, lateral agility
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Deep Lunge Hold (rack leg)              
Plyo         Plyometric                   2        1          partial    Net Kill Jump (explosive overhead)      
Ball         Ball / Implement             1        1          full       (sufficient)                            
Landing      Landing Mechanics            1        1          full       (sufficient)                            
VPush        Vertical Push                1        1          full       (sufficient)                            
VPull        Vertical Pull                1        1          full       (sufficient)                            


---
## Tennis

**Sport defaults:** force=0.4 velocity=0.6 conditioning=0.6 rotation=0.6 landing=0.5 upper_body=0.5

**Existing sport-specific exercises (15 total):**

ID             Name                                     Family     Diff   Objective
-----------------------------------------------------------------------------------
ACC-100        Single-Leg Balance with Reach            Acc        2      STAB  
ACC-101        Overhead Band Pull-Apart                 Acc        2      STAB  
AGI-101        Split-Step Reaction Drill                Agility    3      POW   
AGI-102        Carioca with Sprint Exit                 Agility    3      POW   
Ball-202       Reaction Ball Catch                      Ball       2      STAB  
COND-100       Diagonal Shuttle Run                     Cond       3      COND  
Core-201       Rotational Med Ball Throw (tennis)       Core       3      POW   
Landing-202    Wide Lunge Landing (recovery)            Landing    3      STAB  
Plyo-201       Overhead Smash Jump                      Plyo       3      POW   
ROT-100        Rotational Cable Chop                    Rot        3      POW   
SLHD-202       Split-Stance RDL (racket side)           SLHD       3      STR   
SLKD-100       Lateral Lunge to Recovery                SLKD       3      STR   
Sprint-202     Tennis Split-Step to Sprint              Sprint     3      POW   
VPull-201      Wide-Grip Lat Pulldown (serve)           VPull      3      STR   
VPush-201      Overhead Press (serve follow)            VPush      3      POW   

### Role-by-Role Gap Analysis

**Singles** - High-volume court coverage, endurance, power
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Single-Leg Plant & Drive                
SLHD         Single-Leg Hinge (SLHD)      2        1          partial    Split-Stance RDL (racket side)          
Sprint       Sprint / Acceleration        2        1          partial    Tennis Split-Step to Sprint             
Landing      Landing Mechanics            2        1          partial    Wide Lunge Landing (recovery)           
Rot          Rotation                     2        1          partial    Cable Rotation (forehand/backhand)      
Core         Core Stability               2        1          partial    Rotational Med Ball Throw (tennis stance)
Agility      Agility / COD                2        2          full       (sufficient)                            

**Doubles** - Net play, overhead power, lateral agility
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
Plyo         Plyometric                   2        1          partial    Overhead Smash Jump                     
Ball         Ball / Implement             1        1          full       (sufficient)                            
Landing      Landing Mechanics            1        1          full       (sufficient)                            
VPush        Vertical Push                1        1          full       (sufficient)                            
VPull        Vertical Pull                1        1          full       (sufficient)                            


---
## Volleyball

**Sport defaults:** force=0.5 velocity=0.6 conditioning=0.5 rotation=0.4 landing=0.7 upper_body=0.6

**Existing sport-specific exercises (15 total):**

ID             Name                                     Family     Diff   Objective
-----------------------------------------------------------------------------------
AGI-100        Defensive Shuffle with Deceleration      Agility    3      POW   
Core-202       Anti-Extension Core (spiking arch)       Core       2      STAB  
DLKD-201       Deep Squat (base position)               DLKD       3      STR   
HPull-201      Seated Row (spiking prep)                HPull      3      STR   
HPush-201      Hitting Arm Deceleration (band)          HPush      2      STAB  
Landing-203    Block Landing (double-leg soft)          Landing    3      STAB  
PLYO-100       Block Jump with Stick                    Plyo       3      POW   
PLYO-101       Approach Jump                            Plyo       3      POW   
PLYO-102       Plyometric Depth Drop to Jump            Plyo       4      POW   
Rot-200        Rotational Med Ball Slam (spike)         Rot        3      POW   
SLHD-203       Single-Leg Hinge (jump prep)             SLHD       3      STR   
SLKD-201       Single-Leg Squat (block approach)        SLKD       3      STR   
Sprint-203     Volleyball Sprint (transition)           Sprint     3      POW   
VPull-202      Scapular Pull-up (arm swing)             VPull      3      STR   
VPush-202      Block Press (overhead stability)         VPush      2      STAB  

### Role-by-Role Gap Analysis

**Middle Blocker** - Vertical jumping, blocking, landing absorption
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
DLKD         Squat (DLKD)                 1        1          full       (sufficient)                            
Plyo         Plyometric                   3        3          full       (sufficient)                            
Landing      Landing Mechanics            3        1          gap        Block Landing (double-leg, soft)        
VPush        Vertical Push                1        1          full       (sufficient)                            
VPull        Vertical Pull                1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Extension Core (spiking arch)      

**Outside Hitter** - Attack jumping, arm swing power, lateral movement
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
Plyo         Plyometric                   3        3          full       (sufficient)                            
Landing      Landing Mechanics            3        1          gap        Block Landing (double-leg, soft)        
Rot          Rotation                     1        1          full       (sufficient)                            
HPush        Horizontal Push              1        1          full       (sufficient)                            
HPull        Horizontal Pull              1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Extension Core (spiking arch)      

**Opposite** - Back-court attack, blocking, rotation power
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
Plyo         Plyometric                   3        3          full       (sufficient)                            
Landing      Landing Mechanics            2        1          partial    Block Landing (double-leg, soft)        
Rot          Rotation                     2        1          partial    Rotational Med Ball Slam (spike)        
HPush        Horizontal Push              1        1          full       (sufficient)                            
HPull        Horizontal Pull              1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Extension Core (spiking arch)      

**Setter** - Hand-eye coordination, overhead control, agility
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Single-Leg Squat (block approach)       
SLHD         Single-Leg Hinge (SLHD)      1        1          full       (sufficient)                            
Rot          Rotation                     1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Extension Core (spiking arch)      

**Libero** - Defensive coverage, diving, passing accuracy
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Single-Leg Squat (block approach)       
SLHD         Single-Leg Hinge (SLHD)      1        1          full       (sufficient)                            
Sprint       Sprint / Acceleration        1        1          full       (sufficient)                            
Landing      Landing Mechanics            2        1          partial    Block Landing (double-leg, soft)        
Core         Core Stability               2        1          partial    Anti-Extension Core (spiking arch)      


---
## Rugby

**Sport defaults:** force=0.6 velocity=0.5 conditioning=0.6 rotation=0.4 landing=0.5 upper_body=0.5

**Existing sport-specific exercises (17 total):**

ID             Name                                     Family     Diff   Objective
-----------------------------------------------------------------------------------
Acc-031        Isometric Neck Hold                      Acc        3      STAB  
Acc-032        Tackle Bag Drive                         Acc        4      POW   
Acc-033        Contact Carry                            Acc        4      POW   
Ball-203       Passing Under Pressure Drill             Ball       3      POW   
Carry-200      Collision Pad Carry                      Carry      4      STR   
Core-023       Ruck Engagement                          Core       3      STR   
Core-024       Kick-Specific Core                       Core       3      STR   
DLHD-200       Rugby Deadlift (ruck prep)               DLHD       4      STR   
DLKD-014       Sled Push                                DLKD       4      STR   
HPull-202      Rugby Row (maul prep)                    HPull      4      STR   
HPush-202      Scrum Push (bench variation)             HPush      4      STR   
Landing-009    High-Ball Fielding                       Landing    3      STAB  
PLYO-105       Lineout Jump                             Plyo       3      POW   
Rot-201        Rotational Med Ball Slam (contact)       Rot        3      POW   
SLHD-204       Nordic Curl (hamstring)                  SLHD       3      STR   
SLKD-202       Single-Leg Squat (side-step)             SLKD       3      STR   
Sprint-204     Rugby Multi-Directional Sprint           Sprint     4      POW   

### Role-by-Role Gap Analysis

**Prop** - Scrummaging power, collision readiness, neck + shoulder robustness
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
DLKD         Squat (DLKD)                 2        1          partial    Scrum Squat (wide stance)               
DLHD         Hinge (DLHD)                 2        1          partial    Rugby Deadlift (ruck prep)              
Carry        Carry / Loaded Walk          1        1          full       (sufficient)                            
HPush        Horizontal Push              2        1          partial    Scrum Push / Bench Variation            
HPull        Horizontal Pull              1        1          full       (sufficient)                            
Core         Core Stability               2        2          full       (sufficient)                            
Acc          Accessory / Prehab           2        3          full       (sufficient)                            

**Hooker** - Scrum + lineout power, mobility for throws
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
DLKD         Squat (DLKD)                 2        1          partial    Scrum Squat (wide stance)               
DLHD         Hinge (DLHD)                 2        1          partial    Rugby Deadlift (ruck prep)              
Landing      Landing Mechanics            1        1          full       (sufficient)                            
Carry        Carry / Loaded Walk          1        1          full       (sufficient)                            
HPush        Horizontal Push              2        1          partial    Scrum Push / Bench Variation            
Core         Core Stability               2        2          full       (sufficient)                            
Acc          Accessory / Prehab           2        3          full       (sufficient)                            

**Lock** - Lineout jumping, collision force, scrum power
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
DLKD         Squat (DLKD)                 2        1          partial    Scrum Squat (wide stance)               
DLHD         Hinge (DLHD)                 2        1          partial    Rugby Deadlift (ruck prep)              
Plyo         Plyometric                   2        1          partial    Rugby Box Jump (collision prep)         
Landing      Landing Mechanics            2        1          partial    High-Ball Landing (contested)           
HPush        Horizontal Push              1        1          full       (sufficient)                            
Core         Core Stability               2        2          full       (sufficient)                            
Acc          Accessory / Prehab           2        3          full       (sufficient)                            

**Back Row** - All-round athleticism, breakdown work, link play
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
DLKD         Squat (DLKD)                 2        1          partial    Scrum Squat (wide stance)               
DLHD         Hinge (DLHD)                 2        1          partial    Rugby Deadlift (ruck prep)              
Sprint       Sprint / Acceleration        2        1          partial    Rugby Multi-Directional Sprint          
Carry        Carry / Loaded Walk          1        1          full       (sufficient)                            
Core         Core Stability               2        2          full       (sufficient)                            
Acc          Accessory / Prehab           2        3          full       (sufficient)                            

**Scrum Half** - Agility, passing accuracy, quick decision-making
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Single-Leg Squat (side-step)            
SLHD         Single-Leg Hinge (SLHD)      1        1          full       (sufficient)                            
Sprint       Sprint / Acceleration        2        1          partial    Rugby Multi-Directional Sprint          
Ball         Ball / Implement             1        1          full       (sufficient)                            
Core         Core Stability               2        2          full       (sufficient)                            
Agility      Agility / COD                2        0          gap        Side-Step / Evasion Drill               

**Fly Half** - Distributor, kicking, evasion, game management
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Single-Leg Squat (side-step)            
Sprint       Sprint / Acceleration        2        1          partial    Rugby Multi-Directional Sprint          
Ball         Ball / Implement             2        1          partial    Passing Under Pressure Drill            
Rot          Rotation                     1        1          full       (sufficient)                            
Core         Core Stability               2        2          full       (sufficient)                            
Agility      Agility / COD                2        0          gap        Side-Step / Evasion Drill               

**Centre** - Midfield collisions, line-breaking power, passing
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
DLKD         Squat (DLKD)                 1        1          full       (sufficient)                            
Sprint       Sprint / Acceleration        2        1          partial    Rugby Multi-Directional Sprint          
Plyo         Plyometric                   1        1          full       (sufficient)                            
Ball         Ball / Implement             1        1          full       (sufficient)                            
Core         Core Stability               2        2          full       (sufficient)                            
Acc          Accessory / Prehab           2        3          full       (sufficient)                            

**Back Three** - Open-field running, high-ball catching, finishing
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
Sprint       Sprint / Acceleration        3        1          gap        Rugby Multi-Directional Sprint          
Plyo         Plyometric                   2        1          partial    Rugby Box Jump (collision prep)         
Ball         Ball / Implement             2        1          partial    Passing Under Pressure Drill            
Landing      Landing Mechanics            2        1          partial    High-Ball Landing (contested)           
Core         Core Stability               2        2          full       (sufficient)                            
Agility      Agility / COD                2        0          gap        Side-Step / Evasion Drill               


---
## Soccer

**Sport defaults:** force=0.5 velocity=0.6 conditioning=0.7 rotation=0.3 landing=0.4 upper_body=0.4

**Existing sport-specific exercises (15 total):**

ID             Name                                     Family     Diff   Objective
-----------------------------------------------------------------------------------
Acc-034        Band-Resisted Distribution               Acc        2      STR   
AGI-103        COD Drill                                Agility    3      POW   
AGI-104        Lateral Shuffle to Sprint                Agility    3      POW   
AGI-107        5-10-5 Shuttle                           Agility    3      POW   
Ball-204       Passing / Crossing Accuracy Drill        Ball       2      POW   
Carry-201      Loaded Walk (shield carry)               Carry      3      STR   
Core-203       Anti-Rotation (kicking stability)        Core       2      STAB  
DLHD-100       Kettlebell Swing                         DLHD       3      POW   
DLKD-202       Single-Leg Squat (kicking leg)           DLKD       3      STR   
LANDING-100    Single-Leg Landing Progression           Landing    3      STAB  
Landing-010    Lateral Dive Pattern                     Landing    3      STAB  
PLYO-106       Reactive Box Jump                        Plyo       3      POW   
SLHD-205       Single-Leg RDL (kicking leg)             SLHD       3      STR   
SLKD-203       Single-Leg Squat (plant leg)             SLKD       3      STR   
SPRINT-100     Repeated Sprint Ability (RSA)            Sprint     4      COND  

### Role-by-Role Gap Analysis

**Goalkeeper** - Diving, explosive lateral movement, landing
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Single-Leg Squat (plant leg)            
SLHD         Single-Leg Hinge (SLHD)      2        1          partial    Single-Leg RDL (kicking leg)            
Plyo         Plyometric                   2        1          partial    Soccer Box Jump (heading prep)          
Ball         Ball / Implement             1        1          full       (sufficient)                            
Landing      Landing Mechanics            3        2          partial    Single-Leg Landing (shot follow-through)
Core         Core Stability               2        1          partial    Anti-Rotation (kicking stability)       

**Centre Back** - Aerial duels, physical defending, heading
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
DLKD         Squat (DLKD)                 2        1          partial    Single-Leg Squat (kicking leg)          
DLHD         Hinge (DLHD)                 2        1          partial    Soccer Deadlift (kicking hinge)         
Sprint       Sprint / Acceleration        2        1          partial    Soccer Acceleration (first 5m)          
Landing      Landing Mechanics            1        2          full       (sufficient)                            
Carry        Carry / Loaded Walk          1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Rotation (kicking stability)       
Acc          Accessory / Prehab           2        1          partial    Hip Adductor Prehab                     

**Fullback** - Tactical speed, recovery running, crossing
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Single-Leg Squat (plant leg)            
SLHD         Single-Leg Hinge (SLHD)      2        1          partial    Single-Leg RDL (kicking leg)            
Sprint       Sprint / Acceleration        3        1          gap        Soccer Acceleration (first 5m)          
Landing      Landing Mechanics            1        2          full       (sufficient)                            
Carry        Carry / Loaded Walk          1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Rotation (kicking stability)       
Agility      Agility / COD                2        3          full       (sufficient)                            

**Midfielder** - Endurance, change of direction, passing
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Single-Leg Squat (plant leg)            
SLHD         Single-Leg Hinge (SLHD)      2        1          partial    Single-Leg RDL (kicking leg)            
Sprint       Sprint / Acceleration        2        1          partial    Soccer Acceleration (first 5m)          
Carry        Carry / Loaded Walk          1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Rotation (kicking stability)       
Agility      Agility / COD                2        3          full       (sufficient)                            
Cond         Conditioning                 1        0          gap        Repeated Sprint Ability (RSA)           

**Winger** - Pure speed, finishing, 1v1 attacking
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
Sprint       Sprint / Acceleration        3        1          gap        Soccer Acceleration (first 5m)          
Plyo         Plyometric                   1        1          full       (sufficient)                            
Ball         Ball / Implement             2        1          partial    Passing / Crossing Accuracy Drill       
Landing      Landing Mechanics            1        2          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Rotation (kicking stability)       
Agility      Agility / COD                2        3          full       (sufficient)                            

**Striker** - Finishing, explosive acceleration, hold-up play
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
DLKD         Squat (DLKD)                 1        1          full       (sufficient)                            
Sprint       Sprint / Acceleration        3        1          gap        Soccer Acceleration (first 5m)          
Plyo         Plyometric                   2        1          partial    Soccer Box Jump (heading prep)          
Ball         Ball / Implement             2        1          partial    Passing / Crossing Accuracy Drill       
Landing      Landing Mechanics            1        2          full       (sufficient)                            
Agility      Agility / COD                2        3          full       (sufficient)                            


---
## Football

**Sport defaults:** force=0.5 velocity=0.6 conditioning=0.7 rotation=0.3 landing=0.4 upper_body=0.4

**Existing sport-specific exercises (10 total):**

ID             Name                                     Family     Diff   Objective
-----------------------------------------------------------------------------------
Ball-205       Passing / Crossing Accuracy Drill        Ball       2      POW   
Carry-202      Loaded Walk (shield carry)               Carry      3      STR   
Core-204       Anti-Rotation (kicking stability)        Core       2      STAB  
DLHD-201       Football Deadlift (kicking hinge)        DLHD       4      STR   
DLKD-203       Football Squat (explosive stance)        DLKD       3      STR   
Landing-204    Single-Leg Landing (shot follow)         Landing    3      STAB  
Plyo-202       Football Box Jump (heading prep)         Plyo       3      POW   
SLHD-206       Single-Leg RDL (kicking leg)             SLHD       3      STR   
SLKD-204       Single-Leg Squat (cutting leg)           SLKD       3      STR   
Sprint-205     Football Acceleration (first 5m)         Sprint     3      POW   

### Role-by-Role Gap Analysis

**Goalkeeper** - Diving, explosive lateral movement, landing
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Single-Leg Squat (plant leg)            
SLHD         Single-Leg Hinge (SLHD)      2        1          partial    Single-Leg RDL (kicking leg)            
Plyo         Plyometric                   2        1          partial    Football Box Jump (heading prep)        
Ball         Ball / Implement             1        1          full       (sufficient)                            
Landing      Landing Mechanics            3        1          gap        Single-Leg Landing (shot follow-through)
Core         Core Stability               2        1          partial    Anti-Rotation (kicking stability)       

**Centre Back** - Aerial duels, physical defending, heading
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
DLKD         Squat (DLKD)                 2        1          partial    Single-Leg Squat (kicking leg)          
DLHD         Hinge (DLHD)                 2        1          partial    Football Deadlift (kicking hinge)       
Sprint       Sprint / Acceleration        2        1          partial    Football Acceleration (first 5m)        
Landing      Landing Mechanics            1        1          full       (sufficient)                            
Carry        Carry / Loaded Walk          1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Rotation (kicking stability)       
Acc          Accessory / Prehab           2        0          gap        Hip Adductor Prehab                     

**Fullback** - Tactical speed, recovery running, crossing
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Single-Leg Squat (plant leg)            
SLHD         Single-Leg Hinge (SLHD)      2        1          partial    Single-Leg RDL (kicking leg)            
Sprint       Sprint / Acceleration        3        1          gap        Football Acceleration (first 5m)        
Landing      Landing Mechanics            1        1          full       (sufficient)                            
Carry        Carry / Loaded Walk          1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Rotation (kicking stability)       
Agility      Agility / COD                2        0          gap        Ladder / COD Circuit                    

**Midfielder** - Endurance, change of direction, passing
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Single-Leg Squat (plant leg)            
SLHD         Single-Leg Hinge (SLHD)      2        1          partial    Single-Leg RDL (kicking leg)            
Sprint       Sprint / Acceleration        2        1          partial    Football Acceleration (first 5m)        
Carry        Carry / Loaded Walk          1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Rotation (kicking stability)       
Agility      Agility / COD                2        0          gap        Ladder / COD Circuit                    
Cond         Conditioning                 1        0          gap        Repeated Sprint Ability (RSA)           

**Winger** - Pure speed, finishing, 1v1 attacking
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
Sprint       Sprint / Acceleration        3        1          gap        Football Acceleration (first 5m)        
Plyo         Plyometric                   1        1          full       (sufficient)                            
Ball         Ball / Implement             2        1          partial    Passing / Crossing Accuracy Drill       
Landing      Landing Mechanics            1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Rotation (kicking stability)       
Agility      Agility / COD                2        0          gap        Ladder / COD Circuit                    

**Striker** - Finishing, explosive acceleration, hold-up play
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
DLKD         Squat (DLKD)                 1        1          full       (sufficient)                            
Sprint       Sprint / Acceleration        3        1          gap        Football Acceleration (first 5m)        
Plyo         Plyometric                   2        1          partial    Football Box Jump (heading prep)        
Ball         Ball / Implement             2        1          partial    Passing / Crossing Accuracy Drill       
Landing      Landing Mechanics            1        1          full       (sufficient)                            
Agility      Agility / COD                2        0          gap        Ladder / COD Circuit                    


---
## Basketball

**Sport defaults:** force=0.5 velocity=0.6 conditioning=0.6 rotation=0.4 landing=0.6 upper_body=0.5

**Existing sport-specific exercises (13 total):**

ID             Name                                     Family     Diff   Objective
-----------------------------------------------------------------------------------
Acc-030        Collision Pad Drive                      Acc        4      POW   
Ball-206       Dribbling Under Pressure Drill           Ball       2      STAB  
Core-205       Anti-Rotation (contact finish)           Core       2      STAB  
DLHD-202       Deadlift (post-play strength)            DLHD       4      STR   
DLKD-204       Basketball Squat (defensive stance)      DLKD       3      STR   
HPull-203      Basketball Row (rebound prep)            HPull      3      STR   
HPush-203      Pass Push (chest pass strength)          HPush      2      POW   
Landing-205    Rebound Landing (absorb+explode)         Landing    3      POW   
PLYO-103       Vertical Jump (approach)                 Plyo       3      POW   
PLYO-104       Single-Leg Depth Jump                    Plyo       4      POW   
SLHD-207       Single-Leg Hinge (jump prep)             SLHD       3      STR   
SLKD-205       Single-Leg Squat (cutting leg)           SLKD       3      STR   
Sprint-030     Band Resisted Sprint                     Sprint     3      POW   

### Role-by-Role Gap Analysis

**Guard** - Ball handling, agility, perimeter shooting
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
SLKD         Single-Leg Squat (SLKD)      2        1          partial    Single-Leg Squat (cutting leg)          
SLHD         Single-Leg Hinge (SLHD)      2        1          partial    Single-Leg Hinge (jump prep)            
Sprint       Sprint / Acceleration        3        1          gap        Basketball Sprint (transition)          
Plyo         Plyometric                   2        2          full       (sufficient)                            
Ball         Ball / Implement             2        1          partial    Dribbling Under Pressure Drill          
Core         Core Stability               2        1          partial    Anti-Rotation (contact finish)          

**Wing** - Slashing drives, perimeter D, lateral quickness
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
Sprint       Sprint / Acceleration        2        1          partial    Basketball Sprint (transition)          
Plyo         Plyometric                   3        2          partial    Basketball Vertical Jump (max effort)   
Ball         Ball / Implement             2        1          partial    Dribbling Under Pressure Drill          
Landing      Landing Mechanics            2        1          partial    Rebound Landing (absorb + explode)      
HPush        Horizontal Push              1        1          full       (sufficient)                            
HPull        Horizontal Pull              1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Rotation (contact finish)          

**Big** - Post play, rebounding, verticality, interior D
Family       Label                        Need     Existing   Status     Suggested Exercise                      
-----------------------------------------------------------------------------------------------------------------
DLKD         Squat (DLKD)                 2        1          partial    Deep Squat (defensive stance)           
DLHD         Hinge (DLHD)                 2        1          partial    Deadlift (post-play strength)           
Plyo         Plyometric                   3        2          partial    Basketball Vertical Jump (max effort)   
Landing      Landing Mechanics            3        1          gap        Rebound Landing (absorb + explode)      
HPush        Horizontal Push              1        1          full       (sufficient)                            
HPull        Horizontal Pull              1        1          full       (sufficient)                            
Core         Core Stability               2        1          partial    Anti-Rotation (contact finish)          

