@echo off
echo TouchToggle Executable Builder
echo ==============================
echo.
echo This will create a standalone TouchToggle.exe file
echo that can be run on any Windows computer without Python.
echo.
echo Make sure you have run 'python setup.py' first to install dependencies.
echo.
pause

cd /d "%~dp0"
python build_exe.py

echo.
echo Build process completed.
pause
