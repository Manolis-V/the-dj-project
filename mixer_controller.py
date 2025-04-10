import pygame
import time

class MixerController:
    def __init__(self, update_label_callback=None, audio_player=None):
        self.volume_deck1 = 0.5  # Default volume (50%)
        self.volume_deck2 = 0.5
        self.crossfader_position = 0.5  # Middle position (0 to 1)
        self.channel1 = pygame.mixer.Channel(0)
        self.channel2 = pygame.mixer.Channel(1)
        self.update_label_callback = update_label_callback  # Store the callback function
        self.audio_player = audio_player  # Reference to AudioPlayer instance
        self.is_playing1 = False
        self.is_playing2 = False
        self.has_started1 = False
        self.has_started2 = False
        self.is_transitioning = False

    def set_volume_deck1(self, val):
        self.volume_deck1 = float(val) / 100
        self.channel1.set_volume(self.volume_deck1)

    def set_volume_deck2(self, val):
        self.volume_deck2 = float(val) / 100
        self.channel2.set_volume(self.volume_deck2)

    def get_crossfader_position(self):
        return self.crossfader_position
    
    def set_crossfader(self, val):
        self.crossfader_position = float(val) / 100
        if self.channel1 and self.channel2:  # Ensure both channels are loaded
            volume1 = (self.crossfader_position**0.7)*self.volume_deck1
            volume2 = ((1.0 - self.crossfader_position)**0.7)*self.volume_deck2
            
            self.channel1.set_volume(volume1)
            self.channel2.set_volume(volume2)
            
            # Call the GUI label update function if it exists
            if self.update_label_callback:
                self.update_label_callback(
                    volume1,
                    volume2
                    )
        
    def play_pause_song1_audio(self):
        if self.audio_player.deck1 and self.is_playing1:
            self.channel1.pause()
            self.is_playing1 = False
            return False

        elif self.audio_player.deck1 and self.is_playing1 == False and self.audio_player.changed_track1:
            self.channel1.play(self.audio_player.deck1)
            self.audio_player.deck1_start_time = time.time()  # Record start time
            self.has_started1 = True
            self.is_playing1 = True
            self.audio_player.changed_track1 = False
            return True
        
        elif self.is_playing1 == False:
            print("upause")
            self.channel1.unpause()
            self.is_playing1 = True
            return True

    def play_pause_song2_audio(self):
        if self.audio_player.deck2 and self.is_playing2:
            self.channel2.pause()
            self.is_playing2 = False
            return False

        elif self.audio_player.deck2 and self.is_playing2 == False and self.audio_player.changed_track2:
            self.channel2.play(self.audio_player.deck2)
            self.audio_player.deck2_start_time = time.time()  # Record start time
            self.has_started2 = True
            self.is_playing2 = True
            self.audio_player.changed_track2 = False
            return True
        
        elif self.is_playing2 == False:
            self.channel2.unpause()
            self.is_playing2 = True
            return True

    def cue1_audio(self):
        if self.audio_player.deck1:
            self.channel1.stop()
            self.audio_player.deck1.play(0, 0)
            self.channel1.pause()
            self.is_playing1 = False

    def cue2_audio(self):
        if self.audio_player.deck2:
            self.channel2.stop()
            self.audio_player.deck2.play(0, 0)
            self.channel2.pause()
            self.is_playing2 = False