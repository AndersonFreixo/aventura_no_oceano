import pygame
import random
from pygame.locals import *
from sys import exit
from time import sleep

from aventura_no_oceano.engine import minigui, music_player, sound_player
from aventura_no_oceano.game import entity, state
from aventura_no_oceano.data import levels
from aventura_no_oceano.common.constants import *


class App:
    def __init__(self):
        self.backgrounds = []
        self.sounds = dict()
        self.current_round = 0
        self.context = "game"
        self.game_font = None   # initialized in init_pygame method
        self.screen = None      #
        self.clock = None       #
        self.music = music_player.MusicPlayer()
        self.sound = sound_player.SoundPlayer()

        self.init_pygame()
        self.gui = minigui.MiniGui()

        self.init_music()
        self.init_sounds()
        self.init_backgrounds()
        self.init_buttons()
        self.player = entity.Player((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.state = state.State()

    def init_music(self):
        """Initialize the music player"""
        soundtrack = ["aventura_no_oceano/resources/sound/st_01.ogg",
                    "aventura_no_oceano/resources/sound/st_02.ogg",
                    "aventura_no_oceano/resources/sound/st_03.ogg",
                    "aventura_no_oceano/resources/sound/st_04.ogg"]

        for s in soundtrack:
            self.music.add_track(s)


    def init_sounds(self):
        self.sound.add("select", "aventura_no_oceano/resources/sound/select.ogg")
        self.sound.add("click", "aventura_no_oceano/resources/sound/click-cut.ogg")
        self.sound.add("eat",  "aventura_no_oceano/resources/sound/chomp-cut.ogg")
        self.sound.add("hurt", "aventura_no_oceano/resources/sound/hurt.ogg")
        self.sound.add("gameover", "aventura_no_oceano/resources/sound/game_over2.ogg")


    def init_pygame(self):
        """This method initializes Pygame, the game font, screen and clock and configures some other stuff."""
        pygame.init()

        pygame.display.set_caption("Aventura no oceano")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT+INFO_BOARD_HEIGHT),0,16)
        self.clock = pygame.time.Clock()

    def init_backgrounds(self):
        """This method loads the background picture files into a list."""
        for num in range(0, NUM_OF_ROUNDS):
            self.backgrounds.append(pygame.image.load("aventura_no_oceano/resources/img/bg"+str(num+1)+".png").convert())

    def init_buttons(self):
        """Initialize the buttons used in all screens of the game"""
        self.gui.create_button("init", "INICIAR", (100,30))
        self.gui.create_button("exit", "SAIR", (100,30))
        self.gui.create_button("back", "VOLTAR", (100,30))

    def run(self):
        """This function consists of a loop that calls the three game loops one afther another:
            the initial screen loop, game loop and game over screen loop.
            If player doesn't quit the game after Game Over screen, state.reset() is called
            to reset game state."""

        while True:
            self.state.reset()
            self.initial_screen()
            self.game_loop()
            self.game_over()


    def render_board(self):
        """This function renders information about lives, level and score on screen."""

        self.screen.fill((0,0,0), (0, SCREEN_HEIGHT, SCREEN_WIDTH, INFO_BOARD_HEIGHT))
        level_txt = "Nivel: "+str(self.state.level)
        lives_txt = "Vidas: "+str(self.state.lives)
        score_txt = "Pontos: "+str(self.state.score)

        self.screen.blit(self.gui.get_text(level_txt),(0, SCREEN_HEIGHT))
        self.screen.blit(self.gui.get_text(lives_txt),(100, SCREEN_HEIGHT))
        self.screen.blit(self.gui.get_text(score_txt),(200, SCREEN_HEIGHT))
        if self.state.imune != 0:
            pygame.draw.line(self.screen, (255,0,0), (5, SCREEN_HEIGHT+STD_FONT_SIZE), (self.state.imune*3,SCREEN_HEIGHT+STD_FONT_SIZE), 3)


    def initial_screen(self):
        """The game's starting screen"""
        start_screen = pygame.image.load(START_SCREEN_IMG).convert_alpha()

        start_button_position = 5, 400
        exit_button_position = 5, 440

        self.gui.put_button("init", start_button_position)
        self.gui.put_button("exit", exit_button_position)

        while True:

            self.screen.fill((0,0,255))
            self.screen.blit(start_screen, (0,0))
            self.screen.blit(self.gui.get_text("Criado por Anderson S. Freixo"), (0, SCREEN_HEIGHT))
            self.screen.blit(self.gui.get_text("anderson.freixo@gmail.com"), (0, SCREEN_HEIGHT+20))
            self.gui.render(self.screen)

            if self.gui.check_cursor():

                self.sound.play("select")

            for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()
                    if event.type == MOUSEBUTTONDOWN:
                        self.sound.play("click")

                        sleep(1)
                        if self.gui.what_is_clicked() == "init":

                            self.gui.remove_button("init")
                            self.gui.remove_button("exit")
                            return
                        elif self.gui.what_is_clicked() == "exit":
                            exit()
            pygame.display.update()

    def game_loop(self):
        """This is the game engine's main loop"""
        pygame.mouse.set_visible(False)
        self.music.play(0)

        self.state.populate()

        while True:
            self.clock.tick(STD_FRAME_RATE)
            if self.state.lives <= 0:
                self.sound.play("gameover")
                self.music.stop()
                return

            self.state.update()

              #Change to next song if round changes.
            if self.state.round != self.current_round:
                self.current_round = self.state.round
                self.music.next()

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

            self.screen.blit(self.backgrounds[self.state.round],(0,0))
            pos = pygame.mouse.get_pos()
            self.player.move(pos)

            for ent in self.state.entities:
                #if enemy touches player
                if ent.is_touching(self.player.get_position(), self.player.get_size()) and self.state.imune == 0:
                    #TODO Put collision related functions in state
                    if self.state.lives > 1:
                        self.sound.play("hurt")
                    self.state.lives-=1
                    self.state.imune = STD_FRAME_RATE

                ent.render(self.screen)

            for fd in self.state.food:
                #if player surface covers food surface
                    #TODO Put collision related functions in state
                if fd.is_covered(self.player.get_position(), self.player.get_size()):
                    self.sound.play("eat")
                    self.state.score+=10
                    self.state.food.remove(fd)
                fd.render(self.screen)

            self.player.render(self.screen)
            self.render_board()

            pygame.display.update()

    def game_over(self):
        """The Game Over screen"""

        pygame.mouse.set_visible(True)
        back_button_position = 5, 400
        exit_button_position = 5, 440

        score_txt = "Score: "+str(self.state.score)
        score_surface = self.gui.get_text(score_txt)
        go_screen = pygame.image.load(GAMEOVER_SCREEN_IMG).convert_alpha()

        self.gui.put_button("back", back_button_position)
        self.gui.put_button("exit", exit_button_position)

        while True:

            self.screen.fill((0,0,255))
            self.screen.blit(go_screen, (0,0))
            self.screen.blit(score_surface,(0,0))
            self.gui.render(self.screen)


            if self.gui.check_cursor(): #mouse has just been placed over a button

                self.sound.play("select")

            for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()
                    if event.type == MOUSEBUTTONDOWN:
                        self.sound.play("click")

                        sleep(1)
                        if self.gui.what_is_clicked() == "back":

                            self.gui.remove_button("back")
                            self.gui.remove_button("exit")
                            return
                        elif self.gui.what_is_clicked() == "exit":
                            exit()
            pygame.display.update()
