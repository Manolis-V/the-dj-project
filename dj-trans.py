import pygame
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import librosa
#import matplotlib.pyplot as plt
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading
import gc
import numpy as np
from tkinter import *

# Initialize Pygame mixer
pygame.mixer.init()

# Load audio files
track1 = None
track2 = None
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)

is_transitioning = False
is_playing1, is_playing2, started1, started2 = False, False, False, False
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
    global track1, channel1, started1, is_playing1
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file_path:
        if channel1:
            channel1.stop()
        # is_playing1 = True
        # button1_pp.config(text="Pause")
        # Load and play the new track
        track1 = pygame.mixer.Sound(file_path)
        # channel1.play(track1)
        started1 = False
        volume3.set(volume3.get())
        
        file_name1 = Path(file_path).name
        file_name1 = file_name1.replace('.mp3', '')
        frame1_name.config(text=file_name1)

        # Find and display BPM
        # bpm = find_bpm(file_path)
        # bpm_label1.config(text=f"BPM: {int(bpm)}")


def load_track2():
    global track2, channel2, started2, is_playing2
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file_path:
        if channel2:
            channel2.stop()
        # is_playing2 = True
        # button2_pp.config(text="Pause")
        # Load and play the new track
        track2 = pygame.mixer.Sound(file_path)
        # channel2.play(track2)
        started2 = False
        volume3.set(volume3.get())
        
        file_name2 = Path(file_path).name
        file_name2 = file_name2.replace('.mp3', '')
        frame2_name.config(text=file_name2)
        
        # Find and display BPM
        # bpm = find_bpm(file_path)
        # bpm_label2.config(text=f"BPM: {int(bpm)}")

# Function to handle the crossfade transition
def trans(mode):
    global is_transitioning
    if track1 and track2:
        is_transitioning = True
        
        # Run the crossfade in a separate thread
        t1 = threading.Thread(target=lambda: crossfade_trans(mode))
        t1.start()
        
# Function to perform the crossfade
def crossfade_trans(mode):
    global is_transitioning, is_playing1, is_playing2
    fade_duration = mode  # Crossfade duration in seconds
    fade_steps = 100      # Number of steps in the fade
    step_duration = fade_duration / fade_steps

    if channel1.get_volume() == 1.0:
        print("1->2")
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
        channel1.set_volume(0)
        channel2.set_volume(1)
        # channel1.pause()
        # button1_pp.config(text="Play")
        # is_playing1 = False

    elif channel2.get_volume() == 1.0:
        print("2->1")
        for i in range(fade_steps):
            if not is_transitioning:
                break
            
            # Gradually reduce volume of channel1 (track1)
            current_volume2 = max(0, 1 - (i / fade_steps))  # Fade out
            channel2.set_volume(current_volume2)

            # Gradually increase volume of channel2 (track2)
            current_volume1 = min(1, i / fade_steps)  # Fade in
            channel1.set_volume(current_volume1)

            # Wait before updating again
            time.sleep(step_duration)

        # After crossfade, stop channel1 and let channel2 continue
        channel1.set_volume(1)
        channel2.set_volume(0)
        # channel2.pause()
        # button2_pp.config(text="Play")
        # is_playing2 = False
    
    is_transitioning = False
    print("done!")

def pause_resume1():
    global is_playing1, started1
    if is_playing1:
        channel1.pause()
        button1_pp.config(text="Play")
        is_playing1 = False
    elif is_playing1 == False and started1 == False:
        channel1.play(track1)
        button1_pp.config(text="Pause")
        is_playing1 = True
        started1 = True
    elif is_playing1 == False:
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
    global is_playing2, started2
    if is_playing2:
        channel2.pause()
        button2_pp.config(text="Play")
        is_playing2 = False
    elif is_playing2 == False and started2 == False:
        channel2.play(track2)
        button2_pp.config(text="Pause")
        is_playing2 = True
        started2 = True
    elif is_playing2 == False:
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



# Track 1 Controls
frame1 = ttk.LabelFrame(root, text="Track 1 Controls")
frame1.grid(row=0, column=0, padx=10, pady=10)

frame1_name = ttk.Label(frame1, text='')
frame1_name.grid(row=0, column=0, padx=10, pady=10)

button1_pp = ttk.Button(frame1, text="Play", command=pause_resume1)
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

frame2_name = ttk.Label(frame2, text='')
frame2_name.grid(row=0, column=0, padx=10, pady=10)

button2_pp = ttk.Button(frame2, text="Play", command=pause_resume2)
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
# ttk.Button(frame3, text="Start second Track and transition", command=lambda: trans(2.0)).grid(row=5, column=2, padx=10, pady=10)

ttk.Button(frame3, text="Small", command=lambda: trans(5.0)).grid(row=5, column=1, padx=5, pady=5)
ttk.Button(frame3, text="Mid", command=lambda: trans(8.0)).grid(row=5, column=2, padx=5, pady=5)
ttk.Button(frame3, text="Long", command=lambda: trans(12.0)).grid(row=5, column=3, padx=5, pady=5)

# Handle window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI loop
root.mainloop()
