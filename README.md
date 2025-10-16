# DAC Keep-Alive Tone Generator

A simple Windows program that continuously plays a 21kHz tone to keep your DAC (Digital-to-Analog Converter) awake by providing a constant audio signal.

## Features

- Generates a continuous 21kHz sine wave
- Low amplitude to avoid any audible interference
- Runs in the background
- Can be configured for Windows autostart

## Installation

### Option 1: Run with Python

1. Install Python 3.8 or higher
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the program:
   ```
   python tone_generator.py
   ```

### Option 2: Create Windows Executable

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Build the executable:
   ```
   pyinstaller --onefile --windowed --name DACKeepAlive tone_generator.py
   ```
3. The executable will be in the `dist` folder

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

You can modify these parameters in `tone_generator.py`:

- **FREQUENCY**: Tone frequency in Hz (default: 21000)
- **SAMPLE_RATE**: Audio sample rate (default: 48000)
- **AMPLITUDE**: Volume level from 0.0 to 1.0 (default: 0.1)
- **DURATION**: Chunk duration for generation (default: 1.0 second)

## Stopping the Program

- If running in console: Press `Ctrl+C`
- If running as executable: Use Task Manager to end the process

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
