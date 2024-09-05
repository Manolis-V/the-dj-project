import pygame
import librosa
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
import time

# Initialize Pygame for audio playback
pygame.mixer.init()

# Global variables
current_sound = None
channel1 = pygame.mixer.Channel(0)
volume_meter = None
update_thread = None
is_playing = False
audio_data = None
sample_rate = None
chunk_size = 22050  # Size of the audio chunks (e.g., 1 second at 22.05kHz)

# Function to load and play the selected track
def load_track():
    global current_sound, is_playing, audio_data, sample_rate
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    
    if file_path:
        current_sound = pygame.mixer.Sound(file_path)
        channel1.play(current_sound)
        print("TRACK")
        is_playing = True
        
        # Load audio data once
        audio_data, sample_rate = librosa.load(file_path, sr=None, mono=True)
        
        start_volume_meter()  # Start updating the volume meter

# Function to calculate volume level for a chunk of audio data
def calculate_volume(chunk):
    rms = np.sqrt(np.mean(np.square(chunk)))
    return rms

# Function to update the volume meter
def update_volume_meter():
    global is_playing
    index = 3*chunk_size - 11025
    while is_playing:
        print("start")
        if audio_data is not None and sample_rate is not None:
            # Extract a chunk of audio data
            chunk = audio_data[index:index + chunk_size]
            index += chunk_size
            
            if len(chunk) == 0:
                # Restart from the beginning if we reach the end
                index = 0
                chunk = audio_data[index:index + chunk_size]
            
            # Compute volume level for the chunk
            volume = calculate_volume(chunk)
            # Update the progress bar
            volume_meter['value'] = min(volume * 100, 100)  # Scale volume to fit the progress bar
        time.sleep(0.05)

# Function to start updating the volume meter in a separate thread
def start_volume_meter():
    global update_thread
    if update_thread is None or not update_thread.is_alive():
        update_thread = threading.Thread(target=update_volume_meter, daemon=True)
        update_thread.start()

# Create the GUI
root = tk.Tk()
root.title("Audio Player with Volume Meter")

# Load track button
load_btn = tk.Button(root, text="Load Track", command=load_track)
load_btn.pack(pady=10)

# Volume meter (ttk.Progressbar)
volume_meter = ttk.Progressbar(root, orient="horizontal", length=400, mode='determinate')
volume_meter.pack(pady=10)

# Run the GUI
root.mainloop()
