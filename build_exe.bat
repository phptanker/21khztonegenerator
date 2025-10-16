@echo off
echo Building DAC Keep-Alive executable...
echo.

REM Check if pyinstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

REM Build the executable
echo Building executable with PyInstaller...
echo.
echo Choose version to build:
echo 1. GUI version (with controls and system tray)
echo 2. Console version (original, runs in background)
echo.
choice /C 12 /M "Enter your choice"

if errorlevel 2 (
    echo Building console version...
    pyinstaller --onefile --noconsole --name DACKeepAlive --icon=NONE tone_generator.py
) else (
    echo Building GUI version...
    pyinstaller --onefile --windowed --name DACKeepAlive_GUI --icon=NONE tone_generator_gui.py
)

echo.
echo Build complete! Executable is in the 'dist' folder.
echo.
pause
