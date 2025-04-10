# DJ Software Project

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Future Enhancements](#future-enhancements)
- [License](#license)


---

## Project Overview
This project is a DJ mixing software that allows users to load, play, and manipulate audio tracks. The software includes audio playback, crossfading, and playlist management. It is built using **Python** with libraries such as **Pygame, Pydub, Tkinter** for audio processing and user interface. It also allows for auto mixing, matching and transitioning on beat with a push of a button.

---

## Features
- **Audio Loading & Playback**: Load and play multiple tracks.
- **Crossfader**: Smoothly transition between two tracks.
- **Auto mixing**: Starting next song on beat, and mixes it.
- **Auto song picking**: After the transition, picks next optimal song.
- **Playlist Management**: Load directories and manage playlists using CSV files.
- **Directory Browsing**: View and select songs from directories.

---

## Installation
### Prerequisites
Ensure you have Python installed (3.8 or later) and pyrubberband.

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
python main.py
```
Use the GUI to load songs, play/pause, crossfade.
After adding the first 2 songs, by pressing ```Sync Play``` on the second song, it will start the second song on beat and transition smoothly.
If ```Auto``` is ```On``` after the transition it will pick the next best song, depending on bpm, duration and key.

---

## Dependencies
- **Pygame** - Audio playback and timing
- **Pydub** - Audio processing
- **SciPy** - Digital signal processing (filters, BPM analysis)
- **Mutagen** - Metadata extraction (BPM, key, title)
- **Tkinter** - Graphical user interface
- **pyrubberband** - Audio analysis and manipulation

---

## Future Enhancements
- **Audio Effects**: Echo, reverb, phaser.
- **MIDI Controller Support**: Use external DJ controllers.
- **Cloud Integration**: Load songs from streaming services.

---

## License
MIT License