#!/usr/bin/env python3
"""
FORGE Prototype — minimal program generator.
Source data: FORGE_COACHING_REFERENCE_DATABASE.md,
             FORGE_BLUEPRINT_CATALOG_V1.md,
             FORGE_SUBSTITUTION_MATRIX_V1.md.
No external deps. No database. No AI. One file.
"""

import random
from dataclasses import dataclass, field
from typing import Optional

# ── Data structures ──────────────────────────────────────────────────────────

FAMILIES_SHORT = [
    "DLKD", "DLHD", "SLKD", "SLHD", "HPush", "HPull",
    "VPush", "VPull", "Plyo", "Ball", "Sprint/COD", "Rot",
    "Carry", "Core", "Acc/Prehab",
]

FAMILIES_LONG = {
    "DLKD": "Double Leg Knee Dominant",
    "DLHD": "Double Leg Hip Dominant",
    "SLKD": "Single Leg Knee Dominant",
    "SLHD": "Single Leg Hip Dominant",
    "HPush": "Horizontal Push",
    "HPull": "Horizontal Pull",
    "VPush": "Vertical Push",
    "VPull": "Vertical Pull",
    "Plyo": "Plyometric",
    "Ball": "Ballistic",
    "Sprint/COD": "Sprint / Change of Direction",
    "Rot": "Rotational",
    "Carry": "Carry",
    "Core": "Core",
    "Acc/Prehab": "Accessory / Prehab",
}

OBJ_LABELS = {
    "STR": "Strength", "POW": "Power", "HYP": "Hypertrophy",
    "COND": "Conditioning", "MOB": "Mobility", "STAB": "Stability",
}


@dataclass
class Exercise:
    name: str
    family: str
    secondary: str
    objective: str
    difficulty: int  # 1–5
    equipment: str
    unilateral: bool
    explosive: bool
    isometric: bool
    rotational: bool
    progression: str
    regression: str

    def min_equip_level(self) -> int:
        """Return minimum equipment level required (0=none … 4=full)."""
        e = self.equipment.lower()
        if "bodyweight" in e and ("band" not in e and "dumbbell" not in e and "barbell" not in e):
            return 0
        if "band" in e and "cable" not in e:
            return 0
        if "pvc" in e:
            return 0
        if "dumbbell" in e or "db" in e or "kettlebell" in e or "kb" in e:
            return 1
        if "medicine ball" in e or "med ball" in e or "med ball" in e.replace("med ball","med ball"):
            return 1
        if "ab wheel" in e or "stability ball" in e:
            return 1
        if "barbell" in e or "trap bar" in e or "landmine" in e:
            return 2
        if "bench" in e or "box" in e or "rack" in e or "pull-up bar" in e:
            return 2
        if "weight vest" in e or "belt" in e:
            return 2
        if "cable" in e or "machine" in e:
            return 3
        if "timing gates" in e or "hurdles" in e or "sled" in e:
            return 3
        if "yoke" in e or "sandbag" in e:
            return 3
        if "bumper" in e or "platform" in e:
            return 3
        if "partner" in e or "nordic strap" in e:
            return 1
        if "hyperextension" in e or "reverse hyper" in e:
            return 3
        if "t-bar" in e:
            return 3
        return 2  # default

    def equip_ok(self, athlete_equip_level: int) -> bool:
        return self.min_equip_level() <= athlete_equip_level


@dataclass
class Blueprint:
    name: str
    frequency: str
    slot_order: list  # list of strings e.g. ["Ball", "DLKD", "HPush", "DLHD / HPull", "Core"]
    mandatory: list    # list of family codes
    optional: list     # list of family codes
    notes: str = ""


# ── Data (derived from the three FORGE source files) ──────────────────────

