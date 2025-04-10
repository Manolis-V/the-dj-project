import tkinter as tk
from tkinter import ttk
from audio_processing import AudioPlayer
from mixer_controller import MixerController
import utils
import threading
import time

class DJApp:
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("DJ Mixer")

        self.player = AudioPlayer(update_song_callback=self.update_song_label)

        self.mixer = MixerController(update_label_callback=self.update_volume_label, audio_player = self.player)

        self.file_name = ""
        self.pool_name = ""
        self.bpm, self.key, self.dur = None, None, None

        # Track 1 Controls
        self.frame1 = ttk.LabelFrame(self.root, text="Track 1 Controls")
        self.frame1.grid(row=0, column=0, padx=10, pady=10, sticky="news")

        self.frame1_name = ttk.Label(self.frame1, text='')
        self.frame1_name.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.button1_ppss = ttk.Button(self.frame1, text="Sync Play", command=self.play_sync1)
        self.button1_ppss.grid(row=2, column=0, padx=5, pady=5)
        self.button1_pp = ttk.Button(self.frame1, text="Play", command=self.play_pause_song1)
        self.button1_pp.grid(row=2, column=1, padx=5, pady=5)
        self.button_cue2 = ttk.Button(self.frame1, text="Cue", command=self.cue_song1)
        self.button_cue2.grid(row=2, column=2, padx=5, pady=5)

        self.add_btn1 = ttk.Button(self.frame1, text="Add Track 1", command=self.load_song1)
        self.add_btn1.grid(row=0, column=2, padx=10, pady=10)

        self.bpm_label1 = ttk.Label(self.frame1, text="BPM: Unknown")
        self.bpm_label1.grid(row=3, column=0, padx=10, pady=10)
        self.key_label1 = ttk.Label(self.frame1, text="KEY: Unknown")
        self.key_label1.grid(row=4, column=0, padx=10, pady=10)
        self.volume_label1 = ttk.Label(self.frame1, text="Volume: 100%")
        self.volume_label1.grid(row=3, column=1, padx=10, pady=10)
        self.dur1 = ttk.Label(self.frame1, text="-/-")
        self.dur1.grid(row=3, column=2, padx=10, pady=10)

        self.progress_bar1 = ttk.Scale(self.frame1, from_=0, to=100, orient="horizontal", length=300, style="TScale")
        self.progress_bar1.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Track 2 Controls
        self.frame2 = ttk.LabelFrame(self.root, text="Track 2 Controls")
        self.frame2.grid(row=0, column=2, padx=10, pady=10, sticky="news")

        self.frame2_name = ttk.Label(self.frame2, text='')
        self.frame2_name.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.button2_ppss = ttk.Button(self.frame2, text="Sync Play", command= self.play_sync2)
        self.button2_ppss.grid(row=2, column=0, padx=5, pady=5)
        self.button2_pp = ttk.Button(self.frame2, text="Play", command=self.play_pause_song2)
        self.button2_pp.grid(row=2, column=1, padx=5, pady=5)
        self.button_cue2 = ttk.Button(self.frame2, text="Cue", command=self.cue_song2)
        self.button_cue2.grid(row=2, column=2, padx=5, pady=5)

        self.add_btn2 = ttk.Button(self.frame2, text="Add Track 2", command=self.load_song2)
        self.add_btn2.grid(row=0, column=2, padx=10, pady=10)

        self.bpm_label2 = ttk.Label(self.frame2, text="BPM: Unknown")
        self.bpm_label2.grid(row=3, column=0, padx=10, pady=10)
        self.key_label2 = ttk.Label(self.frame2, text="KEY: Unknown")
        self.key_label2.grid(row=4, column=0, padx=10, pady=10)
        self.volume_label2 = ttk.Label(self.frame2, text="Volume: 0%")
        self.volume_label2.grid(row=3, column=1, padx=10, pady=10)
        self.dur2 = ttk.Label(self.frame2, text="-/-")
        self.dur2.grid(row=3, column=2, padx=10, pady=10)

        self.progress_bar2 = ttk.Scale(self.frame2, from_=0, to=100, orient="horizontal", length=300, style="TScale")
        self.progress_bar2.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Mixer
        self.frame3 = ttk.LabelFrame(self.root, text="Mixer", labelanchor="n")
        self.frame3.grid(row=0, column=1, padx=10, pady=10, sticky="news")

        self.volume1 = ttk.Scale(self.frame3, from_=100, to=0, orient='vertical', command=self.update_volume1)
        self.volume1.set(100)  # Set initial volume to 100%
        self.volume1.grid(row=2, column=0, padx=5, pady=5)

        self.volume2 = ttk.Scale(self.frame3, from_=100, to=0, orient='vertical', command=self.update_volume2)
        self.volume2.set(100)  # Set initial volume to 100%
        self.volume2.grid(row=2, column=4, padx=5, pady=5)

        # crossfader
        self.volume3 = ttk.Scale(self.frame3, from_=100, to=0, orient='horizontal', command=self.update_crossfader)
        self.volume3.set(100)
        self.volume3.grid(row=3, column=2, padx=5, pady=5)


        ttk.Button(self.frame3, text="Stop All Tracks", command=self.play).grid(row=4, column=2, padx=10, pady=10)
        ttk.Button(self.frame3, text="init", command=self.play).grid(row=4, column=3, padx=5, pady=5)
        ttk.Button(self.frame3, text="Sync", command=self.sync1).grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(self.frame3, text="Trans", command=self.transition).grid(row=5, column=2, padx=5, pady=5)
        ttk.Button(self.frame3, text="Sync", command=self.sync2).grid(row=5, column=3, padx=5, pady=5)
        ttk.Button(self.frame3, text="Save Playlist to CSV", command=self.play).grid(row=6, column=2, padx=5, pady=5)
        self.auto_bb = ttk.Button(self.frame3, text="Auto: Off", command=self.auto_play_on_off)
        self.auto_bb.grid(row=6, column=1, padx=5, pady=5)

        self.load_button = ttk.Button(self.frame3, text="Load CSV", command=self.play)
        self.load_button.grid(row=6, column=3, pady=10)

        self.frame4 = ttk.LabelFrame(self.root, text="pools")
        self.frame4.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.player.tree_pool = ttk.Treeview(self.frame4, show="headings")
        self.player.tree_pool.grid(row=0, column=0)
        # Create the Treeview widget
        self.player.tree = ttk.Treeview(self.frame4, show="headings")
        self.player.tree.grid(row=0, column=1)


        utils.load_dir(self.player.tree_pool, self.player.tree)
        utils.load_csv(self.player.tree)
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.frame4, orient="vertical", command=self.player.tree.yview)
        self.player.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=2, sticky="nsew")

        # Bind the double-click event to the Treeview
        self.player.tree.bind('<Double-Button-1>', lambda event: utils.on_single_click(event, self.player.tree, self.handle_selected_file))

        self.player.tree_pool.bind("<Button-1>", lambda event: utils.on_double_click(event, self.player.tree_pool, self.player.tree, self.handle_selected_pool))



    def play(self):
        self.mixer.play_song1_audio()

    def auto_play_on_off(self):

        if self.player.auto_mode:
            self.player.auto_mode = False
            self.auto_bb.config(text="Auto: Off")
        else:
            self.player.auto_mode = True
            self.auto_bb.config(text="Auto: On")

    def play_pause_song1(self):
        if(self.mixer.play_pause_song1_audio()):
            self.button1_pp.config(text="Pause")
        else:
            self.button1_pp.config(text="Play")

    def play_pause_song2(self):
        if(self.mixer.play_pause_song2_audio()):
            self.button2_pp.config(text="Pause")
        else:
            self.button2_pp.config(text="Play")
    
    def play_sync1(self):
        start_op = time.time()
        wait = self.player.sync_play_deck1()

        def sleeping1(time_d):
            time.sleep(time_d - time.time())
            self.play_pause_song1()
            self.transition()

        threading.Thread(target=sleeping1, args=(float(wait + start_op),),  daemon=True).start()

    def play_sync2(self):
        start_op = time.time()
        wait = self.player.sync_play_deck2()

        def sleeping2(time_d):
            time.sleep(time_d - time.time())
            self.play_pause_song2()
            self.transition()

        threading.Thread(target=sleeping2, args=(float(wait + start_op),),  daemon=True).start()

    def cue_song1(self):
        self.mixer.cue1_audio()
        self.button1_pp.config(text="Play")

    def cue_song2(self):
        self.mixer.cue2_audio()
        self.button2_pp.config(text="Play")

    def run(self):
        self.root.mainloop()

    def update_volume1(self, value):
        self.mixer.set_volume_deck1(float(value))

    def update_volume2(self, value):
        self.mixer.set_volume_deck2(float(value))

    def update_crossfader(self, value):
        self.mixer.set_crossfader(float(value))

    def update_volume_label(self, text1, text2):
        """Update the label text from MixerController."""
        self.volume_label1.config(text=f"Volume: {text1:.2f}")
        self.volume_label2.config(text=f"Volume: {text2:.2f}")

    def update_song_label(self, deck, text1, text2, text3, text4):
        if deck == 1:
            self.frame1_name.config(text=text4)
            self.bpm_label1.config(text=text1)
            self.key_label1.config(text=text3)
            self.dur1.config(text=text2)
        elif deck == 2:
            self.frame2_name.config(text=text4)
            self.bpm_label2.config(text=text1)
            self.key_label2.config(text=text3)
            self.dur2.config(text=text2)

    def transition(self, trans_dur=None):
        """Smoothly moves the crossfader."""
        if int(self.volume3.get()) == 100:
            start, end = 100, 0
        else:
            start, end = 0, 100

        step = 1 if start < end else -1

        if not trans_dur: trans_dur = self.player.trans_step

        def move_fader():
            print(f"{utils.bcolors.OKBLUE}gui.py:{utils.bcolors.ENDC} Transitioning for: {trans_dur}")
            for value in range(start, end + step, step):
                self.volume3.set(value)
                time.sleep(trans_dur/100)
            print(f"{utils.bcolors.OKBLUE}gui.py:{utils.bcolors.ENDC} Done")
            if start == 100:
                self.play_pause_song1()
                if self.player.auto_mode:
                    self.player.pick_song(1)
            else:
                self.play_pause_song2()
                if self.player.auto_mode:
                    self.player.pick_song(2)
        threading.Thread(target=move_fader, daemon=True).start()

    def handle_selected_file(self, item_values):
        """Receives file name from on_double_click and does something with it."""
        self.file_name = item_values[1]
        self.bpm = item_values[2]
        self.key = item_values[3]
        self.dur = item_values[5]

    def handle_selected_pool(self, item_values):
        """Receives file name from on_double_click and does something with it."""
        self.pool_name = item_values[0]

    def load_song1(self):
        threading.Thread(target=self.player.load_song1_audio, args=(self.file_name, self.pool_name, self.bpm, self.dur, self.key), daemon=True).start()

    def load_song2(self):
        threading.Thread(target=self.player.load_song2_audio, args=(self.file_name, self.pool_name, self.bpm, self.dur, self.key), daemon=True).start()

    def sync1(self):
        self.player.beatmatch(1)

    def sync2(self):
        self.player.beatmatch(2)