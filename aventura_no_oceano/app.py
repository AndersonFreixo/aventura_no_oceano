import pygame
import random
from pygame.locals import *
from sys import exit
from time import sleep

from engine import minigui, music_player, sound_player
from game import entity, state
from data import levels
from common.constants import *


class App:
    def __init__(self):
        self.backgrounds = []
        self.sounds = dict()
        self.current_round = 0
        self.context = "game"
        self.game_font = None   # initialized in init_pygame method
        self.screen = None      #
        self.clock = None       #

        self.rank = list()
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

    def load_ranking(self):
        self.rank = list()
        with open(RANK_TXT, "r") as file:
            for line in file:
                player, score = line.split(":")
                score = int(score)
                self.rank.append((player, score))

    def init_music(self):
        """Initialize the music player"""
        soundtrack = ["resources/sound/st_01.ogg",
                    "resources/sound/st_02.ogg",
                    "resources/sound/st_03.ogg",
                    "resources/sound/st_04.ogg"]

        for s in soundtrack:
            self.music.add_track(s)


    def init_sounds(self):
        self.sound.add("select", "resources/sound/select.ogg")
        self.sound.add("click", "resources/sound/click-cut.ogg")
        self.sound.add("eat",  "resources/sound/chomp-cut.ogg")
        self.sound.add("hurt", "resources/sound/hurt.ogg")
        self.sound.add("gameover", "resources/sound/game_over2.ogg")


    def init_pygame(self):
        """This method initializes Pygame, the game font, screen and clock and configures some other stuff."""
        pygame.init()

        pygame.display.set_caption("Aventura no oceano")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT+INFO_BOARD_HEIGHT),0,16)
        self.clock = pygame.time.Clock()

    def init_backgrounds(self):
        """This method loads the background picture files into a list."""
        for num in range(0, NUM_OF_ROUNDS):
            self.backgrounds.append(pygame.image.load("resources/img/bg"+str(num+1)+".png").convert())
    
    #TODO Change name to init_widgets
    def init_buttons(self):
        """Initialize the buttons used in all screens of the game"""
        
        self.gui.create_button("init", "INICIAR", (100,30))
        self.gui.create_button("exit", "SAIR", (100,30))
        self.gui.create_button("back", "VOLTAR", (100,30))
        self.gui.create_button("highscore", "RANKING", (100, 30))
        self.gui.create_textbox("nickname", 120)
        
    def run(self):
        """This function consists of a loop that calls the three game loops one afther another:
            the initial screen loop, game loop and game over/highscore screen loop.
            If player doesn't quit the game after Game Over screen, state.reset() is called
            to reset game state."""

        while True:
            self.state.reset()
            self.initial_screen()
            self.game_loop()
            
            #Necessary to check if player made a high score
            self.load_ranking()

            #If High scores table is full but current score is better than the worst
            #high score on the table or if the high scores table is not full 
            #go to high scores screen, otherwise go to game over screen. 
            if len(self.rank) < 10 or self.state.score > self.rank[0][1]:
                self.highscore()
            else:
                self.game_over()


    def render_board(self):
        """This function renders information about lives, level and score on screen."""

        self.screen.fill((0,0,0), (0, SCREEN_HEIGHT, SCREEN_WIDTH, INFO_BOARD_HEIGHT))
        level_txt = "Nivel: "+str(self.state.level)
        lives_txt = "Vidas: "+str(self.state.lives)
        score_txt = "Pontos: "+str(self.state.score)

        self.screen.blit(self.gui.get_text(level_txt, size = "medium"),(0, SCREEN_HEIGHT))
        self.screen.blit(self.gui.get_text(lives_txt, size = "medium"),(100, SCREEN_HEIGHT))
        self.screen.blit(self.gui.get_text(score_txt, size = "medium"),(200, SCREEN_HEIGHT))
        if self.state.imune != 0:
            pygame.draw.line(self.screen, (255,0,0), (5, SCREEN_HEIGHT+STD_FONT_SIZE), (self.state.imune*3,SCREEN_HEIGHT+STD_FONT_SIZE), 3)


    def initial_screen(self):
        """The game's starting screen"""
        start_screen = pygame.image.load(START_SCREEN_IMG).convert_alpha()

        start_button_position = 5, 400
        exit_button_position = 5, 440

        self.gui.put_widget("init", start_button_position)
        self.gui.put_widget("exit", exit_button_position)

        while True:

            self.screen.fill((0,0,255))
            self.screen.blit(start_screen, (0,0))
            self.screen.blit(self.gui.get_text("Criado por Anderson S. Freixo"), (0, SCREEN_HEIGHT))
            self.screen.blit(self.gui.get_text("anderson.freixo@gmail.com"), (0, SCREEN_HEIGHT+20))
            self.gui.render(self.screen)

            events = self.gui.process(pygame.event.get())
            if events:
                for event in events:
                    type, name = event
                    if type == "quit":
                            exit()
                    elif type == "cursor-over":
                        self.sound.play("select")
                    elif type == "clicked":
                        self.sound.play("click")
                        sleep(1)
                        if name == "init":
                            self.gui.remove_widget("init")
                            self.gui.remove_widget("exit")
                            return
                        elif name == "exit":
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
    
    def assembly_hs_board(self, highlight = None):
        """Returns a surface with the assembled high score board. 
        Optional parameter highlight indicates a score to be highlighted"""
        
        self.load_ranking()
        #High score table
        board = pygame.Surface((160,180))

        #The table is organized from lower to higher score, but its shown
        #from higher to lower, so we must reverse it. 
        count = 1
        for hs in reversed(self.rank):
            color = (255, 0, 0) if hs == highlight else (255, 255, 255)
            txt_surf = self.gui.get_text(str(count) + "  " + hs[0] + " " + str(hs[1]), color)
            board.blit(txt_surf, (0, 15 * count))
            count+=1 
        return board 

    def highscore(self):
        
        pygame.mouse.set_visible(True)
        textbox_x = 5
        textbox_y = SCREEN_HEIGHT 
        nickname_text_position = textbox_x, textbox_y 

        self.gui.put_widget("nickname", nickname_text_position) 
        self.gui.set_focus("nickname")
        score_msg_surface = self.gui.get_text("Você entrou para o ranking!")
        instruct_msg_surface = self.gui.get_text("Digite seu nickname e aperte enter!")

        hs_screen = pygame.image.load(HIGHSCORE_SCREEN_IMG).convert_alpha()
         
        #High score table
        position = 0   #stores the position where to put the new high score

        #The table is organized from lower to higher score, but its shown
        #from higher to lower, so we must reverse it. If current score
        #is higher than some score in the table, we add the new one 
        #before it. 

        while True:

            self.screen.fill((0,0,255))
            self.screen.blit(hs_screen, (0,0))
            self.screen.blit(score_msg_surface, (5, SCREEN_HEIGHT-30))
            self.screen.blit(instruct_msg_surface, (5, SCREEN_HEIGHT-15))
            self.gui.render(self.screen)

            events = self.gui.process(pygame.event.get())
            if events:

                for event in events:
                    type, name = event
                    if type == "quit":
                            exit()

                    #Player submited nickname for high score
                    elif type == "submit":
                        if len(self.rank) >= 10:
                            #The first score is the lowest one
                            self.rank.pop(0)
                        #Insert new score and sort list again
                        self.rank.append((name, self.state.score))
                        self.rank.sort(key = lambda row: row[1])
                        #Rewrite rank file with new score
                        with open(RANK_TXT, "w") as file:
                            for player, rank in self.rank: 
                                file.write(player+":"+str(rank)+"\n")
                        self.gui.remove_widget("nickname")
                        
                        self.screen.blit(self.assembly_hs_board((name, self.state.score)), (5, SCREEN_HEIGHT - 220))

                        pygame.display.update()
                        sleep(3)
                        return()
            pygame.display.update()


    def game_over(self):

        """The Game Over screen"""
        
        pygame.mouse.set_visible(True)
        back_button_position = 5, 400
        exit_button_position = 5, 440
        
        self.gui.put_widget("back", back_button_position)
        self.gui.put_widget("exit", exit_button_position)

        score_txt = "Score: "+str(self.state.score)
        score_surface = self.gui.get_text(score_txt)
        
        go_screen = pygame.image.load(GAMEOVER_SCREEN_IMG).convert_alpha()

        while True:

            self.screen.fill((0,0,255))
            self.screen.blit(go_screen, (0,0))
            self.screen.blit(score_surface,(0,0))
            self.gui.render(self.screen)

            events = self.gui.process(pygame.event.get())
            if events:

                for event in events:
                    type, name = event
                    if type == "quit":
                            exit()
                    elif type == "cursor-over":
                        self.sound.play("select")
                    elif type == "clicked":
                        self.sound.play("click")
                        sleep(1)
                        if name == "back":
                            self.gui.remove_widget("back")
                            self.gui.remove_widget("exit")
                            return
                        elif name == "exit":
                            exit()

            pygame.display.update()


if __name__ == "__main__":
    app = App()
    app.run()