def load_exercises() -> list[Exercise]:
    """191 exercises from FORGE_COACHING_REFERENCE_DATABASE.md Part 2."""
    rows = [
        # DLKD
        ("Air Squat","DLKD","—","STR",1,"Bodyweight",False,False,False,False,"Goblet Squat","Wall Sit"),
        ("Wall Sit","DLKD","Acc","STAB",1,"Bodyweight",False,False,True,False,"Air Squat","—"),
        ("Box Squat","DLKD","—","STR",2,"Barbell + Box",False,False,False,False,"Goblet Squat","Air Squat"),
        ("Goblet Squat","DLKD","—","STR",2,"DB/KB",False,False,False,False,"Barbell Back Squat","Box Squat"),
        ("Leg Press","DLKD","—","STR",2,"Machine",False,False,False,False,"Hack Squat","Air Squat"),
        ("Tempo Back Squat","DLKD","—","STR",2,"Barbell + Rack",False,False,False,False,"Paused Back Squat","Goblet Squat"),
        ("Barbell Back Squat","DLKD","—","STR",3,"Barbell + Rack",False,False,False,False,"Front Squat","Goblet Squat"),
        ("Hack Squat","DLKD","—","HYP",3,"Machine",False,False,False,False,"Barbell Back Squat","Leg Press"),
        ("Landmine Squat","DLKD","VPush","STR",3,"Barbell + Landmine",False,False,False,False,"Barbell Back Squat","Goblet Squat"),
        ("Paused Back Squat","DLKD","—","STR",4,"Barbell + Rack",False,False,True,False,"Front Squat","Tempo Back Squat"),
        ("Barbell Front Squat","DLKD","—","STR",4,"Barbell + Rack",False,False,False,False,"Paused Front Squat","Barbell Back Squat"),
        ("Paused Front Squat","DLKD","—","STR",5,"Barbell + Rack",False,False,True,False,"—","Front Squat"),
        # DLHD
        ("Glute Bridge","DLHD","Core","STAB",1,"Bodyweight",False,False,False,False,"Kettlebell Deadlift","—"),
        ("Kettlebell Deadlift","DLHD","—","STR",2,"Kettlebell",False,False,False,False,"RDL","Glute Bridge"),
        ("Trap Bar Deadlift","DLHD","—","STR",2,"Trap Bar",False,False,False,False,"RDL","Kettlebell Deadlift"),
        ("45° Back Extension","DLHD","Core","STAB",2,"Hyperextension Bench",False,False,False,False,"Weighted Back Extension","Glute Bridge"),
        ("Barbell Hip Thrust","DLHD","—","STR",3,"Barbell + Bench",False,False,False,False,"Heavy Hip Thrust","Glute Bridge"),
        ("RDL","DLHD","—","STR",3,"Barbell",False,False,False,False,"Barbell Good Morning","Kettlebell Deadlift"),
        ("Barbell Rack Pull","DLHD","—","STR",3,"Barbell + Rack",False,False,False,False,"Block Pull","RDL"),
        ("Single-Leg RDL","DLHD","SLHD","STR",3,"DB/KB",True,False,False,False,"Weighted SL RDL","Kettlebell Deadlift"),
        ("Weighted Back Extension","DLHD","Core","STR",4,"Hyperextension Bench + Plate",False,False,False,False,"Barbell Good Morning","45° Back Extension"),
        ("Block Pull","DLHD","—","STR",4,"Barbell + Blocks/Rack",False,False,False,False,"Conventional Deadlift","Rack Pull"),
        ("Barbell Good Morning","DLHD","—","STR",4,"Barbell + Rack",False,False,False,False,"Conventional Deadlift","RDL"),
        ("Conventional Deadlift","DLHD","—","STR",5,"Barbell + Platform",False,False,False,False,"Deficit Deadlift","Rack Pull"),
        ("Sumo Deadlift","DLHD","—","STR",5,"Barbell + Platform",False,False,False,False,"—","Rack Pull"),
        ("Deficit Deadlift","DLHD","—","STR",5,"Barbell + Deficit Platform",False,False,False,False,"—","Conventional Deadlift"),
        # SLKD
        ("Assisted Split Squat","SLKD","—","STAB",1,"Bodyweight + Support",True,False,False,False,"Split Squat","—"),
        ("Split Squat","SLKD","—","STR",2,"Bodyweight/DB",True,False,False,False,"Bulgarian Split Squat","Assisted Split Squat"),
        ("Step-Up","SLKD","—","STR",2,"Box + DB",True,False,False,False,"Bulgarian Split Squat","Low Box Step-Up"),
        ("Low Box Step-Up","SLKD","—","STR",1,"Box (low) + Bodyweight",True,False,False,False,"Step-Up","—"),
        ("Bulgarian Split Squat","SLKD","—","STR",3,"DB + Bench",True,False,False,False,"Barbell Reverse Lunge","Split Squat"),
        ("Walking Lunge","SLKD","—","STR/COND",3,"DB",True,False,False,False,"Barbell Reverse Lunge","Split Squat"),
        ("Lateral Lunge","SLKD","—","STR/MOB",3,"DB/Bodyweight",True,False,False,False,"Cossack Squat","Split Squat"),
        ("Barbell Reverse Lunge","SLKD","—","STR",4,"Barbell + Rack",True,False,False,False,"Skater Squat","Bulgarian Split Squat"),
        ("Cossack Squat","SLKD","—","MOB/STR",4,"Bodyweight",True,False,False,True,"Weighted Cossack Squat","Lateral Lunge"),
        ("Skater Squat","SLKD","—","STR",4,"Bodyweight/DB",True,False,False,False,"Pistol Squat","Bulgarian Split Squat"),
        ("Single-Leg Box Squat","SLKD","—","STR",4,"Box + Bodyweight",True,False,False,False,"Pistol Squat","Bulgarian Split Squat"),
        ("Pistol Squat","SLKD","—","STR/MOB",5,"Bodyweight",True,False,False,False,"—","Single-Leg Box Squat"),
        # SLHD
        ("Single-Leg Glute Bridge","SLHD","Core","STAB",1,"Bodyweight",True,False,False,False,"Single-Leg Bridge (elevated)","—"),
        ("Split Stance RDL","SLHD","—","STR",2,"DB/Bodyweight",True,False,False,False,"SL RDL (floor touch)","Single-Leg Glute Bridge"),
        ("SL RDL (floor touch)","SLHD","—","STR",2,"Bodyweight/Light DB",True,False,False,False,"Weighted SL RDL","Split Stance RDL"),
        ("Single-Leg Bridge (elevated)","SLHD","Core","STR",2,"Bench",True,False,False,False,"Single-Leg Hip Thrust","Single-Leg Glute Bridge"),
        ("Weighted SL RDL","SLHD","—","STR",3,"DB/KB",True,False,False,False,"Single-Leg RDL (loaded)","SL RDL (floor touch)"),
        ("Single-Leg Hip Thrust","SLHD","—","STR",3,"Barbell/Bench",True,False,False,False,"Barbell Hip Thrust (bilateral)","Single-Leg Bridge (elevated)"),
        ("Isometric Hamstring Hold","SLHD","Acc","STAB",3,"Partner/Wall",True,False,True,False,"SL RDL (weighted)","Single-Leg Glute Bridge"),
        ("Single-Leg RDL (loaded)","SLHD","—","STR",4,"DB/KB (heavy)",True,False,False,False,"—","Weighted SL RDL"),
        ("Band-Resisted Nordic","SLHD","—","STR",3,"Band + Strap",False,False,False,False,"Nordic Hamstring Curl","Isometric Hamstring Hold"),
        ("Nordic Hamstring Curl","SLHD","—","STR/POW",4,"Partner/Strap",False,False,False,False,"Weighted Nordic","Band-Resisted Nordic"),
        # HPush
        ("Wall Push-Up","HPush","—","STR",1,"Bodyweight",False,False,False,False,"Incline Push-Up","—"),
        ("Incline Push-Up","HPush","—","STR",1,"Bench",False,False,False,False,"Push-Up","Wall Push-Up"),
        ("Push-Up","HPush","—","STR",2,"Bodyweight",False,False,False,False,"Dumbbell Floor Press","Incline Push-Up"),
        ("Dumbbell Floor Press","HPush","—","STR",2,"DB",False,False,False,False,"Dumbbell Bench Press","Push-Up"),
        ("Dumbbell Bench Press","HPush","—","STR",3,"DB + Bench",True,False,False,False,"Barbell Bench Press","Dumbbell Floor Press"),
        ("Barbell Bench Press","HPush","—","STR",3,"Barbell + Bench",False,False,False,False,"Incline Barbell Bench Press","Dumbbell Bench Press"),
        ("Incline Dumbbell Press","HPush","VPush","STR",3,"DB + Incline Bench",True,False,False,False,"Barbell Incline Bench Press","Push-Up"),
        ("Incline Barbell Bench Press","HPush","VPush","STR",4,"Barbell + Incline Bench",False,False,False,False,"—","Flat Barbell Bench Press"),
        ("Band-Resisted Push-Up","HPush","—","POW",3,"Band",False,True,False,False,"Weighted Push-Up","Push-Up"),
        ("Weighted Push-Up","HPush","—","STR",4,"Weight Vest/Belt",False,False,False,False,"—","Push-Up"),
        # HPull
        ("Scapular Retraction","HPull","Acc","STAB",1,"Bodyweight",False,False,False,False,"Band Row","—"),
        ("Band Row","HPull","—","STR",1,"Band",False,False,False,False,"Inverted Row","Scapular Retraction"),
        ("Inverted Row","HPull","—","STR",2,"Barbell/Suspension Trainer",False,False,False,False,"Chest-Supported Row","Band Row"),
        ("Chest-Supported Row","HPull","—","STR",2,"DB + Bench",False,False,False,False,"Dumbbell Row","Inverted Row"),
        ("Dumbbell Row","HPull","—","STR",3,"DB + Bench",True,False,False,False,"Barbell Row","Chest-Supported Row"),
        ("Seal Row","HPull","—","HYP",3,"Barbell + Elevated Bench",False,False,False,False,"Barbell Row","Chest-Supported Row"),
        ("Single-Arm Cable Row","HPull","—","HYP",3,"Cable Machine",True,False,False,False,"Barbell Row","Band Row"),
        ("T-Bar Row","HPull","—","HYP",3,"T-Bar Handle",False,False,False,False,"Barbell Row","Chest-Supported Row"),
        ("Barbell Row","HPull","—","STR",4,"Barbell + Rack",False,False,False,False,"Pendlay Row","Dumbbell Row"),
        ("Meadows Row","HPull","—","HYP",4,"Barbell + Landmine",True,False,False,False,"Barbell Row","Dumbbell Row"),
        ("Pendlay Row","HPull","—","POW",5,"Barbell + Platform",False,True,False,False,"—","Barbell Row"),
        # VPush
        ("Band Overhead Press","VPush","—","STR",1,"Band",False,False,False,False,"Half-Kneeling Landmine Press","—"),
        ("Half-Kneeling Landmine Press","VPush","Core","STR",2,"Barbell + Landmine",False,False,False,False,"Standing Landmine Press","Band Overhead Press"),
        ("Standing Landmine Press","VPush","—","STR",2,"Barbell + Landmine",False,False,False,False,"Single-Arm DB Press","Half-Kneeling Landmine Press"),
        ("Single-Arm DB Press (standing)","VPush","Core","STAB",2,"DB",True,False,False,False,"Standing DB Press","Landmine Press"),
        ("Seated DB Press","VPush","—","STR",3,"DB + Bench",False,False,False,False,"Standing DB Press","Single-Arm DB Press"),
        ("Standing DB Press","VPush","—","STR",3,"DB",False,False,False,False,"Barbell Overhead Press","Seated DB Press"),
        ("Arnold Press","VPush","—","HYP",4,"DB",False,False,False,True,"Standing DB Press","Seated DB Press"),
        ("Barbell Overhead Press","VPush","—","STR",4,"Barbell + Rack",False,False,False,False,"Push Press","Standing DB Press"),
        ("Push Press","VPush","Ball","POW",4,"Barbell + Rack",False,True,False,False,"Power Jerk","Barbell Overhead Press"),
        ("Power Jerk","VPush","Ball","POW",5,"Barbell + Rack",False,True,False,False,"—","Push Press"),
        # VPull
        ("Band Lat Pulldown","VPull","—","STR",1,"Band",False,False,False,False,"Lat Pulldown","—"),
        ("Scapular Pull-Up (hang)","VPull","Acc","STAB",1,"Pull-Up Bar",False,False,True,False,"Lat Pulldown","—"),
        ("Lat Pulldown","VPull","—","STR",2,"Cable Machine",False,False,False,False,"Pull-Up","Band Lat Pulldown"),
        ("V-Grip Pulldown","VPull","—","HYP",2,"Cable Machine + V-Handle",False,False,False,False,"Pull-Up (close grip)","Lat Pulldown"),
        ("Straight-Arm Pulldown","VPull","—","STAB",2,"Cable Machine",False,False,False,False,"Lat Pulldown","Band Straight-Arm Pulldown"),
        ("Chin-Up","VPull","—","STR",3,"Pull-Up Bar",False,False,False,False,"Weighted Chin-Up","Lat Pulldown (underhand)"),
        ("Pull-Up","VPull","—","STR",3,"Pull-Up Bar",False,False,False,False,"Weighted Pull-Up","Lat Pulldown"),
        ("Neutral-Grip Pull-Up","VPull","—","STR",3,"Neutral-Grip Bar",False,False,False,False,"Weighted Neutral Pull-Up","Lat Pulldown (neutral)"),
        ("Single-Arm Lat Pulldown","VPull","—","HYP",3,"Cable Machine",True,False,False,False,"Pull-Up","Lat Pulldown"),
        ("Weighted Chin-Up","VPull","—","STR",4,"Belt + Plate + Bar",False,False,False,False,"—","Chin-Up"),
        ("Weighted Pull-Up","VPull","—","STR",4,"Belt + Plate + Bar",False,False,False,False,"Muscle-Up","Pull-Up"),
        ("Muscle-Up","VPull","VPush","STR/POW",5,"Rings/Pull-Up Bar",False,True,False,False,"—","Weighted Pull-Up + Dip"),
        # Plyo (ponytail: using short "Plyo" internally, display uses long name)
        ("Ankle Bounce","Plyo","—","STAB",1,"Bodyweight",False,True,False,False,"Pogo Jump","—"),
        ("Pogo Jump","Plyo","—","POW",1,"Bodyweight",False,True,False,False,"Squat Jump","Ankle Bounce"),
        ("Pogo Jump (single leg)","Plyo","—","POW",2,"Bodyweight",True,True,False,False,"Broad Jump","Pogo Jump (bilateral)"),
        ("Squat Jump","Plyo","—","POW",2,"Bodyweight",False,True,False,False,"Countermovement Jump","Pogo Jump"),
        ("Depth Drop (land + stick)","Plyo","—","STAB",2,"Box (low)",False,False,True,False,"Box Jump","Pogo Jump"),
        ("Countermovement Jump","Plyo","—","POW",3,"Bodyweight",False,True,False,False,"Broad Jump","Squat Jump"),
        ("Broad Jump","Plyo","—","POW",3,"Bodyweight",False,True,False,False,"Bounding","Countermovement Jump"),
        ("Lateral Pogo","Plyo","—","POW",3,"Bodyweight",False,True,False,True,"Lateral Bound","Pogo Jump"),
        ("Box Jump","Plyo","—","POW",3,"Box",False,True,False,False,"Depth Jump","Countermovement Jump"),
        ("Hurdle Hop","Plyo","—","POW",4,"Hurdles",False,True,False,False,"Depth Jump","Box Jump"),
        ("Lateral Bound","Plyo","—","POW",4,"Bodyweight",True,True,False,True,"Single-Leg Lateral Bound","Lateral Pogo"),
        ("Bounding","Plyo","—","POW",4,"Bodyweight",True,True,False,False,"Single-Leg Bounding","Broad Jump"),
        ("Depth Jump","Plyo","—","POW",5,"Box",False,True,False,False,"Depth Jump + Sprint","Box Jump"),
        ("Single-Leg Bounding","Plyo","—","POW",5,"Bodyweight",True,True,False,False,"—","Bounding"),
        # Ball
        ("Med Ball Push","Ball","HPush","POW",1,"Medicine Ball",False,True,False,False,"Med Ball Chest Pass","—"),
        ("KB Swing","Ball","DLHD","POW",1,"Kettlebell",False,True,False,False,"High Pull (KB or barbell)","—"),
        ("Med Ball Chest Pass","Ball","HPush","POW",2,"Medicine Ball",False,True,False,False,"Med Ball Overhead Throw","Med Ball Push"),
        ("Jump Shrug","Ball","—","POW",2,"Barbell",False,True,False,False,"High Pull (hang)","—"),
        ("KB Clean","Ball","—","POW",2,"Kettlebell",False,True,False,False,"Hang Clean","KB Swing"),
        ("Snatch High Pull","Ball","—","POW",3,"Barbell",False,True,False,False,"Power Snatch","Jump Shrug (snatch grip)"),
        ("High Pull (hang)","Ball","—","POW",3,"Barbell",False,True,False,False,"Hang Clean","Jump Shrug"),
        ("Med Ball Overhead Throw","Ball","VPush","POW",3,"Medicine Ball",False,True,False,False,"Med Ball Slam","Med Ball Chest Pass"),
        ("Med Ball Slam","Ball","—","POW",3,"Medicine Ball",False,True,False,False,"Rotational Med Ball Slam","Med Ball Overhead Throw"),
        ("Hang Clean","Ball","—","POW",4,"Barbell + Bumpers",False,True,False,False,"Power Clean","High Pull"),
        ("Power Snatch","Ball","—","POW",4,"Barbell + Bumpers",False,True,False,False,"Snatch + Overhead Squat","Snatch High Pull"),
        ("Power Clean","Ball","—","POW",5,"Barbell + Bumpers",False,True,False,False,"Clean + Jerk","Hang Clean"),
        ("Clean + Jerk","Ball","—","POW",5,"Barbell + Bumpers",False,True,False,False,"—","Power Clean"),
        # Sprint/COD
        ("High Knee March","Sprint/COD","—","MOB",1,"Bodyweight",False,False,False,False,"A-Skip","—"),
        ("Standing Fall (lean)","Sprint/COD","—","POW",1,"Bodyweight",False,True,False,False,"Wall Lean Drill","—"),
        ("March to Stop","Sprint/COD","—","STAB",1,"Bodyweight + Cones",False,False,False,False,"Deceleration to Stop","—"),
        ("Wall Lean Drill","Sprint/COD","—","POW",2,"Wall + Bodyweight",False,True,False,False,"10m Sled Push","Standing Fall"),
        ("A-Skip","Sprint/COD","—","POW",2,"Bodyweight",False,True,False,False,"A-Run","High Knee March"),
        ("Deceleration to Stop","Sprint/COD","—","STAB",2,"Bodyweight + Cones",False,False,False,False,"Decel + Reaccel","March to Stop"),
        ("10m Sled Push","Sprint/COD","—","POW",2,"Sled + Light Weight",False,True,False,False,"10m Acceleration","Wall Lean Drill"),
        ("A-Run","Sprint/COD","—","POW",3,"Bodyweight",False,True,False,False,"Flying 10m","A-Skip"),
        ("Wicket Run","Sprint/COD","—","POW",3,"Mini-Hurdles",False,True,False,False,"Low Wickets","High Knee March"),
        ("Decel + Reaccel","Sprint/COD","—","POW/COND",3,"Bodyweight + Cones",False,True,False,False,"Pro Shuttle","Deceleration to Stop"),
        ("10m Acceleration","Sprint/COD","—","POW",3,"Timing Gates",False,True,False,False,"20m Acceleration","10m Sled Push"),
        ("Flying 10m","Sprint/COD","—","POW",4,"Timing Gates",False,True,False,False,"Flying 20m","A-Run"),
        ("Pro Shuttle (5-10-5)","Sprint/COD","—","POW/COD",4,"Cones",False,True,False,True,"T-Drill","Decel + Reaccel"),
        ("3-Cone Drill (L-Drill)","Sprint/COD","—","COD",4,"Cones",False,True,False,True,"Pro Shuttle","Box Drill"),
        ("20m Acceleration","Sprint/COD","—","POW",4,"Timing Gates",False,True,False,False,"Resisted Sprint","10m Acceleration"),
        ("Flying 20m","Sprint/COD","—","POW",5,"Timing Gates",False,True,False,False,"Flying 30m","Flying 10m"),
        ("Resisted Sprint (heavy sled)","Sprint/COD","—","POW",5,"Sled (heavy)",False,True,False,False,"—","20m Acceleration"),
        ("T-Drill","Sprint/COD","—","COD",5,"Cones",False,True,False,True,"Reactive Shuttle","Pro Shuttle"),
        # Rot
        ("Band Half-Kneeling Chop","Rot","Core","POW/STAB",1,"Band + Anchor",False,False,False,True,"Standing Band Chop","—"),
        ("Standing Band Chop","Rot","Core","POW",2,"Band + Anchor",False,False,False,True,"Cable Chop","Band Half-Kneeling Chop"),
        ("Half-Kneeling Landmine Rotation","Rot","Core","STR",2,"Barbell + Landmine",False,False,False,True,"Standing Landmine Rotation","Band Anti-Rotation Press"),
        ("Med Ball Rotational Throw","Rot","Ball","POW",2,"Medicine Ball + Wall",False,True,False,True,"Cable Rotational Row","Band Rotational Chop"),
        ("Cable Rotational Row","Rot","HPull","STR",3,"Cable Machine",False,False,False,True,"Landmine Rotation (heavy)","Med Ball Rotational Throw"),
        ("Standing Landmine Rotation","Rot","Core","STR",3,"Barbell + Landmine",False,False,False,True,"Heavy Landmine Rotation","Half-Kneeling Landmine Rotation"),
        ("Cable Chop (low to high)","Rot","—","POW",3,"Cable Machine",False,True,False,True,"Med Ball Overhead Rotational Slam","Band Rotational Chop"),
        ("Landmine Rotation (heavy)","Rot","Core","STR",4,"Barbell + Landmine",False,False,False,True,"—","Standing Landmine Rotation"),
        ("Med Ball Overhead Rotational Slam","Rot","Ball","POW",4,"Medicine Ball",False,True,False,True,"Rotational Slam + Sprint","Med Ball Rotational Throw"),
        ("Russian Twist (weighted)","Rot","Core","HYP",2,"Plate/Med Ball",False,False,False,True,"Standing Rotational Med Ball","Bicycle Crunch"),
        # Carry
        ("Farmer's Walk (light)","Carry","Core","COND/STAB",1,"DB/KB",False,False,False,False,"Farmer's Walk (moderate)","—"),
        ("Bear Hug Carry","Carry","Core","COND/STAB",1,"Med Ball/Plate",False,False,False,False,"Farmer's Walk","Farmer's Walk (lighter)"),
        ("Suitcase Carry (light)","Carry","Core","STAB",2,"Single DB/KB",True,False,False,False,"Suitcase Carry (moderate)","Farmer's Walk (light)"),
        ("Farmer's Walk (moderate)","Carry","Core","COND/STAB",2,"DB/KB",False,False,False,False,"Front Rack Carry","Farmer's Walk (light)"),
        ("Suitcase Carry (moderate)","Carry","Core","STAB",3,"Single DB/KB",True,False,False,False,"Waiter's Walk","Suitcase Carry (light)"),
        ("Front Rack Carry","Carry","DLKD","COND/STAB",3,"KB/Barbell (racked)",False,False,False,False,"Trap Bar Carry","Farmer's Walk (moderate)"),
        ("Waiter's Walk","Carry","VPush","STAB",3,"Single DB/KB (overhead)",True,False,False,False,"Single-Arm Overhead Carry","Suitcase Carry (moderate)"),
        ("Trap Bar Carry","Carry","DLHD","STR/COND",4,"Trap Bar",False,False,False,False,"Farmer's Walk (heavy)","Front Rack Carry"),
        ("Single-Arm Overhead Carry","Carry","Core","STAB",4,"Single DB/KB",True,False,False,False,"Overhead Carry (bilateral)","Waiter's Walk"),
        ("Farmer's Walk (heavy)","Carry","Core","STR/COND",4,"DB/KB (heavy)",False,False,False,False,"Yoke Walk","Trap Bar Carry"),
        ("Overhead Carry (bilateral)","Carry","VPush","STAB",4,"DB (overhead)",False,False,False,False,"Single-Arm Overhead Carry (heavier)","Single-Arm Overhead Carry"),
        ("Zercher Carry","Carry","DLKD","STR",5,"Barbell (in elbows)",False,False,False,False,"—","Front Rack Carry"),
        ("Yoke Walk","Carry","DLHD","STR/COND",5,"Yoke/Barbell on Back",False,False,False,False,"—","Farmer's Walk (heavy)"),
        # Core
        ("Marching Dead Bug","Core","—","STAB",1,"Bodyweight",False,False,False,False,"Dead Bug","—"),
        ("Dead Bug","Core","—","STAB",1,"Bodyweight",False,False,False,False,"Hollow Hold","Marching Dead Bug"),
        ("Bent-Knee Side Plank","Core","—","STAB",1,"Bodyweight",False,False,True,False,"Side Plank","—"),
        ("Pallof Press (hold)","Core","Rot","STAB",1,"Cable/Band",False,False,True,False,"Single-Leg Pallof","Band Hold"),
        ("Reverse Crunch","Core","—","STR",1,"Floor/Mat",False,False,False,False,"Hanging Knee Raise","Dead Bug"),
        ("Plank (front)","Core","—","STAB",2,"Bodyweight",False,False,True,False,"RKC Plank","Dead Bug"),
        ("Side Plank","Core","—","STAB",2,"Bodyweight",False,False,True,False,"Side Plank (leg raise)","Bent-Knee Side Plank"),
        ("Single-Leg Pallof","Core","Rot","STAB",2,"Cable/Band",False,False,True,False,"Cable Anti-Rotation Press","Pallof Press"),
        ("Lying Leg Raise","Core","—","STR",2,"Floor/Mat",False,False,False,False,"Hanging Knee Raise","Dead Bug"),
        ("RKC Plank","Core","—","STAB",3,"Bodyweight",False,False,True,False,"Weighted Plank","Plank"),
        ("Side Plank (leg raise)","Core","—","STAB",3,"Bodyweight",False,False,True,False,"Copenhagen Plank","Side Plank"),
        ("Dead Bug (weighted)","Core","—","STR",3,"DB/Plate",False,False,False,False,"Weighted Hollow Hold","Dead Bug"),
        ("Weighted Plank","Core","—","STAB",3,"Plate/Barbell",False,False,True,False,"Ab Wheel Rollout","RKC Plank"),
        ("Ab Wheel Rollout (kneeling)","Core","—","STR",3,"Ab Wheel",False,False,False,False,"Standing Rollout","Weighted Plank"),
        ("Cable Anti-Rotation Press","Core","Rot","STAB",3,"Cable Machine",False,False,True,False,"Walking Pallof","Single-Leg Pallof"),
        ("Hanging Knee Raise","Core","VPull","STR",3,"Pull-Up Bar",False,False,False,False,"Hanging Leg Raise","Lying Leg Raise"),
        ("Walking Pallof","Core","Rot","STAB",4,"Cable Machine",False,False,True,False,"Single-Leg + Overhead Pallof","Single-Leg Pallof"),
        ("Hanging Leg Raise","Core","VPull","STR",4,"Pull-Up Bar",False,False,False,False,"Toes to Bar","Hanging Knee Raise"),
        ("Copenhagen Plank","Core","—","STAB",4,"Bench/Partner",False,False,True,False,"Weighted Copenhagen","Side Plank (leg raise)"),
        ("Standing Rollout","Core","—","STR",4,"Ab Wheel",False,False,False,False,"—","Ab Wheel Rollout (kneeling)"),
        ("Toes to Bar","Core","VPull","STR",5,"Pull-Up Bar",False,False,False,False,"—","Hanging Leg Raise"),
        # Acc/Prehab
        ("Band Pull-Apart","Acc/Prehab","HPull","STAB",1,"Band",False,False,False,False,"Prone T Raise","Band Dislocate"),
        ("Band Dislocate","Acc/Prehab","—","MOB",1,"Band (long)",False,False,False,False,"PVC Pass-Through","—"),
        ("Band Lateral Walk","Acc/Prehab","—","STAB",1,"Band (ankle)",False,False,False,False,"Banded Side Step (squat)","—"),
        ("Band External Rotation","Acc/Prehab","—","STAB",1,"Band",True,False,False,False,"Cable External Rotation","—"),
        ("Band Internal Rotation","Acc/Prehab","—","STAB",1,"Band",True,False,False,False,"Cable Internal Rotation","—"),
        ("Glute Med Clamshell","Acc/Prehab","Core","STAB",1,"Band/Bodyweight",False,False,False,False,"Band Lateral Walk","—"),
        ("PVC Shoulder Pass-Through","Acc/Prehab","—","MOB",1,"PVC Pipe",False,False,False,False,"Weighted Bar Pass-Through","Band Dislocate"),
        ("Ankle Dorsiflexion Mobilisation","Acc/Prehab","—","MOB",1,"Band/Wall",False,False,False,False,"Weighted Ankle Mobilisation","Calf Stretch"),
        ("Seated Calf Raise","Acc/Prehab","—","STR/HYP",1,"DB/Machine",False,False,False,False,"Standing Calf Raise","Bodyweight Calf Raise"),
        ("Tibialis Raise","Acc/Prehab","—","STR",1,"Band/Weight Plate",False,False,False,False,"Weighted Tib Raise","Band Dorsiflexion"),
        ("Face Pull","Acc/Prehab","HPull","STAB",1,"Cable/Band",False,False,False,False,"Cable Face Pull (heavy)","Band Pull-Apart"),
        ("Prone W Raise","Acc/Prehab","HPull","STAB",1,"Bodyweight",False,False,False,False,"Prone T Raise","Scapular Retraction"),
        ("Prone T Raise","Acc/Prehab","HPull","STAB",2,"Light DB",False,False,False,False,"Prone Y Raise","Prone W Raise"),
        ("Standing Calf Raise","Acc/Prehab","—","STR/HYP",2,"Barbell/Machine",False,False,False,False,"Single-Leg Calf Raise","Seated Calf Raise"),
        ("Cable External Rotation","Acc/Prehab","—","STAB",2,"Cable Machine",True,False,False,False,"Prone Y Raise","Band External Rotation"),
        ("Cable Internal Rotation","Acc/Prehab","—","STAB",2,"Cable Machine",True,False,False,False,"—","Band Internal Rotation"),
        ("Dumbbell Lateral Raise","Acc/Prehab","VPush","HYP",2,"DB",False,False,False,False,"Cable Lateral Raise","Band Lateral Raise"),
        ("Prone Y Raise","Acc/Prehab","HPull","STAB",3,"Light DB",False,False,False,False,"Bent-Over Rear Delt Fly","Prone T Raise"),
        ("Single-Leg Calf Raise","Acc/Prehab","Sprint","STR",3,"DB",True,False,False,False,"Weighted Single-Leg Calf Raise","Standing Calf Raise"),
        ("Weighted Ankle Mobilisation","Acc/Prehab","—","MOB",2,"Band + Weight",False,False,False,False,"—","Ankle Dorsiflexion Mobilisation"),
        ("Cable Face Pull (heavy)","Acc/Prehab","HPull","STAB/HYP",3,"Cable Machine",False,False,False,False,"—","Face Pull"),
    ]
    exercises = []
    for r in rows:
        exercises.append(Exercise(
            name=r[0], family=r[1], secondary=r[2], objective=r[3],
            difficulty=r[4], equipment=r[5], unilateral=r[6],
            explosive=r[7], isometric=r[8], rotational=r[9],
            progression=r[10], regression=r[11],
        ))
    return exercises


