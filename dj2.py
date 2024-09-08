import pygame
import tkinter as tk
import csv
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
from csv_conv import *
#from help_functions import *
# from display_csv import *

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
added_song = ''
added_song_name = ''
    

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

        track1 = pygame.mixer.Sound(file_path)
        started1 = False
        volume3.set(volume3.get())
        
        file_name1 = Path(file_path).name
        file_name1 = file_name1.replace('.mp3', '')
        frame1_name.config(text=file_name1)

        selected_item = tree.selection()
        bpm_ar1 = tree.item(selected_item, 'values')
        # Assuming the file name is in the first column
        bpm1 = bpm_ar1[2]  # Adjust the index if file name is in another column
        bpm_label1.config(text=f"Bpm: {bpm1}")

def added1():
    global track1, channel1, started1, is_playing1
        
    track1 = pygame.mixer.Sound("New folder/" + added_song)

    if channel1 and is_playing1:
        channel1.stop()
        
        channel1.play(track1)
        button1_pp.config(text="Pause")
        started1 = True
    else:
        started1 = False
        is_playing1 = False
        button1_pp.config(text="Play")

    volume3.set(volume3.get())
    frame1_name.config(text=added_song_name)


    selected_item = tree.selection()
    bpm_ar1 = tree.item(selected_item, 'values')
    # Assuming the file name is in the first column
    bpm1 = bpm_ar1[2]  # Adjust the index if file name is in another column
    bpm_label1.config(text=f"Bpm: {bpm1}")

def added2():
    global track2, channel2, started2, is_playing2
            
    track2 = pygame.mixer.Sound("New folder/" + added_song)

    if channel2 and is_playing2:
        channel2.stop()
        
        channel2.play(track2)
        button2_pp.config(text="Pause")
        started2 = True
    else:
        started2 = False
        is_playing2 = False
        button2_pp.config(text="Play")

    volume3.set(volume3.get())
    frame2_name.config(text=added_song_name)

    
    selected_item = tree.selection()
    bpm_ar2 = tree.item(selected_item, 'values')
    bpm2 = bpm_ar2[2]  # Adjust the index if file name is in another column
    bpm_label2.config(text=f"Bpm: {bpm2}")

def load_track2():
    global track2, channel2, started2, is_playing2
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file_path:
        if channel2:
            channel2.stop()

        track2 = pygame.mixer.Sound(file_path)
        started2 = False
        volume3.set(volume3.get())
        
        file_name2 = Path(file_path).name
        file_name2 = file_name2.replace('.mp3', '')
        frame2_name.config(text=file_name2)

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
            volume3.set(100-i)

        # After crossfade, stop channel1 and let channel2 continue
        channel1.set_volume(0)
        channel2.set_volume(1)
        volume3.set(0)

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
            volume3.set(i)

        # After crossfade, stop channel1 and let channel2 continue
        channel1.set_volume(1)
        channel2.set_volume(0)
        volume3.set(100)
    
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
# Function to load and display CSV in Treeview
def load_csv(mode=0):
    # Ask the user to select a CSV file
    if mode == 0:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    elif mode == 1:
        file_path = "C:/Users/manol/Desktop/New folder/c1.csv"
    
    if not file_path:
        return

    # Clear existing data in the Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Open the CSV file and read it
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Get the headers from the first row

        # Clear existing columns in the Treeview
        tree["columns"] = headers

        # Define columns and headings
        for header in headers:
            if header == 'File Name':
                tree.heading(header, text=header)
                tree.column(header, width=400)
            else:
                tree.heading(header, text=header)
                tree.column(header, width=100)

        # Add rows to the Treeview
        for row in reader:
            tree.insert("", tk.END, values=row)

# Function to handle double-click event and print file name
def on_double_click(event):
    global added_song, added_song_name
    # Get the item selected by the user
    selected_item = tree.selection()
    if selected_item:
        # Get the values of the selected row
        item_values = tree.item(selected_item, 'values')
        # Assuming the file name is in the first column
        file_name = item_values[0]  # Adjust the index if file name is in another column
        added_song = file_name
        added_song_name = file_name
        print(f"File Name: {file_name}")

# Track 1 Controls
frame1 = ttk.LabelFrame(root, text="Track 1 Controls")
frame1.grid(row=0, column=0, padx=10, pady=10, sticky="news")

frame1_name = ttk.Label(frame1, text='')
frame1_name.grid(row=0, column=0, padx=10, pady=10)

