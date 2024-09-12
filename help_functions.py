import tkinter as tk
from tkinter import ttk
import pygame

# Initialize Pygame mixer
pygame.mixer.init()

# Load an audio file (example)
file_path = "2Pole - Troja (Clean) (Extended).mp3"
song  = pygame.mixer.music
song.load(file_path)
# Create the main application window
root = tk.Tk()
root.title("Song Progress Slider")

# Global variables to track song's total length and update status
total_duration = 0
is_updating_slider = False
bef = 0
step = 0.0001

# Function to update the progress slider
def update_slider():
    global step, song
    if not is_updating_slider:
        current_pos = step / total_duration # Current position in seconds
        step = step + 0.25
        time = song.get_pos() / 1000
        print(time)
        if current_pos > 0:  # Avoid updating slider when music is not playing
            progress_slider.set(time)
            #print("current_pos", current_pos)
            current_pos = round(time, 2)
            dur2.config(text=f"{time}/-")
    
    if pygame.mixer.music.get_busy():
        root.after(250, update_slider)  # Update slider every 500 ms

# Function to seek the song when the slider is moved by the user
def seek_song(event):
    global is_updating_slider, bef, song
    is_updating_slider = True
    seek_time = progress_slider.get()
    bef = song.get_pos() / 1000
    # Stop the song and play it from the seek position
    song.stop()  # Stop the current song
    song.load(file_path)
    song.play(start=seek_time)  # Restart the song from the seek time
    is_updating_slider = False

# Function to start playing the song
def play_song():
    global total_duration, step, song
    song.play()
    # Get total duration of the song using pygame.mixer.Sound
    total_duration = pygame.mixer.Sound(file_path).get_length()  # Get total duration of the song
    print("total_duration", total_duration)
    progress_slider.config(to=total_duration)  # Set the scale range to the song's total length
    update_slider()  # Start updating the slider as the song plays

# Create a play button
play_button = tk.Button(root, text="Play", command=play_song)
play_button.grid(row=0, column=0, padx=10, pady=10)

# Create a progress slider
progress_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=300, style="TScale")
progress_slider.grid(row=1, column=0, padx=10, pady=10)
dur2 = ttk.Label(root, text="-/-")
dur2.grid(row=1, column=0, padx=10, pady=10)

# Bind the slider to seek functionality
progress_slider.bind("<ButtonRelease-1>", seek_song)

# Run the Tkinter event loop
root.mainloop()

# Quit pygame mixer on exit
pygame.mixer.quit()
