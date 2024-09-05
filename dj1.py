import pygame
import tkinter as tk
from tkinter import ttk

# Initialize Pygame mixer
pygame.mixer.init()

# Load audio files
track1 = pygame.mixer.Sound("001.Katy Perry - I Kissed A Girl (Official Music Video).mp3")
track2 = pygame.mixer.Sound("004.Katy Perry - Hot N Cold (Official Music Video).mp3")

# Play tracks on separate channels
channel1 = track1.play(loops=-1)  # loops=-1 for infinite loop
channel2 = track2.play(loops=-1)

def pause_track1():
    channel1.pause()

def resume_track1():
    channel1.unpause()

def stop_track1():
    channel1.stop()

def pause_track2():
    channel2.pause()

def resume_track2():
    channel2.unpause()

def stop_track2():
    channel2.stop()

def stop_all_tracks():
    channel1.stop()
    channel2.stop()

# Create the main window
root = tk.Tk()
root.title("DJ Software Controls")

# Track 1 Controls
frame1 = ttk.LabelFrame(root, text="Track 1 Controls")
frame1.grid(row=0, column=0, padx=10, pady=10)

ttk.Button(frame1, text="Pause", command=pause_track1).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(frame1, text="Resume", command=resume_track1).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(frame1, text="Stop", command=stop_track1).grid(row=0, column=2, padx=5, pady=5)

# Track 2 Controls
frame2 = ttk.LabelFrame(root, text="Track 2 Controls")
frame2.grid(row=1, column=0, padx=10, pady=10)

ttk.Button(frame2, text="Pause", command=pause_track2).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(frame2, text="Resume", command=resume_track2).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(frame2, text="Stop", command=stop_track2).grid(row=0, column=2, padx=5, pady=5)

# Stop All Tracks
ttk.Button(root, text="Stop All Tracks", command=stop_all_tracks).grid(row=2, column=0, padx=10, pady=10)

# Run the GUI loop
root.mainloop()
