@echo off
echo Stopping FORGE processes...
taskkill /FI "WINDOWTITLE eq FORGE Backend" /F
taskkill /FI "WINDOWTITLE eq FORGE Frontend" /F
echo Done.
pause