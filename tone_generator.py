"""
DAC Keep-Alive Tone Generator
Plays a continuous 21kHz tone to keep your DAC awake.
"""

import numpy as np
import sounddevice as sd
import sys
import signal
import time

# Configuration
FREQUENCY = 21000  # 21kHz
SAMPLE_RATE = 48000  # 48kHz sample rate (must be >= 2x the frequency per Nyquist)
AMPLITUDE = 0.1  # Volume (0.0 to 1.0) - kept low to avoid issues
DURATION = 1.0  # Generate 1 second chunks

class ToneGenerator:
    def __init__(self):
        self.running = True
        self.stream = None
        
    def generate_tone(self, duration, frequency, sample_rate, amplitude):
        """Generate a sine wave tone."""
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = amplitude * np.sin(2 * np.pi * frequency * t)
        return tone.astype(np.float32)
    
    def audio_callback(self, outdata, frames, time_info, status):
        """Callback function for audio stream."""
        if status:
            print(f"Audio status: {status}", file=sys.stderr)
        
        # Generate tone for this chunk
        tone = self.generate_tone(frames / SAMPLE_RATE, FREQUENCY, SAMPLE_RATE, AMPLITUDE)
        outdata[:] = tone.reshape(-1, 1)
    
    def start(self):
        """Start playing the tone continuously."""
        print(f"Starting continuous {FREQUENCY}Hz tone at {SAMPLE_RATE}Hz sample rate...")
        print(f"Amplitude: {AMPLITUDE}")
        print("Press Ctrl+C to stop.")
        
        try:
            # Create output stream
            self.stream = sd.OutputStream(
                samplerate=SAMPLE_RATE,
                channels=1,
                callback=self.audio_callback,
                blocksize=int(SAMPLE_RATE * DURATION)
            )
            
            with self.stream:
                # Keep running until interrupted
                while self.running:
                    time.sleep(0.1)
                    
        except KeyboardInterrupt:
            print("\nStopping tone generator...")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    def stop(self):
        """Stop the tone generator."""
        self.running = False
        if self.stream:
            self.stream.stop()

def signal_handler(sig, frame):
    """Handle shutdown signals."""
    print("\nShutdown signal received...")
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and start generator
    generator = ToneGenerator()
    generator.start()
