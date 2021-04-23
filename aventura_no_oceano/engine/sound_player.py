import pygame

class SoundPlayer:
    def __init__(self):
        self.sounds = dict()

    def add(self, name, path):
        self.sounds[name] = pygame.mixer.Sound(path)

    def play(self, name):
        self.sounds[name].play()