button1_pp = ttk.Button(frame1, text="Play", command=pause_resume1)
button1_pp.grid(row=2, column=1, padx=5, pady=5)
button_cue2 = ttk.Button(frame1, text="Cue", command=cue1)
button_cue2.grid(row=2, column=2, padx=5, pady=5)

load_btn1 = ttk.Button(frame1, text="Load Track 1", command=load_track1)
load_btn1.grid(row=0, column=1, padx=10, pady=10)

add_btn1 = ttk.Button(frame1, text="Add Track 1", command=added1)
add_btn1.grid(row=0, column=2, padx=10, pady=10)

bpm_label1 = ttk.Label(frame1, text="BPM: Unknown")
bpm_label1.grid(row=3, column=0, padx=10, pady=10)
volume_label1 = ttk.Label(frame1, text="Volume: 100%")
volume_label1.grid(row=3, column=1, padx=10, pady=10)


# Track 2 Controls
frame2 = ttk.LabelFrame(root, text="Track 2 Controls")
frame2.grid(row=0, column=2, padx=10, pady=10, sticky="news")

frame2_name = ttk.Label(frame2, text='')
frame2_name.grid(row=0, column=0, padx=10, pady=10)

button2_pp = ttk.Button(frame2, text="Play", command=pause_resume2)
button2_pp.grid(row=2, column=1, padx=5, pady=5)
button_cue2 = ttk.Button(frame2, text="Cue", command=cue2)
button_cue2.grid(row=2, column=2, padx=5, pady=5)

load_btn2 = ttk.Button(frame2, text="Load Track 2", command=load_track2)
load_btn2.grid(row=0, column=1, padx=10, pady=10)

add_btn2 = ttk.Button(frame2, text="Add Track 2", command=added2)
add_btn2.grid(row=0, column=2, padx=10, pady=10)

bpm_label2 = ttk.Label(frame2, text="BPM: Unknown")
bpm_label2.grid(row=3, column=0, padx=10, pady=10)
volume_label2 = ttk.Label(frame2, text="Volume: 0%")
volume_label2.grid(row=3, column=1, padx=10, pady=10)


# Mixer
frame3 = ttk.LabelFrame(root, text="Mixer", labelanchor="n")
frame3.grid(row=0, column=1, padx=10, pady=10, sticky="news")

volume1 = ttk.Scale(frame3, from_=100, to=0, orient='vertical', command=volume1_cr)
volume1.set(100)  # Set initial volume to 100%
volume1.grid(row=2, column=0, padx=5, pady=5)

volume2 = ttk.Scale(frame3, from_=100, to=0, orient='vertical', command=volume2_cr)
volume2.set(100)  # Set initial volume to 100%
volume2.grid(row=2, column=4, padx=5, pady=5)

# crossfader
volume3 = ttk.Scale(frame3, from_=100, to=0, orient='horizontal', command=set_crossfade)
volume3.set(100)  # Set initial volume to 100%
volume3.grid(row=3, column=2, padx=5, pady=5)


# Stop All Tracks
ttk.Button(frame3, text="Stop All Tracks", command=stop_all_tracks).grid(row=4, column=2, padx=10, pady=10)
ttk.Button(frame3, text="Small", command=lambda: trans(5.0)).grid(row=5, column=1, padx=5, pady=5)
ttk.Button(frame3, text="Mid", command=lambda: trans(8.0)).grid(row=5, column=2, padx=5, pady=5)
ttk.Button(frame3, text="Long", command=lambda: trans(12.0)).grid(row=5, column=3, padx=5, pady=5)
ttk.Button(frame3, text="Save Playlist to CSV", command=save_as_csv).grid(row=6, column=1, padx=5, pady=5)

# Button to load and display the CSV
load_button = ttk.Button(frame3, text="Load CSV", command=load_csv)
load_button.grid(row=6, column=3, pady=10)

frame4 = ttk.LabelFrame(root, text="grid")
frame4.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
# Create the Treeview widget
tree = ttk.Treeview(frame4, show="headings")
tree.grid(row=1, column=0)
load_csv(1)

# Add a scrollbar
scrollbar = ttk.Scrollbar(frame4, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=1, column=3, sticky="ns")

# Bind the double-click event to the Treeview
tree.bind("<Button-1>", on_double_click)

# Handle window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI loop
root.mainloop()