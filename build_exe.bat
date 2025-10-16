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
pyinstaller --onefile --noconsole --name DACKeepAlive --icon=NONE tone_generator.py

echo.
echo Build complete! Executable is in the 'dist' folder.
echo.
pause
