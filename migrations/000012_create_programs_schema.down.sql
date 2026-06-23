-- Forge Exercise Intelligence Database - Migration 000012 (Down)
-- Description: Safely drop program builder tables.

DROP TABLE IF EXISTS program_session_exercises CASCADE;
DROP TABLE IF EXISTS program_sessions CASCADE;
DROP TABLE IF EXISTS program_weeks CASCADE;
DROP TABLE IF EXISTS programs CASCADE;
