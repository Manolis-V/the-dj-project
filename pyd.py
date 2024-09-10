import tkinter as tk
from tkinter import ttk
from pydub import AudioSegment
import simpleaudio as sa
import time

# Create the main application window
root = tk.Tk()
root.title("Music Player with Slider (pydub)")

# Load audio using pydub
file_path = "2Pole - Troja (Clean) (Extended).mp3"
audio = AudioSegment.from_file(file_path)
total_duration = len(audio) / 1000  # Duration in seconds

# Variables to control playback and position
play_obj = None  # simpleaudio play object
is_playing = False
current_position = 0  # Current position in milliseconds
is_updating_slider = False

# Function to play audio
def play_audio(start_position=0):
    global play_obj, is_playing, current_position
    if play_obj:
        play_obj.stop()  # Stop previous playback if exists
    
    # Extract the portion of the audio to play from the seeked position
    segment_to_play = audio[start_position:]
    play_obj = sa.play_buffer(
        segment_to_play.raw_data,
        num_channels=segment_to_play.channels,
        bytes_per_sample=segment_to_play.sample_width,
        sample_rate=segment_to_play.frame_rate
    )
    is_playing = True
    current_position = start_position / 1000  # Start from this position in seconds
    update_slider()

# Function to pause audio
def pause_audio():
    global is_playing
    if play_obj:
        play_obj.stop()  # Stop the audio playback
    is_playing = False

# Function to update the slider position
def update_slider():
    global current_position, is_playing
    if is_playing and not is_updating_slider:
        current_position += 0.1  # Update by 0.1 seconds (100ms)
        progress_slider.set(current_position)
        
        if current_position < total_duration:
            root.after(100, update_slider)  # Update slider every 100ms
        else:
            is_playing = False  # Stop updating when song finishes

# Function to seek when the slider is moved
def seek_audio(event):
    global is_updating_slider, current_position
    is_updating_slider = True
    seek_time = progress_slider.get() * 1000  # Convert to milliseconds
    current_position = seek_time / 1000
    play_audio(start_position=seek_time)
    is_updating_slider = False

# Function to start playing the song
def start_playing():
    play_audio(start_position=0)

# Function to stop the song
def stop_playing():
    global is_playing
    if play_obj:
        play_obj.stop()
    is_playing = False
    progress_slider.set(0)

# Create play, pause, and stop buttons
play_button = tk.Button(root, text="Play", command=start_playing)
play_button.grid(row=0, column=0, padx=10, pady=10)

pause_button = tk.Button(root, text="Pause", command=pause_audio)
pause_button.grid(row=0, column=1, padx=10, pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_playing)
stop_button.grid(row=0, column=2, padx=10, pady=10)

# Create a progress slider
progress_slider = ttk