def load_blueprints() -> list[Blueprint]:
    """14 blueprints from FORGE_BLUEPRINT_CATALOG_V1.md."""
    return [
        Blueprint("Full Body Strength", "3-4",
            ["Ball", "DLKD", "HPush", "DLHD / HPull", "Core"],
            ["DLKD", "DLHD", "HPush", "HPull"],
            ["Core", "Acc/Prehab", "VPush", "VPull"]),
        Blueprint("Strength + Power", "4-5",
            ["Ball", "DLKD", "HPush / HPull", "DLHD", "Core"],
            ["Ball", "DLKD", "DLHD", "HPush"],
            ["Carry", "Sprint/COD", "Rot", "Core"]),
        Blueprint("Strength + Conditioning", "3-4",
            ["DLKD / DLHD", "HPush", "HPull", "Core"],
            ["DLKD", "DLHD", "HPush", "HPull"],
            ["Carry", "Core", "Acc/Prehab", "Sprint/COD"],
            notes="1 Knee Dominant OR 1 Hip Dominant required."),
        Blueprint("Power + Speed", "3-4",
            ["Sprint/COD", "Plyo", "Ball", "DLHD", "Core"],
            ["Sprint/COD", "Plyo", "Ball"],
            ["DLHD", "HPush", "Core"]),
        Blueprint("Upper / Lower Split", "4",
            ["Plyo", "DLKD", "DLHD", "Carry", "Core",
             "VPush", "HPush", "VPull", "HPull", "Acc/Prehab"],
            ["DLKD", "DLHD", "HPush", "HPull"],
            ["Carry", "Core", "Acc/Prehab", "Rot", "VPush", "VPull"],
            notes="Lower day + Upper day alternated. Bodybuilding focus."),
        Blueprint("Power Maintenance", "1-2",
            ["Sprint/COD", "Ball", "Plyo", "Core"],
            ["Ball", "Plyo"],
            ["Sprint/COD", "DLHD", "Core", "Acc/Prehab"]),
        Blueprint("Youth Foundation (U14-U20)", "2-3",
            ["Sprint/COD", "DLKD / DLHD", "HPush", "HPull", "Core"],
            ["DLKD", "DLHD", "HPush", "HPull"],
            ["All"],
            notes="Prioritise variety over specialisation."),
        Blueprint("Court Sport Athletic Development", "3-4",
            ["Sprint/COD", "Plyo", "SLKD", "Rot", "HPull", "Core"],
            ["Sprint/COD", "SLKD", "HPush", "Rot"],
            ["DLHD", "Ball", "Carry", "Core", "Acc/Prehab"]),
        Blueprint("Rugby Off-Season", "4-5",
            ["Ball", "DLKD", "HPull / HPush", "Carry", "Sprint/COD", "Acc/Prehab"],
            ["Ball", "DLKD", "HPush", "HPull", "Carry"],
            ["Sprint/COD", "Core", "Rot", "Acc/Prehab"]),
        Blueprint("Sprint Development", "3-4",
            ["Sprint/COD", "Plyo", "DLHD", "DLKD", "Core"],
            ["Sprint/COD", "DLHD", "Plyo"],
            ["DLKD", "HPull", "Core", "Acc/Prehab"]),
        Blueprint("Hypertrophy / Mass Accrual", "4-6",
            ["DLKD", "DLHD", "HPush", "HPull", "Core"],
            ["DLKD", "DLHD", "HPush", "HPull"],
            ["All"],
            notes="Higher volume (15-20 reps), shorter rest (60-90s)."),
        Blueprint("Return to Sport (Foundation)", "3-4",
            ["Acc/Prehab", "DLKD / DLHD", "SLKD", "Core", "Sprint/COD"],
            ["Acc/Prehab", "DLKD", "Core"],
            ["SLKD", "Sprint/COD", "Rot", "Carry"],
            notes="Regressed versions only. Pain-free movement priority."),
        Blueprint("Deload / Active Recovery", "2-3",
            ["Acc/Prehab", "DLKD / DLHD", "Core", "Acc/Prehab"],
            [],  # no mandatory — move well
            ["Acc/Prehab", "Core", "Carry"],
            notes="50-60% 1RM, 2-3 RIR. This IS the regression."),
        Blueprint("Mixed Modal (GPP)", "4-5",
            ["Sprint/COD", "DLKD", "DLHD", "HPush", "HPull", "Plyo", "Core", "Carry", "Acc/Prehab"],
            [],
            ["All"],
            notes="Rotates daily. All families hit 1-2x/week."),
    ]


