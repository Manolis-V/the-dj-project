import pygame
import tkinter as tk
import csv
from tkinter import ttk, filedialog
from pathlib import Path
import time
import threading
import numpy as np
from fuzzywuzzy import fuzz
from tkinter import *
from csv_conv import *

# Initialize Pygame mixer
pygame.mixer.init()

# Load audio files
track1 = None
track2 = None
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)

is_transitioning = False
songs_played = []
is_playing1, is_playing2, started1, started2, auto, done, full_auto = False, False, False, False, False, False, False
vol1, vol2, crossfade_position, start_time1, pause_time1, start_time2, pause_time2, duration1, duration2, song_id, key1, key2 = 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 1, '', ''
added_song, added_song_name, directory_path, pool = '', '', '', ''


# loads trackes using the folders
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

def added1(item_data=0):
    global track1, channel1, started1, is_playing1, start_time1, pause_time1, duration1
    
    track1 = pygame.mixer.Sound("../music-for-the-dj-project/music/"+ pool + "/" + added_song)

    if channel1 and is_playing1:
        channel1.stop()
        
        channel1.play(track1)
        button1_pp.config(text="Pause")
        started1 = True

    else:
        started1 = False
        is_playing1 = False
        button1_pp.config(text="Play")

    pause_time1 = 0.0
    start_time1 = time.time()
    volume3.set(volume3.get())
    frame1_name.config(text=added_song)

    if item_data == 0:
        selected_item = tree.selection()
        item_data = tree.item(selected_item, 'values')
    # Assuming the file name is in the first column
    bpm1 = item_data[2]  # Adjust the index if file name is in another column
    key1 = item_data[4]
    duration1 = item_data[1]
    bpm_label1.config(text=f"Bpm: {bpm1}")
    key_label1.config(text=f"KEY: {key1}")
    dur1.config(text=f"-/{duration1}")

def added2(item_data=0):
    global track2, channel2, started2, is_playing2, pause_time2, start_time2, duration2

    track2 = pygame.mixer.Sound("../music-for-the-dj-project/music/"+ pool + "/" + added_song)
    
    if channel2 and is_playing2:
        channel2.stop()
        channel2.play(track2)
        button2_pp.config(text="Pause")
        started2 = True
    else:
        started2 = False
        is_playing2 = False
        button2_pp.config(text="Play")

    pause_time2 = 0.0
    start_time2 = time.time()
    volume3.set(volume3.get())
    frame2_name.config(text=added_song)

    if item_data == 0:
        selected_item = tree.selection()
        item_data = tree.item(selected_item, 'values')
    bpm2 = item_data[2]  # Adjust the index if file name is in another column
    duration2 = item_data[1]
    key2 = item_data[4]
    bpm_label2.config(text=f"Bpm: {bpm2}")
    key_label2.config(text=f"KEY: {key2}")
    dur2.config(text=f"-/{duration2}")

# loads trackes using the folders
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
    print("trans")
    if track1 and track2:
        is_transitioning = True
        
        # Run the crossfade in a separate thread
        t1 = threading.Thread(target=lambda: crossfade_trans(mode))
        t1.start()

def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v = list(d.values())
     k = list(d.keys())
     return k[v.index(max(v))]

def pick_id(bpm_of_the_curr, key_of_the_curr, duration_of_the_curr):
    global song_id, songs_played
    huristics = {}

    for child in tree.get_children():
        item_data = tree.item(child)["values"]
        bpm = item_data[2]
        duration = item_data[1]
        key = item_data[4]
        song_id = item_data[5]
        score = 0

        """analises the songs that are not in the list of played songs"""
        if song_id not in songs_played:

            if bpm == bpm_of_the_curr:
                score = score + 7
            if bpm in range((bpm_of_the_curr-2),(bpm_of_the_curr+2)):
                score = score + 4
            if bpm in range((bpm_of_the_curr-5),(bpm_of_the_curr+5)):
                score = score + 2

            score = score + fuzz.ratio(key, key_of_the_curr)/10

            if duration in range((duration_of_the_curr-10),(duration_of_the_curr+10)):
                score = score + 3
            if duration in range((duration_of_the_curr-15),(duration_of_the_curr+15)):
                score = score + 2
            if duration in range((duration_of_the_curr-25),(duration_of_the_curr+25)):
                score = score + 1

            huristics[song_id] = score

    song_id = keywithmaxval(huristics)
    songs_played.append(song_id)
    print("The song with highest score: ", song_id)

