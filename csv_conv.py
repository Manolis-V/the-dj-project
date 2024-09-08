import csv
import os
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
from tkinter import filedialog
import tkinter as tk

# Function to get the metadata of a song
def get_song_metadata(file_path):
    try:
        audio = MP3(file_path)
        # Extract metadata
        title = audio.tags.get("TIT2", "Unknown Title")
        artist = audio.tags.get("TPE1", "Unknown Artist")
        genre = audio.tags.get("TCON", "Unknown Genre")
        duration = int(audio.info.length)
        bpm = audio.tags.get("TBPM", "Unknown bpm")
        key = str(audio.tags.get("TKEY", "Unknown key").text[0])
        return {
            "Title": title,
            "Artist": artist,
            "Duration": duration,
            "bpm" : bpm,
            "genre" : genre,
            "key" : key
        }
    except Exception as e:
        print(f"Error getting metadata for {file_path}: {e}")
        return None

# Dictionary containing musical keys
def key_conv(key):
    music_dict = {
        "Abm" : "1A",
        "Ebm" : "2A",
        "Bbm" : "3A",
        "Fm" : "4A",
        "Cm" : "5A",
        "Gm" : "6A",
        "Dm" : "7A",
        "Am" : "8A",
        "Em" : "9A",
        "Bm" : "10A",
        "Gbm" : "11A",
        "Dbm" : "12A",
        "B" : "1B",
        "Gb" : "2B",
        "Db" : "3B",
        "Ab" : "4B",
        "Eb" : "5B",
        "Bb" : "6B",
        "F" : "7B",
        "C" : "8B",
        "G" : "9B",
        "D" : "10B",
        "A" : "11B",
        "E" : "12B"
    }
    return music_dict.get(key)

# Function to save the playlist to a CSV
def save_playlist_to_csv(playlist, output_file):

    # Define CSV columns
    # fieldnames = ["File Name", "Title", "Artist", "Duration (seconds)", "bpm", "genre", "key"]
    fieldnames = ["File Name", "Duration (seconds)", "bpm", "genre", "key"]
    
    # Create and write the CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row
        
        # Process each song in the playlist
        for song_path in playlist:
            metadata = get_song_metadata(song_path)
            if metadata:
                # Get the file name from the path
                file_name = os.path.basename(song_path)
                # Write the metadata row
                key = key_conv(metadata.get("key"))
                writer.writerow({
                    "File Name": file_name,
                    # "Title": metadata.get("Title"),
                    # "Artist": metadata.get("Artist"),
                    "Duration (seconds)": metadata.get("Duration"),
                    "bpm": metadata.get("bpm"),
                    "genre": metadata.get("genre"),
                    "key": key
                })

# Function to load the playlist from a folder
def load_playlist():
    file_paths = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav")])
    return list(file_paths)

# Function to save the playlist as a CSV
def save_as_csv():
    playlist = load_playlist()
    if playlist:
        output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if output_file:
            save_playlist_to_csv(playlist, output_file)
            print(f"Playlist saved to {output_file}")

# # Create the GUI
# root = tk.Tk()
# root.title("Save Playlist to CSV")

# # Button to load the playlist and save as CSV
# # save_csv_btn = tk.Button(root, text="Save Playlist to CSV", command=save_as_csv)
# # save_csv_btn.pack(pady=20)

# # Run the GUI
# root.mainloop()