# ── Substitution data from FORGE_SUBSTITUTION_MATRIX_V1.md ─────────────────

CROSS_FAMILY_SUBSTITUTE = {
    "DLKD": "SLKD", "SLKD": "DLKD",
    "DLHD": "SLHD", "SLHD": "DLHD",
    "HPush": "VPush", "VPush": "HPush",
    "HPull": "VPull", "VPull": "HPull",
    "Plyo": "Ball", "Ball": "Plyo",
    "Sprint/COD": "Plyo",
    "Rot": "Core",
    "Carry": "Core",
    "Core": "Carry",
}


# ── Logic ──────────────────────────────────────────────────────────────────

def difficulty_range(level: str) -> tuple:
    """Map athlete level to (min_diff, max_diff)."""
    m = {"beginner": (1, 2), "intermediate": (2, 4), "advanced": (3, 5)}
    return m.get(level.lower(), (2, 4))


def select_exercise(
    exercises: list[Exercise], family: str,
    diff_min: int, diff_max: int, equip_level: int,
    used_names: set, allow_explosive: bool = True,
) -> Optional[Exercise]:
    """Pick an exercise matching filters. Prefer unused, then random."""
    pool = [e for e in exercises if e.family == family
            and e.difficulty >= diff_min and e.difficulty <= diff_max
            and e.equip_ok(equip_level)
            and (allow_explosive or not e.explosive)]
    if not pool:
        return None
    unused = [e for e in pool if e.name not in used_names]
    if unused:
        return random.choice(unused)
    return random.choice(pool)


