-- Migration 000020: Populate technical_difficulty for Olympic lifts
-- Exercises 18-31 (added by 000017) have NULL technical_difficulty.
-- Values sourced from recommendation_engine.py mock catalog (the S&C authority).

BEGIN;

UPDATE exercises SET technical_difficulty = 3  WHERE id = 18;  -- Clean Pull
UPDATE exercises SET technical_difficulty = 4  WHERE id = 19;  -- Mid-Thigh Pull
UPDATE exercises SET technical_difficulty = 5  WHERE id = 20;  -- High Pull
UPDATE exercises SET technical_difficulty = 5  WHERE id = 21;  -- Snatch Pull
UPDATE exercises SET technical_difficulty = 6  WHERE id = 22;  -- Hang Clean
UPDATE exercises SET technical_difficulty = 9  WHERE id = 23;  -- Squat Clean
UPDATE exercises SET technical_difficulty = 10 WHERE id = 24;  -- Clean and Jerk
UPDATE exercises SET technical_difficulty = 8  WHERE id = 25;  -- Power Snatch
UPDATE exercises SET technical_difficulty = 7  WHERE id = 26;  -- Hang Snatch
UPDATE exercises SET technical_difficulty = 8  WHERE id = 27;  -- Snatch Balance
UPDATE exercises SET technical_difficulty = 7  WHERE id = 28;  -- Overhead Squat
UPDATE exercises SET technical_difficulty = 4  WHERE id = 29;  -- Push Press
UPDATE exercises SET technical_difficulty = 6  WHERE id = 30;  -- Push Jerk
UPDATE exercises SET technical_difficulty = 9  WHERE id = 31;  -- Split Jerk

COMMIT;