# loads songs automaticaly after trans
def pick_song(deck):
    global song_id, added_song

    for child in tree.get_children():
        if tree.item(child)["values"][0] == added_song:     #finds the song playing
            item_data = tree.item(child)["values"]
            break

    pick_id(item_data[2], item_data[4], item_data[1])       #sends it to analise and changes song_id
    if deck == 1:
        print("deck ", deck)
        for child in tree.get_children():
            if tree.item(child)["values"][5] == song_id:    #searches new song_id
                item_data = tree.item(child)["values"]
                added_song = item_data[0]
                print("deck: 1, adding song: ", added_song)
                added1(item_data)
    elif deck == 2:
        print("deck ", deck)
        for child in tree.get_children():
            if tree.item(child)["values"][5] == song_id:
                item_data = tree.item(child)["values"]
                added_song = item_data[0]
                print("deck: 2, adding song: ", added_song)
                added2(item_data)
    
# Function to perform the crossfade
def crossfade_trans(mode):
    global is_transitioning, is_playing1, is_playing2, done
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
        if auto == True:
            pause_resume1()     # pauses after trans
            pick_song(1)

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
        if auto == True:
            pause_resume2()     # pauses after trans
            pick_song(2)
    
    done = False
    is_transitioning = False
    print("done!")
    if full_auto == True:
        auto_play()

"""
    A lot is happening here, the main controls are taking place here
    This function is running on a thread
"""
def update_time1():
    global channel1, track1, is_playing1, start_time1, pause_time1, done, duration1
    curr_time = time.time() - start_time1
    if channel1 and is_playing1:
        
        curr_time = round(curr_time, 3)
        
        dur1.config(text=f"{curr_time}/{duration1}")

        if auto == True:
            if curr_time >= (int(duration1)/12) and curr_time <= (int(duration1)/12) + 0.3 and not done:
                print("calling  trans")
                done = TRUE
                pause_resume2()
                trans(int(duration1)/24)

    if not is_playing1:
        pause_time1 = curr_time
        print(pause_time1)
        return
    if channel1.get_busy():
        root.after(250, update_time1)  # Update slider every 500 ms

"""
    A lot is happening here, the main controls are taking place here
    This function is running on a thread
"""
def update_time2():
    global channel2, track2, is_playing2, start_time2, pause_time2, done, duration2
    curr_time = time.time() - start_time2
    if channel2 and is_playing2:
        
        curr_time = round(curr_time, 3)
        
        dur2.config(text=f"{curr_time}/{duration2}")

        if auto == True:
            if curr_time >= (int(duration2)/12) and curr_time <= (int(duration2)/12) + 0.3 and not done:
                print("calling trans")
                done = TRUE
                pause_resume1()
                trans(int(duration1)/24)

    if not is_playing2:
        pause_time2 = curr_time
        print(pause_time2)
        return
    if channel2.get_busy():
        root.after(250, update_time2)  # Update slider every 500 ms


"""
    When calling this function it automaticaly pauses/playes, stops/continues time
"""
def pause_resume1():
    global is_playing1, started1, start_time1
    if is_playing1:
        channel1.pause()
        button1_pp.config(text="Play")
        is_playing1 = False
        
        t2 = threading.Thread(target=update_time1)
        t2.start()

    # when it was on cue or just loaded
    elif is_playing1 == False and started1 == False:
        channel1.play(track1)
        button1_pp.config(text="Pause")
        is_playing1 = True
        started1 = True
        start_time1 = time.time() - pause_time1
        t2 = threading.Thread(target=update_time1)
        t2.start()
        
        volume3.set(volume3.get())

    elif is_playing1 == False:
        channel1.unpause()
        button1_pp.config(text="Pause")
        is_playing1 = True
        start_time1 = time.time() - pause_time1
        t2 = threading.Thread(target=update_time1)
        t2.start()

