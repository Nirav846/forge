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

REM ---- Start backend ----
start "FORGE Backend" cmd /k "cd /d %ROOT% && python -m uvicorn src.forge.api_server:app --reload --host 127.0.0.1 --port 8000"

REM ---- Start frontend ----
start "FORGE Frontend" cmd /k "cd /d %FRONTEND% && npm run dev"

echo FORGE is launching...
echo Backend:  http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo Frontend: http://127.0.0.1:3000
echo.
echo You can close this window.
timeout /t 3 >nul
exit