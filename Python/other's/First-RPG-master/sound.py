#!/usr/bin/env python
import os, pygame

class sound():
    def __init__(self):
        freq = 44100
        bitsize = -16
        channels = 2
        buffer = 2048
        pygame.mixer.init(freq, bitsize, channels, buffer)

    def play_music(self, music_file):
        try:
            pygame.mixer.music.load(os.path.join('music',str(music_file)))
        except pygame.error:
            print("File %s not found! (%s)" % (music_file, pygame.get_error()))
            return
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.6)

    def stop_music(self):
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()