"""
    When calling this function it automaticaly pauses/playes, stops/continues time
"""
def pause_resume2():
    global is_playing2, started2, start_time2
    if is_playing2:
        channel2.pause()
        button2_pp.config(text="Play")
        is_playing2 = False

        t3 = threading.Thread(target=update_time2)
        t3.start()

    # when it was on cue or just loaded
    elif is_playing2 == False and started2 == False:
        channel2.play(track2)
        button2_pp.config(text="Pause")
        is_playing2 = True
        started2 = True
        
        start_time2 = time.time() - pause_time2
        t3 = threading.Thread(target=update_time2)
        t3.start()

        volume3.set(volume3.get())
    elif is_playing2 == False:
        channel2.unpause()
        button2_pp.config(text="Pause")
        is_playing2 = True

        start_time2 = time.time() - pause_time2
        t3 = threading.Thread(target=update_time2)
        t3.start()

def cue1():
    global is_playing1, channel1, pause_time1, start_time1, started1
    channel1.stop()
    channel1 = track1.play(0, 0)  # Restart from the beginning
    channel1.pause()  # Immediately pause it

    is_playing1 = False
    button1_pp.config(text="Play")
    started1 = False

    pause_time1 = 0.0
    start_time1 = time.time()
    selected_item = tree.selection()
    bpm_ar1 = tree.item(selected_item, 'values')
    duration1 = bpm_ar1[1]
    dur1.config(text=f"0.0/{duration1}")

def cue2():
    global is_playing2, channel2, pause_time2, start_time2, started2
    channel2.stop()
    channel2 = track2.play(0, 0)  # Restart from the beginning
    channel2.pause()  # Immediately pause it

    is_playing2 = False
    button2_pp.config(text="Play")
    started2 = False

    pause_time2 = 0.0
    start_time2 = time.time()
    selected_item = tree.selection()
    bpm_ar2 = tree.item(selected_item, 'values')
    duration2 = bpm_ar2[1]
    dur2.config(text=f"0.0/{duration2}")

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

"""
    loads the main csv with the directiories
"""
def load_dir(mode=0):

    file_path = ''
    if mode == 0:
        load_csv(2)
    elif mode == 1:
        file_path = "C:/Users/manol/Documents/git/music-for-the-dj-project/music/csvs/music.csv"
    if not file_path:
        return
    # Clear existing data in the Treeview
    for row in tree1.get_children():
        tree1.delete(row)

        # Open the CSV file and read it
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Get the headers from the first row

        # Clear existing columns in the Treeview
        tree1["columns"] = headers

        # Define columns and headings
        for header in headers:
            if header == 'path':
                tree1.heading(header, text=header)
                tree1.column(header, width=100, stretch=False)
        # Add rows to the Treeview
        for row in reader:
            tree1.insert("", tk.END, values=row)


"""
    mode == 0 : loads a directory from file explorer
    mode == 1 : loads a hard coded directory
    mode == 2 : loads the directory selected based on the pool variable
"""
def load_csv(mode=0):
    global pool
    # Ask the user to select a CSV file
    if mode == 0:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    elif mode == 1:
        file_path = "C:/Users/manol/Documents/git/music-for-the-dj-project/music/csvs/pool1.csv"
        pool = "pool1"
    elif mode == 2:
        file_path = "C:/Users/manol/Documents/git/music-for-the-dj-project/music/csvs/" + pool + ".csv"
        
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
                # print(100)
                tree.heading(header, text=header)
                tree.column(header, width=300, stretch=False)
            elif header == 'id':
                # print(110)
                tree.heading(header, text=header)
                tree.column(header, width=30, stretch=False)
            else:
                # print(101)
                tree.heading(header, text=header)
                tree.column(header, width=100, stretch=False)

        # Add rows to the Treeview
        for row in reader:
            tree.insert("", tk.END, values=row)

# Function to handle double-click event and print file name
def on_double_click(event):
    global added_song, added_song_name
    # Get the item selected by the user
    print(1)
    selected_item = tree.selection()
    if selected_item:
        print(2)
        # Get the values of the selected row
        item_values = tree.item(selected_item, 'values')
        # Assuming the file name is in the first column
        file_name = item_values[0]  # Adjust the index if file name is in another column
        added_song = file_name
        added_song_name = file_name
        print(f"File Name: {file_name}")
