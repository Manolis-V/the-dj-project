import pygame
import tkinter as tk
from tkinter import filedialog
import threading
import time

# Initialize Pygame for audio playback
pygame.mixer.init()

# Global variables to store sound objects and channels
track1 = None
track2 = None
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
is_transitioning = False

# Function to load the first track
def load_track1():
    global track1
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    
    if file_path:
        track1 = pygame.mixer.Sound(file_path)
        channel1.play(track1)  # Play the first track immediately

# Function to load the second track
def load_track2():
    global track2
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    
    if file_path:
        track2 = pygame.mixer.Sound(file_path)
        start_transition()  # Start the crossfade transition

# Function to handle the crossfade transition
def start_transition():
    global is_transitioning
    if track1 and track2:
        is_transitioning = True
        # Start playing the second track on channel2 but at zero volume
        channel2.play(track2)
        channel2.set_volume(0)
        
        # Run the crossfade in a separate thread
        threading.Thread(target=crossfade_tracks, daemon=True).start()

# Function to perform the crossfade
def crossfade_tracks():
    global is_transitioning
    fade_duration = 5.0  # Crossfade duration in seconds
    fade_steps = 50      # Number of steps in the fade
    step_duration = fade_duration / fade_steps

    for i in range(fade_steps):
        if not is_transitioning:
            break
        
        # Gradually reduce volume of channel1 (track1)
        current_volume1 = max(0, 1 - (i / fade_steps))  # Fade out
        channel1.set_volume(current_volume1)

        # Gradually increase volume of channel2 (track2)
        current_volume2 = min(1, i / fade_steps)  # Fade in
        channel2.set_volume(current_volume2)

        # Wait before updating again
        time.sleep(step_duration)

    # After crossfade, stop channel1 and let channel2 continue
    channel1.stop()
    is_transitioning = False

# Create the GUI
root = tk.Tk()
root.title("DJ Crossfade Transition")

# Buttons to load the two tracks
load_track1_btn = tk.Button(root, text="Load First Track", command=load_track1)
load_track1_btn.pack(pady=10)

load_track2_btn = tk.Button(root, text="Load Second Track", command=load_track2)
load_track2_btn.pack(pady=10)

# Run the GUI
root.mainloop()