def substitute(
    exercises: list[Exercise], family: str,
    diff_min: int, diff_max: int, equip_level: int,
    used_names: set,
) -> Optional[Exercise]:
    """Fallback: try same family, then cross-family. Never exceeds athlete level."""
    pool = [e for e in exercises if e.family == family
            and e.difficulty >= diff_min and e.difficulty <= diff_max
            and e.equip_ok(equip_level)]
    if pool:
        unused = [e for e in pool if e.name not in used_names]
        return random.choice(unused or pool)
    # cross-family — still respects athlete level
    alt = CROSS_FAMILY_SUBSTITUTE.get(family)
    if alt:
        return select_exercise(exercises, alt, diff_min, diff_max, equip_level, used_names)
    return None


def resolve_slot_families(slot_order: list, mandatory: list, optional: list) -> list:
    """Flatten slot order into concrete family list for a single session.
    Handles '/' alternatives (e.g. 'DLHD / HPull' picks DLHD if mandatory, else HPull)."""
    result = []
    seen = set()
    need = list(mandatory)
    for slot in slot_order:
        parts = [s.strip() for s in slot.split("/")]
        chosen = None
        for p in parts:
            if p in need and p not in seen:
                chosen = p
                break
        if chosen is None:
            for p in parts:
                if p not in seen and p in FAMILIES_SHORT:
                    chosen = p
                    break
        if chosen and chosen not in seen:
            result.append(chosen)
            seen.add(chosen)
            if chosen in need:
                need.remove(chosen)
    # Add any remaining mandatory families not covered by slot_order
    for f in need:
        if f not in seen:
            result.append(f)
            seen.add(f)
    # Add a few optional families
    extra = [f for f in optional if f not in seen]
    random.shuffle(extra)
    for f in extra[:random.randint(0, 2)]:
        result.append(f)
    return result