# Function to handle double-click event and print file name
def on_double_click2(event):
    global pool
    # Get the item selected by the user
    selected_item = tree1.selection()
    if selected_item:
        # Get the values of the selected row
        item_values = tree1.item(selected_item, 'values')
        # Assuming the file name is in the first column
        file_name = item_values[0]  # Adjust the index if file name is in another column
        pool = file_name
        print(f"File Name: {file_name}")
        load_dir()


def auto_added1(item_data):
    global track1, channel1, started1, is_playing1, start_time1, pause_time1, duration1
        
    track1 = pygame.mixer.Sound("New folder/" + added_song)

    if channel1 and is_playing1:
        channel1.stop()
    channel1.play(track1)
    button1_pp.config(text="Pause")
    started1 = True
    is_playing1 = True
    pause_time1 = 0.0
    start_time1 = time.time()
    volume3.set(volume3.get())
    frame1_name.config(text=added_song_name)

    bpm1 = item_data[2]  # Adjust the index if file name is in another column
    bpm_label1.config(text=f"Bpm: {bpm1}")
    duration1 = item_data[1]
    dur1.config(text=f"-/{duration1}")

    start_time1 = time.time() - pause_time1
    t2 = threading.Thread(target=update_time1)
    t2.start()

def auto_added2(item_data):
    global track2, channel2, started2, is_playing2, start_time2, pause_time2, duration2
        
    track2 = pygame.mixer.Sound("New folder/" + added_song)

    if channel2 and is_playing2:
        channel2.stop()
    channel2.play(track2)
    button2_pp.config(text="Pause")
    started2 = True
    is_playing2 = True
    pause_time2 = 0.0
    start_time2 = time.time()
    volume3.set(volume3.get())
    frame2_name.config(text=added_song_name)

    bpm2 = item_data[2]  # Adjust the index if file name is in another column
    bpm_label2.config(text=f"Bpm: {bpm2}")
    duration2 = item_data[1]
    dur2.config(text=f"-/{duration2}")

    start_time2 = time.time() - pause_time2
    t2 = threading.Thread(target=update_time2)
    t2.start()

def auto_play():
    global started1, started2, song_id, added_song, added_song_name, full_auto
    deck = 1
    full_auto = True
    print("autoplay")
    if deck == 1:
        print("deck ", deck)
        for child in tree.get_children():
            if tree.item(child)["values"][5] == song_id:
                item_data = tree.item(child)["values"]
                added_song = item_data[0]
                added_song_name = added_song
                
                deck = 2
                auto_added1(item_data)
                print(f"File Name: {added_song}")
    elif deck == 2:
        print("deck ", deck)
        for child in tree.get_children():
            if tree.item(child)["values"] == song_id:
                item_data = tree.item(child)["values"]
                added_song = item_data[0]
                added_song_name = added_song
                
                deck = 2
                auto_added2(item_data)
                print(f"File Name: {added_song}")
    song_id = song_id + 1

def init_songs():
    automoto()

def automoto():
    global auto
    if auto:
        auto = False
        auto_bb.config(text="Auto: off")
    else:
        auto = True
        auto_bb.config(text="Auto: on")
    print(auto)



# Track 1 Controls
frame1 = ttk.LabelFrame(root, text="Track 1 Controls")
frame1.grid(row=0, column=0, padx=10, pady=10, sticky="news")

frame1_name = ttk.Label(frame1, text='')
frame1_name.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

button1_pp = ttk.Button(frame1, text="Play", command=pause_resume1)
button1_pp.grid(row=2, column=1, padx=5, pady=5)
button_cue2 = ttk.Button(frame1, text="Cue", command=cue1)
button_cue2.grid(row=2, column=2, padx=5, pady=5)

# load_btn1 = ttk.Button(frame1, text="Load Track 1", command=load_track1)
# load_btn1.grid(row=0, column=1, padx=10, pady=10)

add_btn1 = ttk.Button(frame1, text="Add Track 1", command=added1)
add_btn1.grid(row=0, column=2, padx=10, pady=10)

