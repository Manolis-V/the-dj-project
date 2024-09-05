import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pygame
import threading
import time

# Initialize Pygame for audio playback
pygame.mixer.init()

# Global variables
track_length = 0
is_playing = False
progress_bar = None
update_thread = None

# Function to load and play the selected track
def load_track():
    global track_length, is_playing
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    
    if file_path:
        pygame.mixer.music.load(file_path)  # Load the track
        pygame.mixer.music.play()  # Play the track
        track_length = pygame.mixer.Sound(file_path).get_length()  # Get track length
        is_playing = True
        start_progress_bar()  # Start updating the progress bar

# Function to update the progress bar
def update_progress():
    while is_playing:
        current_time = pygame.mixer.music.get_pos() / 1000  # Get current playback time in seconds
        if current_time >= 0:
            progress_bar['value'] = (current_time / track_length) * 100  # Update progress bar
        time.sleep(0.1)

# Function to start updating the progress bar in a separate thread
def start_progress_bar():
    global update_thread
    if update_thread is None or not update_thread.is_alive():
        update_thread = threading.Thread(target=update_progress, daemon=True)
        update_thread.start()

# Function to pause and resume the track
def toggle_pause_resume():
    global is_playing
    if is_playing:
        pygame.mixer.music.pause()
        is_playing = False
    else:
        pygame.mixer.music.unpause()
        is_playing = True
        start_progress_bar()

# Create the GUI
root = tk.Tk()
root.title("Audio Player with Progress Bar")

# Load track button
load_btn = tk.Button(root, text="Load Track", command=load_track)
load_btn.pack(pady=10)

# Play/Pause button
play_pause_btn = tk.Button(root, text="Play/Pause", command=toggle_pause_resume)
play_pause_btn.pack(pady=10)

# Progress bar using ttk
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="indeterminate")
progress_bar.pack(pady=10)
# Run the GUI
root.mainloop()
