# DJ Software Project

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Audio Processing](#audio-processing)
- [Beat Matching and Synchronization](#beat-matching-and-synchronization)
- [User Interface](#user-interface)
- [File Management](#file-management)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

---

## Project Overview
This project is a DJ mixing software that allows users to load, play, and manipulate audio tracks. The software includes audio playback, crossfading, and playlist management. It is built using **Python** with libraries such as **Pygame, Pydub, Tkinter** for audio processing and user interface.

---

## Features
- **Audio Loading & Playback**: Load and play multiple tracks.
- **Crossfader**: Smoothly transition between two tracks.
- **Playlist Management**: Load directories and manage playlists using CSV files.
- **Directory Browsing**: View and select songs from directories.

---

## Installation
### Prerequisites
Ensure you have Python installed (3.8 or later).

### Install Dependencies
```bash
pip install pygame pydub scipy numpy mutagen tkinter
```

If using **FFmpeg** for audio processing, install it separately:
```bash
sudo apt install ffmpeg  # Linux
brew install ffmpeg      # MacOS
```
For Windows, download and install FFmpeg from [ffmpeg.org](https://ffmpeg.org/).

---

## Usage
Run the main script:
```bash
python dj2.py
```
Use the GUI to load songs, play/pause, crossfade.

---

## Dependencies
- **Pygame** - Audio playback and timing
- **Pydub** - Audio processing
- **SciPy** - Digital signal processing (filters, BPM analysis)
- **Mutagen** - Metadata extraction (BPM, key, title)
- **Tkinter** - Graphical user interface

---

## Audio Processing
### 1. Loading Audio Files
```python
from pydub import AudioSegment
track = AudioSegment.from_file("song.mp3", format="mp3")
```

### 2. Playing Audio
```python
import pygame.mixer
pygame.mixer.init()
pygame.mixer.music.load("song.mp3")
pygame.mixer.music.play()
```

### 3. Crossfading
```python
crossfade_time = 5000  # 5 seconds
mixed = track1.append(track2, crossfade=crossfade_time)
mixed.export("output.mp3", format="mp3")
```


---

## Beat Matching and Synchronization
### 1. Detecting BPM
```python
from mutagen.mp3 import MP3

audio = MP3("song.mp3")
bpm = audio.info.bitrate  # Example: Extract BPM from metadata
```

### 2. Synchronizing Two Tracks
```python
if track1_bpm > track2_bpm:
    track2 = track2.speedup(playback_speed=track1_bpm/track2_bpm)
```

---

## User Interface
### 1. Tkinter UI with Progress Bar
```python
from tkinter import ttk
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode='determinate')
progress.pack()
```

### 2. Directory Browsing in Treeview
```python
import os
from tkinter import ttk

tree = ttk.Treeview(root)
tree.insert("", "end", text=os.path.basename("C:/Users/Desktop"))
tree.pack()
```

---

## File Management
### Storing Playlists in CSV
```python
import csv

playlist = ["song1.mp3", "song2.mp3"]
with open("playlist.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows([[song] for song in playlist])
```

---

## Performance Optimization
- **Reduce Memory Usage**: Load only sections of a song instead of full tracks.
- **Use Threads**: Run playback and UI updates in separate threads.
- **Limit FFT Computation**: If visualizing waveforms, downsample the signal before processing.

---

## Troubleshooting
### 1. Pygame Mixer Errors
If `pygame.mixer` fails to play MP3 files, install FFmpeg and use Pydub instead.

### 2. Memory Issues
If RAM usage is high, use streaming instead of loading full files.

### 3. Permission Errors
Ensure the script has write access to temporary directories.

---

## Future Enhancements
- **Auto-DJ Mode**: AI-powered track selection.
- **More Audio Effects**: Echo, reverb, phaser.
- **MIDI Controller Support**: Use external DJ controllers.
- **Cloud Integration**: Load songs from streaming services.

---

## Contributors
- [Your Name]

## License
MIT License

