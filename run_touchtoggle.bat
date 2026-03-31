@echo off
echo TouchToggle - Starting Application...
echo.
echo Note: This application requires Administrator privileges
echo to modify touchscreen device settings.
echo.
echo If you see permission errors, please run this batch file
echo as Administrator (right-click and select "Run as administrator")
echo.
pause

cd /d "%~dp0"
python main.py

echo.
echo TouchToggle has exited.
pause
