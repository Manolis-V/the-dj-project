from tkinter import filedialog
import tkinter as tk
import csv
import tempfile
import soundfile as sf
import librosa
import numpy as np
from pathlib import Path

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

CIRCLE_OF_FIFTHS = {
    "C major":    ["G major", "F major", "A minor", "C minor"],
    "G major":    ["D major", "C major", "E minor", "G minor"],
    "D major":    ["A major", "G major", "B minor", "D minor"],
    "A major":    ["E major", "D major", "F# minor", "A minor"],
    "E major":    ["B major", "A major", "C# minor", "E minor"],
    "B major":    ["F# major", "E major", "D# minor", "B minor"],
    "F# major":   ["C# major", "B major", "G# minor", "F# minor"],
    "C# major":   ["G# major", "F# major", "A# minor", "C# minor"],
    "F major":    ["C major", "B- major", "D minor", "F minor"],
    "B- major":   ["F major", "Eb major", "G minor", "B- minor"],
    "E- major":   ["B- major", "A- major", "C minor", "E- minor"],
    "A- major":   ["E- major", "D- major", "F minor", "A- minor"],
    "D- major":   ["A- major", "G- major", "B- minor", "D- minor"],
    "G- major":   ["D- major", "C- major", "E- minor", "G- minor"],
    "C- major":   ["G- major", "E major", "A- minor", "C- minor"],

    # **Minor Keys**
    "A minor":    ["C major", "E minor", "D minor", "A major"],
    "E minor":    ["G major", "B minor", "A minor", "E major"],
    "B minor":    ["D major", "F# minor", "E minor", "B major"],
    "F# minor":   ["A major", "C# minor", "B minor", "F# major"],
    "C# minor":   ["E major", "G# minor", "F# minor", "C# major"],
    "G# minor":   ["B major", "D# minor", "C# minor", "G# major"],
    "D# minor":   ["F# major", "A# minor", "G# minor", "D# major"],
    "A# minor":   ["C# major", "F minor", "D# minor", "A# major"],
    "D minor":    ["F major", "B- major", "C minor", "D major"],
    "G minor":    ["B- major", "E- major", "A minor", "G major"],
    "C minor":    ["E- major", "A- major", "D minor", "C major"],
    "F minor":    ["A- major", "D- major", "G minor", "F major"],
    "B- minor":   ["D- major", "G- major", "C# minor", "B- major"],
    "E- minor":   ["G- major", "C- major", "F# minor", "E- major"],
    "A- minor":   ["C- major", "E major", "G# minor", "A- major"]
}
relative_minor_major = {
        "C major": "A minor", "A minor": "C major",
        "G major": "E minor", "E minor": "G major",
        "D major": "B minor", "B minor": "D major",
        "A major": "F# minor", "F# minor": "A major",
        "E major": "C# minor", "C# minor": "E major",
        "B major": "G# minor", "G# minor": "B major",
        "F# major": "D# minor", "D# minor": "F# major",
        "C# major": "A# minor", "A# minor": "C# major",
        "F major": "D minor", "D minor": "F major",
        "B- major": "G minor", "G minor": "B- major",
        "E- major": "C minor", "C minor": "E- major",
        "A- major": "F minor", "F minor": "A- major",
        "D- major": "B- minor", "B- minor": "D- major",
        "G- major": "E- minor", "E- minor": "G- major",
        "C- major": "A- minor", "A- minor": "C- major",
}


def load_dir(tree_pool, tree, mode=1, dir="pool1"):

    file_path = ''
    if mode == 0:
        load_csv(tree, 1, dir)
    elif mode == 1:
        file_path = "../music/csvs/music.csv"
    if not file_path:
        return
    # Clear existing data in the Treeview
    for row in tree_pool.get_children():
        tree_pool.delete(row)

    # Open the CSV file and read it
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Get the headers from the first row

        # Clear existing columns in the Treeview
        tree_pool["columns"] = headers

        # Define columns and headings
        for header in headers:
            if header == 'path':
                tree_pool.heading(header, text=header)
                tree_pool.column(header, width=100, stretch=False)
        # Add rows to the Treeview
        for row in reader:
            tree_pool.insert("", tk.END, values=row)

def load_csv(tree, mode=1, pool="pool1"):
    # Ask the user to select a CSV file
    if mode == 0:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    elif mode == 1:
        file_path = "../music/csvs/" + pool + ".csv"
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
                tree.column(header, width=300, stretch=False)
            elif header == 'id':
                tree.heading(header, text=header)
                tree.column(header, width=30, stretch=False)
            else:
                tree.heading(header, text=header)
                tree.column(header, width=100, stretch=False)

        # Add rows to the Treeview
        for row in reader:
            tree.insert("", tk.END, values=row)

# songs
def on_single_click(event, tree, callback):
    # Get the item selected by the user
    selected_item = tree.selection()
    if selected_item:
        item_values = tree.item(selected_item, 'values')
        callback(item_values)  # Call the GUI function with the selected file name
# pools
def on_double_click(event, tree_pool, tree, callback):
    selected_item = tree_pool.selection()
    if selected_item:
        item_values = tree_pool.item(selected_item, 'values')
        file_name = item_values[0]
        pool = file_name
        load_dir(tree_pool, tree, 0, pool)
        callback(item_values)  # Call the GUI function with the selected file name

def convert_to_wav(mp3_path, threshold=0.02):
    """Convert MP3 to WAV for faster loading."""
    y, sr = librosa.load(mp3_path, sr=None)
    # Compute absolute energy
    energy = np.abs(y)
    
    # Find the first non-silent frame
    start_index = np.argmax(energy > np.max(energy) * threshold)
    # Trim the silence
    y_trimmed = y[start_index:]

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_file_path = temp_file.name
    temp_file.close()  # Close so pydub can write to it

    # Save the trimmed file
    sf.write(temp_file_path, y_trimmed, sr)
    print(f"{bcolors.OKCYAN}utils.py:{bcolors.ENDC} Converted {Path(mp3_path).stem}")
    return temp_file_path  # Return the WAV file path