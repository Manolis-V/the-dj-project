import pygame
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import librosa
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading
import gc
import numpy as np
from tkinter import *

# Initialize Pygame mixer
pygame.mixer.init()

# Load audio files
track1_name = "001.Katy Perry - I Kissed A Girl (Official Music Video)"
track2_name = "002.Katy Perry - Teenage Dream (Official Music Video)"
track1 = pygame.mixer.Sound(track1_name + ".mp3")
track2 = pygame.mixer.Sound(track2_name + ".mp3")
temp1, temp2 = 1, 2
is_playing1, is_playing2 = True, True
vol1, vol2, crossfade_position = 1.0, 1.0, 1.0

    

def find_bpm(file_path):
    # Load the entire audio file
    y, sr = librosa.load(file_path, mono=True)  # Set duration=None to load the entire file
    # Estimate tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    del y, sr, _
    gc.collect() # Force garbage collection
    return tempo

# Function to calculate volume level for a chunk of audio data
def calculate_volume(chunk):
    rms = np.sqrt(np.mean(np.square(chunk)))
    return rms

def load_track1():
    global track1, channel1, current_file_path1, is_playing1
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file_path:
        if channel1:
            channel1.stop()
        is_playing1 = True
        button1_pp.config(text="Pause")
        # Load and play the new track
        track1 = pygame.mixer.Sound(file_path)
        channel1 = track1.play(loops=-1)

        volume3.set(volume3.get())
        
        file_name1 = Path(file_path).name
        file_name1 = file_name1.replace('.mp3', '')
        frame1_name.config(text=file_name1)

        # Find and display BPM
        # bpm = find_bpm(file_path)
        # bpm_label1.config(text=f"BPM: {int(bpm)}")


def load_track2():
    global track2, channel2, current_file_path2, is_playing2
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file_path:
        if channel2:
            channel2.stop()
        is_playing2 = True
        button2_pp.config(text="Pause")
        # Load and play the new track
        track2 = pygame.mixer.Sound(file_path)
        channel2 = track2.play(loops=-1)

        volume3.set(volume3.get())
        
        file_name2 = Path(file_path).name
        file_name2 = file_name2.replace('.mp3', '')
        frame2_name.config(text=file_name2)
        
        # Find and display BPM
        # bpm = find_bpm(file_path)
        # bpm_label2.config(text=f"BPM: {int(bpm)}")


def pause_resume1():
    global is_playing1
    if is_playing1:
        channel1.pause()
        button1_pp.config(text="Play")
        is_playing1 = False
    else:
        channel1.unpause()
        button1_pp.config(text="Pause")
        is_playing1 = True

def cue1():
    global is_playing1, channel1
    channel1.stop()
    channel1 = track1.play(0, 0)  # Restart from the beginning
    channel1.pause()  # Immediately pause it
    is_playing1 = False
    button1_pp.config(text="Play")

def pause_resume2():
    global is_playing2
    if is_playing2:
        channel2.pause()
        button2_pp.config(text="Play")
        is_playing2 = False
    else:
        channel2.unpause()
        button2_pp.config(text="Pause")
        is_playing2 = True

def cue2():
    global is_playing2, channel2
    channel2.stop()
    channel2 = track2.play(0, 0)  # Restart from the beginning
    channel2.pause()  # Immediately pause it
    is_playing2 = False
    button2_pp.config(text="Play")

def stop_all_tracks():
    global is_playing1, is_playing2
    channel1.pause()
    is_playing1 = False
    button1_pp.config(text="Play")
    channel2.pause()
    is_playing2 = False
    button2_pp.config(text="Play")

def on_closing():
    stop_all_tracks()
    pygame.mixer.quit()
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("DJ Software Controls")

# Volume Indicators

def volume1_cr(val):
    global vol1
    vol1 = float(val) / 100
    volume1 = vol1*(crossfade_position**0.8)
    channel1.set_volume(volume1)

def volume2_cr(val):
    global vol2
    vol2 = float(val) / 100
    volume2 = vol2*((1.0 - crossfade_position)**0.8)
    channel2.set_volume(volume2)