bpm_label1 = ttk.Label(frame1, text="BPM: Unknown")
bpm_label1.grid(row=3, column=0, padx=10, pady=10)
key_label1 = ttk.Label(frame1, text="KEY: Unknown")
key_label1.grid(row=4, column=0, padx=10, pady=10)
volume_label1 = ttk.Label(frame1, text="Volume: 100%")
volume_label1.grid(row=3, column=1, padx=10, pady=10)
dur1 = ttk.Label(frame1, text="-/-")
dur1.grid(row=3, column=2, padx=10, pady=10)
# move_forward_btn1 = ttk.Button(frame1, text="+15s", command=move_forward1)
# move_forward_btn1.grid(row=4, column=2, padx=10, pady=10)

progress_bar1 = ttk.Scale(frame1, from_=0, to=100, orient="horizontal", length=300, style="TScale")
progress_bar1.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Track 2 Controls
frame2 = ttk.LabelFrame(root, text="Track 2 Controls")
frame2.grid(row=0, column=2, padx=10, pady=10, sticky="news")

frame2_name = ttk.Label(frame2, text='')
frame2_name.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

button2_pp = ttk.Button(frame2, text="Play", command=pause_resume2)
button2_pp.grid(row=2, column=1, padx=5, pady=5)
button_cue2 = ttk.Button(frame2, text="Cue", command=cue2)
button_cue2.grid(row=2, column=2, padx=5, pady=5)

# load_btn2 = ttk.Button(frame2, text="Load Track 2", command=load_track2)
# load_btn2.grid(row=0, column=1, padx=10, pady=10)

add_btn2 = ttk.Button(frame2, text="Add Track 2", command=added2)
add_btn2.grid(row=0, column=2, padx=10, pady=10)

bpm_label2 = ttk.Label(frame2, text="BPM: Unknown")
bpm_label2.grid(row=3, column=0, padx=10, pady=10)
key_label2 = ttk.Label(frame2, text="KEY: Unknown")
key_label2.grid(row=4, column=0, padx=10, pady=10)
volume_label2 = ttk.Label(frame2, text="Volume: 0%")
volume_label2.grid(row=3, column=1, padx=10, pady=10)
dur2 = ttk.Label(frame2, text="-/-")
dur2.grid(row=3, column=2, padx=10, pady=10)

progress_bar2 = ttk.Scale(frame2, from_=0, to=100, orient="horizontal", length=300, style="TScale")
progress_bar2.grid(row=5, column=0, columnspan=3, padx=10, pady=10)


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
ttk.Button(frame3, text="init", command=init_songs).grid(row=4, column=3, padx=5, pady=5)
ttk.Button(frame3, text="Small", command=lambda: trans(5.0)).grid(row=5, column=1, padx=5, pady=5)
ttk.Button(frame3, text="Mid", command=lambda: trans(8.0)).grid(row=5, column=2, padx=5, pady=5)
ttk.Button(frame3, text="Long", command=lambda: trans(12.0)).grid(row=5, column=3, padx=5, pady=5)
ttk.Button(frame3, text="Save Playlist to CSV", command=save_as_csv).grid(row=6, column=2, padx=5, pady=5)
auto_bb = ttk.Button(frame3, text="Auto: off", command=automoto)
auto_bb.grid(row=6, column=1, padx=5, pady=5)

# Button to load and display the CSV
load_button = ttk.Button(frame3, text="Load CSV", command=load_csv)
load_button.grid(row=6, column=3, pady=10)

frame4 = ttk.LabelFrame(root, text="pools")
frame4.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# frame5 = ttk.LabelFrame(root, text="dirs")
# frame5.grid(row=2, column=0, padx=10, pady=10)
tree1 = ttk.Treeview(frame4, show="headings")
tree1.grid(row=0, column=0)
# Create the Treeview widget
tree = ttk.Treeview(frame4, show="headings")
tree.grid(row=0, column=1)
load_dir(1)
load_csv(1)
# auto_play()
# Add a scrollbar
scrollbar = ttk.Scrollbar(frame4, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=2, sticky="nsew")

# Bind the double-click event to the Treeview
tree.bind('<Double-Button-1>', on_double_click)

tree1.bind("<Button-1>", on_double_click2)

# Handle window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI loop
root.mainloop()