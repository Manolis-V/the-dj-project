import pygame
from utils import convert_to_wav, bcolors, CIRCLE_OF_FIFTHS, relative_minor_major
import librosa
import time
import numpy as np
import tempfile
import os
import soundfile as sf
import pyrubberband as pyrb
import librosa.display
from scipy.signal import find_peaks

class AudioPlayer:
    def __init__(self, update_song_callback=None):
        pygame.mixer.pre_init(44100, -16, 2, 512)  # Lower buffer size
        pygame.init()
        # pygame.mixer.init()
        self.deck1, self.deck2 = None, None
        self.changed_track1, self.changed_track2 = False, False
        self.beats1, self.beats2, self.bpm1, self.bpm2, self.dur1, self.dur2, self.key1, self.key2 = [], [], None, None, None, None, None, None
        self.deck1_start_time, self.deck2_start_time = None, None  # Track when Deck 1 starts
        self.file_path1, self.file_path2 = None, None
        self.played_song_ids, self.song_id1, self.song_id2 = [], None, None
        self.trans_step = None
        self.tree, self.tree_pool= None, None
        self.auto_mode = None
        self.update_song_callback = update_song_callback  # Store the callback function

    def load_song1_audio(self, file_name=None, pool_name=None, bpm=None, dur=None, key=None):
        """Loads a song into Deck 1 and prepares it for playback."""
        if file_name == None and pool_name == None:
            pool_name = "pool4"
            for child in self.tree.get_children():
                if self.tree.item(child)["values"][0] == self.song_id1:
                    file_name = self.tree.item(child)["values"][1]
        file_path = "music/" + pool_name + "/" + file_name + ".mp3"
        if self.file_path1:
            os.remove(self.file_path1)
        self.file_path1 = convert_to_wav(file_path)  # Convert before loading

        self.deck1 = pygame.mixer.Sound(self.file_path1)
        self.changed_track1 = True

        for child in self.tree.get_children():
            if self.tree.item(child)["values"][1] == file_name:
                self.played_song_ids.append(self.tree.item(child)["values"][0])
                self.song_id1 = self.tree.item(child)["values"][0]
                
        if bpm:
            bpm = int(float(bpm))-1
            dur = int(float(dur))
            beat_interval = 60.0 / bpm  # Seconds per beat
            beat_times = np.array([0.0 + (i * beat_interval) for i in range(int(dur/beat_interval))])
            beat_times = beat_times.flatten()

            self.beats1 = beat_times
            self.bpm1 = bpm
            self.dur1 = dur
            self.key1 = key

            # Call the GUI label update function if it exists
            if self.update_song_callback:
                self.update_song_callback(
                    1,
                    bpm,
                    dur,
                    key,
                    file_name
                    )
                
            print(f"{bcolors.OKGREEN}Deck 1:{bcolors.ENDC} Ready.")
            return
        self.beats1, self.bpm1 = self.get_beat_positions(self.file_path1)
        return
    
    def load_song2_audio(self, file_name=None, pool_name=None, bpm=None, dur=None, key=None):
        """Loads a song into Deck 2 and prepares it for playback."""
        if file_name == None and pool_name == None:
            pool_name = "pool4"
            for child in self.tree.get_children():
                if self.tree.item(child)["values"][0] == self.song_id2:
                    file_name = self.tree.item(child)["values"][1]
        file_path = "music/" + pool_name + "/" + file_name + ".mp3"
        if self.file_path2:
            os.remove(self.file_path2)
        self.file_path2 = convert_to_wav(file_path)  # Convert before loading
         
        self.deck2 = pygame.mixer.Sound(self.file_path2)
        self.changed_track2 = True

        for child in self.tree.get_children():
            if self.tree.item(child)["values"][1] == file_name:
                self.played_song_ids.append(self.tree.item(child)["values"][0])
                self.song_id2 = self.tree.item(child)["values"][0]

        if bpm:
            bpm = int(float(bpm))-1
            dur = int(float(dur))
            beat_interval = 60.0 / bpm
            beat_times = np.array([0.0 + (i * beat_interval) for i in range(int(dur/beat_interval))])
            beat_times = beat_times.flatten()
            self.beats2 = beat_times
            self.bpm2 = bpm
            self.dur2 = dur
            self.key2 = key

            if self.update_song_callback:
                self.update_song_callback(
                    2,
                    bpm,
                    dur,
                    key,
                    file_name
                    )
                    
            print(f"{bcolors.OKGREEN}Deck 2:{bcolors.ENDC} Ready.")
            return
        self.beats2, self.bpm2 = self.get_beat_positions(self.file_path2)
        return

    def pick_best_next_song(self, bpm_of_the_curr, duration_of_the_curr, key_of_the_curr):


        def bpm_score(bpm1, bpm2):
            """ Higher score if BPMs are close """
            return 1 - abs(bpm1 - bpm2) / max(bpm1, bpm2)

        def key_score(key1, key2):
            """ Uses Circle of Fifths for harmonic mixing """
            if key1 == key2 :
                return 1.0
            if key2 in CIRCLE_OF_FIFTHS.get(key1, []):
                return 0.8  # Closely related keys (dominant/subdominant)
            if key2 == relative_minor_major.get(key1, ""):
                return 0.75  # Relative minor/major match
            if key1.split()[0] == key2.split()[0]:  # Parallel keys (C Major & C Minor)
                return 0.6
            return 0.3  # Distant keys - bad match

        def duration_score(d1, d2):
            """ Prefers songs with similar durations """
            return 1 - abs(d1 - d2) / max(d1, d2)

        best_song_id = None
        highest_score = -1

        for child in self.tree.get_children():
            item_data = self.tree.item(child)["values"]
            bpm = int(float(item_data[2])) - 1
            duration = int(float(item_data[5]))
            key = item_data[3]
            song_id = item_data[0]
            
            if song_id not in self.played_song_ids:
                bpm_match = bpm_score(bpm_of_the_curr, bpm) * 0.55
                key_match = key_score(key_of_the_curr, key) * 0.3
                duration_match = duration_score(duration_of_the_curr, duration) * 0.15

                total_score = bpm_match + key_match + duration_match
                
                if total_score > highest_score:
                    highest_score = total_score
                    best_song_id = song_id
            
        return best_song_id

    def pick_song(self, deck=None):
        print(f"Pick_song.")
        if deck == 1:

            self.song_id1 = self.pick_best_next_song(self.bpm2, self.dur2, self.key2)
            for child in self.tree.get_children():
                if self.song_id1 == self.tree.item(child)["values"][0]:
                    item_data = self.tree.item(child)["values"]
            self.load_song1_audio(bpm=item_data[2], dur=item_data[5], key=item_data[3])

        elif deck == 2:

            self.song_id2 = self.pick_best_next_song(self.bpm1, self.dur1, self.key1)
            for child in self.tree.get_children():
                if self.song_id2 == self.tree.item(child)["values"][0]:
                    item_data = self.tree.item(child)["values"]
            self.load_song2_audio(bpm=item_data[2], dur=item_data[5], key=item_data[3])

    def get_beat_positions(self, file_path):
        # Load the audio file
        y, sr = librosa.load(file_path, sr=None)

        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

        # Convert beat frames to times
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        # 3️⃣ Calculate beat intervals using BPM
        beat_interval = 60.0 / (int(tempo)-1)  # Seconds per beat

        beat_times = np.array([0.0 + (i * beat_interval) for i in range(len(beat_times))])
        beat_times = beat_times.flatten()
        print(f"Bpm and bpm possition: Done!")
        return beat_times, int(tempo)

    def find_next_beat1(self):
        """Finds the next beat timestamp after the current playtime."""
        elapsed_time = time.time() - self.deck2_start_time  # Get current playback time
        return next((b for b in self.beats2[::32] if b > elapsed_time), None)#min([b for b in self.beats2[::32] if b > elapsed_time], default=None)

    def sync_play_deck1(self):
        """Starts Deck 1 exactly on the next beat of Deck 2."""

        next_beat2 = self.find_next_beat1()  # Get next beat timestamp
        if next_beat2 is None:
            print(f"{bcolors.FAIL}Error:{bcolors.ENDC} No beat detected!")
            return

        wait_time = next_beat2 - (time.time() - self.deck2_start_time)

        print(f"{bcolors.OKGREEN}Syncing Deck 1 in:{bcolors.ENDC} {wait_time:.6f} seconds...")
        self.trans_step = (self.beats2[31] - self.beats2[0])
        return wait_time

    def find_next_beat2(self):
        """Finds the next beat timestamp after the current playtime."""
        elapsed_time = time.time() - self.deck1_start_time  # Get current playback time
        return min([b for b in self.beats1[::32] if b > elapsed_time], default=None)#next((b for b in self.beats1[::32] if b > elapsed_time), None)

    def sync_play_deck2(self):
        """Starts Deck 2 exactly on the next beat of Deck 1."""

        next_beat1 = self.find_next_beat2()  # Get next beat timestamp
        if next_beat1 is None:
            print(f"{bcolors.FAIL}Error:{bcolors.ENDC} No beat detected!")
            return
        wait_time = next_beat1 - (time.time() - self.deck1_start_time)
        print(f"{bcolors.OKGREEN}Syncing Deck 2 in:{bcolors.ENDC} {wait_time:.6f} seconds...")
        self.trans_step = (self.beats1[31] - self.beats1[0])
        return wait_time

    def beatmatch(self, track_num) -> None:
        """Find's bpm ratio depending on track_num."""
        if self.deck1 and self.deck2:
            bpm1 = self.bpm1
            bpm2 = self.bpm2
            if bpm1 and bpm2 and bpm1 != bpm2:
                if track_num == 1:
                    speed_factor = bpm2 / bpm1  # Calculate speed ratio
                    self.change_bpm1(speed_factor)  # Adjust speed
                else:
                    speed_factor = bpm1 / bpm2  # Calculate speed ratio
                    self.change_bpm2(speed_factor)  # Adjust speed

    def change_bpm1(self, bpm_ratio) -> None:
        """
        Adjusts the BPM of an audio file while preserving pitch.
        """
        try:
            print("changing bpm1")
            y, sr = librosa.load(self.file_path1, sr=None)

            # Apply time-stretching while preserving pitch
            y_stretched = pyrb.time_stretch(y, sr, bpm_ratio)

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                temp_path = temp_wav.name  # Get the temporary file path

            sf.write(temp_path, y_stretched, sr)
            if self.file_path1:
                os.remove(self.file_path1)
            self.file_path1 = temp_path
            self.deck1 = pygame.mixer.Sound(temp_path)
            self.changed_track1 = True

            beat_interval = 60.0 / self.bpm2
            print(f"beat interval2: {beat_interval} len: {int(self.dur1/beat_interval)}")
            beat_times = np.array([0.0 + (i * beat_interval) for i in range(int(self.dur1/beat_interval))])
            beat_times = beat_times.flatten()

            self.bpm1 = self.bpm2
            self.beats1 = beat_times
            print(f"BPM1 changed. Saved as {temp_path}")
        except Exception as e:
            print(f"{bcolors.FAIL}Error changing BPM1 for:{bcolors.ENDC} '{self.file_path1}': {e}")

    def change_bpm2(self, bpm_ratio) -> None:
        """
        Adjusts the BPM of an audio file while preserving pitch.
        """
        try:
            print("changing bpm2")
            y, sr = librosa.load(self.file_path2, sr=None)

            # Apply time-stretching while preserving pitch
            y_stretched = pyrb.time_stretch(y, sr, bpm_ratio)

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                temp_path = temp_wav.name  # Get the temporary file path

            sf.write(temp_path, y_stretched, sr)
            if self.file_path2:
                os.remove(self.file_path2)
            self.file_path2 = temp_path
            self.deck2 = pygame.mixer.Sound(temp_path)
            self.changed_track2 = True
            
            beat_interval = 60.0 / self.bpm1
            print(f"beat interval2: {beat_interval} len: {int(self.dur2/beat_interval)}")
            beat_times = np.array([0.0 + (i * beat_interval) for i in range(int(self.dur2/beat_interval))])
            beat_times = beat_times.flatten()

            self.bpm2 = self.bpm1
            self.beats2 = beat_times
            print(f"BPM2 changed. Saved as {temp_path}")
        except Exception as e:
            print(f"{bcolors.FAIL}Error changing BPM2 for:{bcolors.ENDC} '{self.file_path2}': {e}")