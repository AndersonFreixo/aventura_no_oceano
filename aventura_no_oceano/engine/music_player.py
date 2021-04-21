import pygame

class MusicPlayer:
    def __init__(self):
        self.playlist = []
        self.current = 0
    def add_track(self, filename):
        self.playlist.append(filename)

    def play(self, index = 0):
        self.current = index
        pygame.mixer.music.load(self.playlist[index])
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        """Play next song on soundtrack"""
        #increments current or sets to 0 if == to number of
        #songs in playlist
        self.current = (self.current + 1) % len(self.playlist)
        self.play(self.current)
