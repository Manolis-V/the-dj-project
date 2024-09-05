import pygame
import librosa
import matplotlib.pyplot as plt
import numpy as np
import threading
import time
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import gc
# Initialize Pygame mixer for audio playback
pygame.mixer.init()

# Variables to store the loaded track and channel
track = None
channel = None
current_file_path = None


def plot_waveform(file_path, ax, playhead_position=0):
    gc.collect()
    y, sr = librosa.load(file_path, sr=None, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)
    
    ax.clear()
    
    # Plot the waveform
    ax.plot(y, color='blue')
    
    # Draw the playhead
    playhead_sample = int(playhead_position * sr)
    ax.axvline(playhead_sample, color='red', linestyle='--', label='Playhead')
    
    ax.set_xlim([0, len(y)])
    ax.set_ylim([-1, 1])
    ax.set_title("Waveform")
    ax.set_xlabel("Samples")
    ax.set_ylabel("Amplitude")
    
    ax.figure.canvas.draw()
    
    return duration


def update_waveform(channel, ax, duration, start_time):
    while channel.get_busy():
        current_time = time.time() - start_time
        playhead_position = (current_time / duration)*100
        
        print("duration: " , duration )
        print("\ncurrent_time: " , current_time)
        print("\nplayhead_position: " , playhead_position)
        plot_waveform(current_file_path, ax, playhead_position)
        
        time.sleep(0.05)  # Update every 50ms for a smooth transition


def load_and_play_track(file_path, ax):
    global track, channel, current_file_path
    current_file_path = file_path
    
    if channel:
        channel.stop()
    
    # Load and play the track
    track = pygame.mixer.Sound(file_path)
    channel = track.play()
    
    # Plot the initial waveform and get the duration
    duration = plot_waveform(file_path, ax)
    
    # Start the waveform update thread
    start_time = time.time()
    threading.Thread(target=update_waveform, args=(channel, ax, duration, start_time), daemon=True).start()




def load_track():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file_path:
        load_and_play_track(file_path, ax)

# Create the main window
root = tk.Tk()
root.title("Real-Time Waveform")

# Create a button to load the track
load_btn = tk.Button(root, text="Load Track", command=load_track)
load_btn.pack()

# Create the waveform plot
fig, ax = plt.subplots(figsize=(10, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Run the GUI loop
root.mainloop()
