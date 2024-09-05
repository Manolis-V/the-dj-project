import pygame
import time

def main():
    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load an audio file
    track = pygame.mixer.Sound("001.Katy Perry - I Kissed A Girl (Official Music Video).mp3")

    # Play the track
    channel = track.play()
    print("Playing track1.mp3")

    while True:
        command = input("Enter command (pause/resume/stop): ").strip().lower()
        
        if command == "pause":
            channel.pause()
            print("Paused.")
        elif command == "resume":
            channel.unpause()
            print("Resumed.")
        elif command == "stop":
            channel.stop()
            print("Stopped.")
            break
        else:
            print("Unknown command. Please enter pause, resume, or stop.")

if __name__ == "__main__":
    main()
