"""
DAC Keep-Alive Tone Generator with GUI
Plays a continuous tone to keep your DAC awake with a graphical interface.
"""

import numpy as np
import sounddevice as sd
import tkinter as tk
from tkinter import ttk
import threading
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import io

class ToneGeneratorGUI:
    def __init__(self):
        self.running = False
        self.stream = None
        self.frequency = 21.0  # kHz
        self.amplitude = 0.1  # Volume (0.0 to 1.0)
        self.sample_rate = 48000
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("DAC Keep-Alive Tone Generator")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # System tray icon
        self.tray_icon = None
        
        # Set up window close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="DAC Keep-Alive Tone Generator", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frequency setting
        freq_frame = ttk.LabelFrame(main_frame, text="Frequency", padding="10")
        freq_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(freq_frame, text="Frequency (kHz):").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.freq_var = tk.DoubleVar(value=self.frequency)
        self.freq_spinbox = ttk.Spinbox(freq_frame, from_=1.0, to=24.0, increment=0.1,
                                        textvariable=self.freq_var, width=10,
                                        command=self.update_frequency)
        self.freq_spinbox.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        self.freq_scale = ttk.Scale(freq_frame, from_=1.0, to=24.0, orient=tk.HORIZONTAL,
                                    variable=self.freq_var, command=self.update_frequency)
        self.freq_scale.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.freq_display = ttk.Label(freq_frame, text=f"{self.frequency:.1f} kHz")
        self.freq_display.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Volume setting
        vol_frame = ttk.LabelFrame(main_frame, text="Volume", padding="10")
        vol_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(vol_frame, text="Volume:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.vol_var = tk.DoubleVar(value=self.amplitude)
        self.vol_spinbox = ttk.Spinbox(vol_frame, from_=0.01, to=1.0, increment=0.01,
                                       textvariable=self.vol_var, width=10,
                                       command=self.update_volume)
        self.vol_spinbox.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        self.vol_scale = ttk.Scale(vol_frame, from_=0.01, to=1.0, orient=tk.HORIZONTAL,
                                   variable=self.vol_var, command=self.update_volume)
        self.vol_scale.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.vol_display = ttk.Label(vol_frame, text=f"{int(self.amplitude * 100)}%")
        self.vol_display.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Status: Stopped", 
                                     font=("Arial", 10))
        self.status_label.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Start/Stop button
        self.toggle_button = ttk.Button(main_frame, text="Start", 
                                       command=self.toggle_tone, width=20)
        self.toggle_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Minimize to tray button
        minimize_button = ttk.Button(main_frame, text="Minimize to Tray", 
                                    command=self.minimize_to_tray, width=20)
        minimize_button.grid(row=5, column=0, columnspan=2, pady=5)
        
    def update_frequency(self, *args):
        """Update frequency from UI controls."""
        try:
            self.frequency = float(self.freq_var.get())
            self.freq_display.config(text=f"{self.frequency:.1f} kHz")
        except:
            pass
    
    def update_volume(self, *args):
        """Update volume from UI controls."""
        try:
            self.amplitude = float(self.vol_var.get())
            self.vol_display.config(text=f"{int(self.amplitude * 100)}%")
        except:
            pass
    
    def generate_tone(self, frames):
        """Generate a sine wave tone."""
        frequency_hz = self.frequency * 1000  # Convert kHz to Hz
        t = np.linspace(0, frames / self.sample_rate, frames, False)
        tone = self.amplitude * np.sin(2 * np.pi * frequency_hz * t)
        return tone.astype(np.float32)
    
    def audio_callback(self, outdata, frames, time_info, status):
        """Callback function for audio stream."""
        if status:
            print(f"Audio status: {status}", file=sys.stderr)
        
        # Generate tone for this chunk
        tone = self.generate_tone(frames)
        outdata[:] = tone.reshape(-1, 1)
    
    def start_tone(self):
        """Start playing the tone."""
        if not self.running:
            try:
                self.running = True
                self.stream = sd.OutputStream(
                    samplerate=self.sample_rate,
                    channels=1,
                    callback=self.audio_callback,
                    blocksize=int(self.sample_rate * 0.1)  # 100ms chunks
                )
                self.stream.start()
                
                self.toggle_button.config(text="Stop")
                frequency_hz = self.frequency * 1000
                self.status_label.config(
                    text=f"Status: Playing {frequency_hz:.0f} Hz at {int(self.amplitude * 100)}%"
                )
                
            except Exception as e:
                self.running = False
                self.status_label.config(text=f"Error: {str(e)}")
    
    def stop_tone(self):
        """Stop playing the tone."""
        if self.running:
            self.running = False
            if self.stream:
                self.stream.stop()
                self.stream.close()
                self.stream = None
            
            self.toggle_button.config(text="Start")
            self.status_label.config(text="Status: Stopped")
    
    def toggle_tone(self):
        """Toggle between start and stop."""
        if self.running:
            self.stop_tone()
        else:
            self.start_tone()
    
    def create_tray_icon(self):
        """Create a system tray icon."""
        # Create a simple icon image
        width = 64
        height = 64
        color1 = (0, 120, 215)  # Blue
        color2 = (255, 255, 255)  # White
        
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        
        # Draw a simple waveform
        dc.ellipse([16, 16, 48, 48], fill=color2)
        
        # Create menu
        menu = Menu(
            MenuItem('Show', self.show_window, default=True),
            MenuItem('Start' if not self.running else 'Stop', self.toggle_tone),
            MenuItem('Quit', self.quit_app)
        )
        
        return Icon("DAC Keep-Alive", image, "DAC Keep-Alive", menu)
    
    def minimize_to_tray(self):
        """Minimize window to system tray."""
        self.root.withdraw()
        
        if self.tray_icon is None:
            self.tray_icon = self.create_tray_icon()
            # Run tray icon in separate thread
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
    
    def show_window(self):
        """Show the main window from tray."""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def quit_app(self):
        """Quit the application."""
        self.stop_tone()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()
        self.root.destroy()
        sys.exit(0)
    
    def run(self):
        """Run the application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = ToneGeneratorGUI()
    app.run()
