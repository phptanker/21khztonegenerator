# DAC Keep-Alive Tone Generator

A simple Windows program that continuously plays a 21kHz tone to keep your DAC (Digital-to-Analog Converter) awake by providing a constant audio signal.

## Features

- **Two versions available:**
  - **GUI version** (`tone_generator_gui.py`) - With controls and system tray
  - **Console version** (`tone_generator.py`) - Runs in background
- Generates a continuous tone (default 21kHz)
- Adjustable frequency (1-24 kHz) and volume (1-100%)
- System tray support - minimize to taskbar
- Start/Stop control
- Can be configured for Windows autostart

## Installation

### Option 1: Run with Python

1. Install Python 3.8 or higher
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the program:
   - **GUI version (recommended):** `python tone_generator_gui.py`
   - **Console version:** `python tone_generator.py`

### Option 2: Create Windows Executable

1. Install dependencies:
   ```
   pip install -r requirements.txt
   pip install pyinstaller
   ```
2. Double-click `build_exe.bat` and choose which version to build
   - **Option 1:** GUI version with controls
   - **Option 2:** Console version (background only)
3. The executable will be in the `dist` folder

## Using the GUI Version

The GUI version (`tone_generator_gui.py` or `DACKeepAlive_GUI.exe`) provides:

- **Frequency Control:** Adjust from 1 kHz to 24 kHz using slider or spinbox
- **Volume Control:** Set volume from 1% to 100%
- **Start/Stop Button:** Control tone playback
- **System Tray:** Minimize to tray - right-click tray icon to show/start/stop/quit
- **Live Status:** See current frequency and volume in real-time

Simply adjust the settings and click **Start** to begin playing the tone. You can minimize the window to the system tray while it runs in the background.

## Windows Autostart Setup

### Method 1: Startup Folder (Recommended)

1. Press `Win + R` and type: `shell:startup`
2. Create a shortcut to the executable or Python script in this folder
3. The program will start automatically when Windows boots

### Method 2: Task Scheduler

1. Open Task Scheduler
2. Create a new task:
   - Trigger: At log on
   - Action: Start a program (point to the executable or python script)
   - Settings: Allow task to be run on demand, run task as soon as possible if missed

### Method 3: Registry (Advanced)

Add a registry entry to:
```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```
With the value pointing to your executable path.

## Configuration

### GUI Version
Use the built-in controls to adjust settings in real-time:
- **Frequency:** 1-24 kHz (adjustable via slider/spinbox)
- **Volume:** 1-100% (adjustable via slider/spinbox)

### Console Version
Modify these parameters in `tone_generator.py`:
- **FREQUENCY**: Tone frequency in Hz (default: 21000)
- **SAMPLE_RATE**: Audio sample rate (default: 48000)
- **AMPLITUDE**: Volume level from 0.0 to 1.0 (default: 0.1)
- **DURATION**: Chunk duration for generation (default: 1.0 second)

## Stopping the Program

- **GUI version:** Click the **Stop** button or right-click tray icon → Quit
- **Console version:** Press `Ctrl+C` or use Task Manager to end the process

## Troubleshooting

### No audio output
- Check that your default audio device is set correctly
- Try increasing the AMPLITUDE value
- Ensure your DAC supports the sample rate (48kHz)

### High CPU usage
- Increase the DURATION value for larger chunks
- This generates audio in chunks to reduce CPU load

### DAC still goes to sleep
- Some DACs may require higher sample rates (try 96000 or 192000)
- Increase AMPLITUDE slightly (but keep it low)
- Try a lower frequency if 21kHz is beyond your DAC's range

## Notes

- The 21kHz tone is above the typical human hearing range (20Hz-20kHz)
- Uses low amplitude to minimize any potential audible artifacts
- Sample rate is set to 48kHz (sufficient for 21kHz tone per Nyquist theorem)