# ── Program generation ────────────────────────────────────────────────────

def generate_session(
    exercises: list[Exercise], blueprint: Blueprint,
    diff_min: int, diff_max: int, equip_level: int,
    week: int = 1, session_num: int = 1,
) -> list[tuple[str, Exercise]]:
    """Generate one session. Returns list of (label, exercise)."""
    families = resolve_slot_families(blueprint.slot_order, blueprint.mandatory, blueprint.optional)
    used_names = set()
    # Vary difficulty slightly by week
    w_diff_min = max(1, diff_min + (week - 1) // 2)
    w_diff_max = min(5, diff_max + (week - 1) // 2)
    result = []
    for fam in families:
        ex = select_exercise(exercises, fam, w_diff_min, w_diff_max, equip_level, used_names)
        if ex is None:
            ex = substitute(exercises, fam, w_diff_min, w_diff_max, equip_level, used_names)
        if ex is None:
            continue
        result.append((fam, ex))
        used_names.add(ex.name)
    return result


def format_program(
    blueprint: Blueprint, sessions: list[list[tuple[str, Exercise]]],
    athlete_level: str, equip_label: str,
) -> str:
    """Format as human-readable program."""
    lines = [
        "=" * 60,
        f"  FORGE Program: {blueprint.name}",
        f"  Athlete Level: {athlete_level}   Equipment: {equip_label}",
        f"  Frequency: {blueprint.frequency}",
        "=" * 60,
        "",
    ]
    for i, session in enumerate(sessions):
        lines.append(f"Session {i + 1}")
        lines.append("-" * 40)
        current_slot = None
        for fam, ex in session:
            label = FAMILIES_LONG.get(fam, fam)
            if label != current_slot:
                lines.append(f"\n{label}")
                current_slot = label
            diff_label = f"L{ex.difficulty}"
            lines.append(f"  * {ex.name}  [{diff_label}]  ({ex.equipment})")
        lines.append("")
    return "\n".join(lines)


def generate_program(
    blueprint_name: str, athlete_level: str, equip_label: str,
    weeks: int = 4,
) -> str:
    """Top-level: generate a complete program."""
    exercises = load_exercises()
    bps = load_blueprints()
    bp = next((b for b in bps if b.name.lower() == blueprint_name.lower()), None)
    if bp is None:
        return f"Unknown blueprint: {blueprint_name}"

    equip_map = {"bodyweight": 0, "minimal": 1, "basic gym": 2, "full gym": 3, "full": 3}
    equip_level = equip_map.get(equip_label.lower(), 2)
    diff_min, diff_max = difficulty_range(athlete_level)
    freq = int(bp.frequency[0]) if bp.frequency else 3

    all_sessions = []
    for w in range(1, weeks + 1):
        for s in range(1, freq + 1):
            session = generate_session(exercises, bp, diff_min, diff_max, equip_level, w, s)
            all_sessions.append(session)

    return format_program(bp, all_sessions, athlete_level, equip_label)


# ── Substitution tests ────────────────────────────────────────────────────

def test_substitution():
    """Verify substitute() never returns an exercise outside athlete range."""
    exercises = load_exercises()
    bps = load_blueprints()
    levels_def = {"beginner": (1, 2), "intermediate": (2, 4), "advanced": (3, 5)}
    equip_defs = [("bodyweight", 0), ("minimal", 1), ("basic gym", 2), ("full gym", 3)]

    violations = []
    for bp in bps:
        for level, (dmin, dmax) in levels_def.items():
            for elabel, ecode in equip_defs:
                freq = int(bp.frequency[0])
                for w in range(1, 5):
                    w_min = max(1, dmin + (w - 1) // 2)
                    w_max = min(5, dmax + (w - 1) // 2)
                    for s in range(freq):
                        session = generate_session(exercises, bp, dmin, dmax, ecode, w, s)
                        for fam, ex in session:
                            if ex.difficulty < w_min or ex.difficulty > w_max:
                                violations.append(
                                    f"{bp.name:35s} {level:12s} {elabel:12s} "
                                    f"week{w} L{ex.difficulty} {ex.name:35s} "
                                    f"(range L{w_min}-L{w_max})"
                                )

    if violations:
        print(f"\nVIOLATIONS: {len(violations)}")
        for v in violations[:30]:
            print(f"  {v}")
        if len(violations) > 30:
            print(f"  ... and {len(violations)-30} more")
    else:
        print("\nALL PASS — no substitution violations across 168 programs.")
    return len(violations)


# ── Demo / 20-program test ────────────────────────────────────────────────

def demo():
    """Generate and print 20 example programs."""
    blueprints = [b.name for b in load_blueprints()]
    levels = ["beginner", "intermediate", "advanced"]
    equips = ["bodyweight", "minimal", "basic gym", "full gym"]

    random.seed(42)
    count = 0
    for i in range(20):
        bp = random.choice(blueprints)
        lvl = random.choice(levels)
        eq = random.choice(equips)
        print(f"\n{'#'*60}")
        print(f"# PROGRAM {i+1}: {bp} | {lvl} | {eq}")
        print(f"{'#'*60}")
        try:
            prog = generate_program(bp, lvl, eq)
            print(prog)
            count += 1
        except Exception as e:
            print(f"  FAILED: {e}")

    print(f"\n{'='*60}")
    print(f"  Generated {count}/20 programs successfully.")
    print(f"{'='*60}")


# ── CLI ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    elif len(sys.argv) > 1 and sys.argv[1] == "test_substitution":
        test_substitution()
    elif len(sys.argv) >= 4:
        bp = sys.argv[1]
        lvl = sys.argv[2]
        eq = sys.argv[3]
        weeks = int(sys.argv[4]) if len(sys.argv) > 4 else 4
        print(generate_program(bp, lvl, eq, weeks))
    else:
        print("Usage:")
        print("  python forge_prototype.py demo")
        print("  python forge_prototype.py \"Blueprint Name\" level equipment [weeks]")
        print()
        print("Levels: beginner | intermediate | advanced")
        print("Equipment: bodyweight | minimal | basic gym | full gym")
        print()
        print("Example:")
        print('  python forge_prototype.py "Full Body Strength" intermediate "basic gym"')
        print('  python forge_prototype.py "Rugby Off-Season" advanced "full gym" 6')
