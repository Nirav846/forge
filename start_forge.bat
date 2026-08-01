@echo off
setlocal

REM =========================
REM FORGE local launcher
REM Root: D:\forge
REM Backend: FastAPI / Uvicorn
REM Frontend: Vite / React
REM =========================

set ROOT=D:\forge
set FRONTEND=%ROOT%\forge_web

echo Starting FORGE...
echo.

REM ---- Start backend in the same window (not separate) ----
echo Starting backend...
start "FORGE Backend" cmd /k "cd /d %ROOT% && python -m uvicorn src.forge.api_server:app --reload --host 127.0.0.1 --port 8000"

REM ---- Start frontend in a separate window ----
start "FORGE Frontend" cmd /k "cd /d %FRONTEND% && npm run dev"

echo.
echo FORGE is launching...
echo Backend:  http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo Frontend: http://127.0.0.1:3000
echo.
echo To stop both, close the FORGE Backend and FORGE Frontend windows.
echo Or run: stop_forge.bat
echo.
timeout /t 2 >nul