def set_crossfade(val):
    global crossfade_position
    crossfade_position = float(val) / 100
    
    if channel1 and channel2:  # Ensure both channels are loaded
        volume1 = (crossfade_position**0.8)*vol1
        volume2 = ((1.0 - crossfade_position)**0.8)*vol2
        
        channel1.set_volume(volume1)
        channel2.set_volume(volume2)
        
        volume_label1.config(text=f"Volume: {int(volume1 * 100)}%")
        volume_label2.config(text=f"Volume: {int(volume2 * 100)}%")

# Play tracks on separate channels
channel1 = track1.play(loops=-1)  # loops=-1 for infinite loop
channel2 = track2.play(loops=-1)


# Track 1 Controls
frame1 = ttk.LabelFrame(root, text="Track 1 Controls")
frame1.grid(row=0, column=0, padx=10, pady=10)

if temp1 == 1:
    frame1_name = ttk.Label(frame1, text='')
    frame1_name.grid(row=0, column=0, padx=10, pady=10)
    temp1 = 0

button1_pp = ttk.Button(frame1, text="Pause", command=pause_resume1)
button1_pp.grid(row=2, column=1, padx=5, pady=5)
button_cue2 = ttk.Button(frame1, text="Cue", command=cue1)
button_cue2.grid(row=2, column=2, padx=5, pady=5)

load_btn1 = ttk.Button(frame1, text="Load Track 1", command=load_track1)
load_btn1.grid(row=0, column=1, padx=10, pady=10)

bpm_label1 = ttk.Label(frame1, text="BPM: Unknown")
bpm_label1.grid(row=3, column=0, padx=10, pady=10)
volume_label1 = ttk.Label(frame1, text="Volume: 100%")
volume_label1.grid(row=3, column=1, padx=10, pady=10)


# Track 2 Controls
frame2 = ttk.LabelFrame(root, text="Track 2 Controls")
frame2.grid(row=0, column=2, padx=10, pady=10)

if temp2 == 2:
    frame2_name = ttk.Label(frame2, text='')
    frame2_name.grid(row=0, column=0, padx=10, pady=10)
    temp2 = 0

button2_pp = ttk.Button(frame2, text="Pause", command=pause_resume2)
button2_pp.grid(row=2, column=1, padx=5, pady=5)
button_cue2 = ttk.Button(frame2, text="Cue", command=cue2)
button_cue2.grid(row=2, column=2, padx=5, pady=5)

load_btn2 = ttk.Button(frame2, text="Load Track 2", command=load_track2)
load_btn2.grid(row=0, column=1, padx=10, pady=10)

bpm_label2 = ttk.Label(frame2, text="BPM: Unknown")
bpm_label2.grid(row=3, column=0, padx=10, pady=10)
volume_label2 = ttk.Label(frame2, text="Volume: 0%")
volume_label2.grid(row=3, column=1, padx=10, pady=10)


# Mixer
frame3 = ttk.LabelFrame(root, text="Mixer", labelanchor="n")
frame3.grid(row=0, column=1, padx=10, pady=10)

volume1 = ttk.Scale(frame3, from_=100, to=0, orient='vertical', command=volume1_cr)
volume1.set(100)  # Set initial volume to 100%
volume1.grid(row=2, column=0, padx=5, pady=5)

volume_meter1 = ttk.Progressbar(frame3, orient='vertical', mode='determinate')
volume_meter1.grid(row=2, column=1, padx=5, pady=5)

volume_meter2 = ttk.Progressbar(frame3, orient='vertical', mode='determinate')
volume_meter2.grid(row=2, column=3, padx=5, pady=5)

volume2 = ttk.Scale(frame3, from_=100, to=0, orient='vertical', command=volume2_cr)
volume2.set(100)  # Set initial volume to 100%
volume2.grid(row=2, column=4, padx=5, pady=5)

# crossfader
volume3 = ttk.Scale(frame3, from_=100, to=0, orient='horizontal', command=set_crossfade)
volume3.set(100)  # Set initial volume to 100%
volume3.grid(row=3, column=2, padx=5, pady=5)


# Stop All Tracks
ttk.Button(frame3, text="Stop All Tracks", command=stop_all_tracks).grid(row=4, column=2, padx=10, pady=10)

# Handle window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI loop
root.mainloop()
