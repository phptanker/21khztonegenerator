# Quick Start Guide - GUI Version

## Run the GUI Version Directly

```bash
# Install dependencies (one time only)
pip install -r requirements.txt

# Run the GUI
python tone_generator_gui.py
```

## Using the Interface

### Main Controls

1. **Frequency Slider/Spinbox**
   - Range: 1.0 - 24.0 kHz
   - Default: 21.0 kHz (above human hearing)
   - Adjust in real-time even while playing

2. **Volume Slider/Spinbox**
   - Range: 1% - 100%
   - Default: 10%
   - Start low to avoid issues, increase if DAC still sleeps

3. **Start/Stop Button**
   - Click to toggle tone playback
   - Shows current status and settings when playing

4. **Minimize to Tray Button**
   - Hides window to system tray
   - Program continues running in background

### System Tray Features

When minimized to tray, right-click the tray icon to:
- **Show** - Restore the main window
- **Start/Stop** - Toggle tone without opening window
- **Quit** - Close the application completely

## Recommended Settings for DAC Keep-Alive

- **Frequency:** 20-22 kHz (inaudible to most people)
- **Volume:** 5-15% (just enough to keep DAC awake)
- **Minimize to tray** and let it run in background

## Build Standalone Executable

For a version that doesn't require Python:

1. Install PyInstaller: `pip install pyinstaller`
2. Run: `build_exe.bat` and select **Option 1** (GUI version)
3. Find executable in `dist\DACKeepAlive_GUI.exe`
4. Double-click `create_startup_shortcut.vbs` to add to Windows startup

## Tips

- Start with low volume (10%) and increase if needed
- Most DACs stay awake with 21 kHz at 10% volume
- System tray icon allows control without opening window
- Settings can be adjusted while tone is playing
