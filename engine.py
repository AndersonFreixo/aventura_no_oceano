import pygame
import random 
from pygame.locals import *
from sys import exit
from time import sleep

import entity
import levels
import minigui
from constants import *

class Engine:
	def __init__(self):
		self.entities = []
		self.food = []
		self.backgrounds = []
		self.sounds = dict()
		self.st_counter = 0 #keeps track of the current soundtrack file loaded
		self.lives = 3
		self.level = 0
		self.score = 0
		self.imune = 0		#a counter that specifies immunity period
		self.background_num = 0 #active background id
		self.state = "game"
	
		self.game_font = None   # initialized in init_pygame method
		self.screen = None      #
		self.clock = None       #

		self.soundtrack = ["sound/st_01.ogg", "sound/st_02.ogg", "sound/st_03.ogg", "sound/st_04.ogg"]

		self.init_pygame()
		self.init_sounds()
		self.init_backgrounds()
		self.gui = minigui.MiniGui()
		self.init_buttons()
		self.player = entity.Player((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

	def init_sounds(self):
		self.sounds["select"] = pygame.mixer.Sound("sound/select.ogg")
		self.sounds["click"] = pygame.mixer.Sound("sound/click-cut.ogg")
		self.sounds["eat"] = pygame.mixer.Sound("sound/chomp-cut.ogg")	
		self.sounds["hurt"] = pygame.mixer.Sound("sound/hurt.ogg")
		self.sounds["gameover"] = pygame.mixer.Sound("sound/game_over2.ogg")
	def reset(self):
		"""This method resets all variables to their initial values."""
		self.food = []
		self.lives = 3
		self.level = 0
		self.score = 0
		self.imune = 0			
		self.background_num = 0;
	

	def play_sound(self, name):
		self.sounds[name].play()
		
	def init_pygame(self):
		"""This method initializes Pygame, the game font, screen and clock and configures some other stuff."""
		pygame.init()
		
		pygame.display.set_caption("Aventura no oceano")
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT+INFO_BOARD_HEIGHT),0,16)
		self.clock = pygame.time.Clock()
		
	def init_backgrounds(self):
		"""This method loads the background picture files into a list."""
		for num in range(0, NUM_OF_BGS):
			self.backgrounds.append(pygame.image.load("img/bg"+str(num+1)+".png").convert())

	def init_buttons(self):
		"""This method initializes the buttons used in all screens of the game"""
		self.gui.create_button("init", "INICIAR", (100,30))
		self.gui.create_button("exit", "SAIR", (100,30))
		self.gui.create_button("back", "VOLTAR", (100,30))
	
	def run(self):
		"""This function consists of a loop the calls the three game loops one afther another:
			the initial screen loop, game loop and game over screen loop.
			If player doesn't quit the game after Game Over screen, self.reset() is called
			to reset game state."""

		while True:
			self.reset()
			self.initial_screen()
			self.game_loop()
			self.game_over()
	
	
	def render_board(self):
		"""This function renders information about lives, level and score on screen."""
		
		self.screen.fill((0,0,0), (0, SCREEN_HEIGHT, SCREEN_WIDTH, INFO_BOARD_HEIGHT))
		level_txt = "Nivel: "+str(self.level)
		lives_txt = "Vidas: "+str(self.lives)
		score_txt = "Pontos: "+str(self.score)
		
		self.screen.blit(self.gui.get_text(level_txt),(0, SCREEN_HEIGHT))
		self.screen.blit(self.gui.get_text(lives_txt),(100, SCREEN_HEIGHT))
		self.screen.blit(self.gui.get_text(score_txt),(200, SCREEN_HEIGHT))
		if self.imune != 0:
			pygame.draw.line(self.screen, (255,0,0), (5, SCREEN_HEIGHT+STD_FONT_SIZE), (self.imune*3,SCREEN_HEIGHT+STD_FONT_SIZE), 3)
		
	def reset_level(self):
		"""This function resets entities and food for each level."""
	
		self.entities = levels.get_level(self.level)
		self.food = [entity.Food((random.randint(1, int(SCREEN_WIDTH/FOOD_STD_WIDTH))*FOOD_STD_WIDTH,
					random.randint(1, int(SCREEN_HEIGHT/FOOD_STD_HEIGHT)*FOOD_STD_HEIGHT))) for _ in range(FOOD_NUM)]

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
						
				self.play_sound("select")

			for event in pygame.event.get():
					if event.type == QUIT:
						exit()
					if event.type == MOUSEBUTTONDOWN:
						self.play_sound("click")
						
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
		pygame.mixer.music.load(self.soundtrack[0])
		pygame.mixer.music.play(-1)
		pygame.mixer.music.set_volume(0.3)

		while True:
			self.clock.tick(STD_FRAME_RATE)
			if self.lives <= 0:
				self.play_sound("gameover")
				pygame.mixer.music.stop()
				return
			
			if self.imune > 0: self.imune-=1      #When imune > 0 hero doesn't lose life points when touching an enemy.
			if len(self.food) == 0:               #Finished the level! Go to the next one!
				
				self.reset_level()
				self.imune = STD_FRAME_RATE


				if self.level !=0:            #Each level adds 50pts to the score
					self.score+= 50
					if self.level%2 == 0: #Adds 1 life for each 2 levels
						self.lives+=1
	
				
				if self.level//MAX_ROUNDS > 0 and self.level%MAX_ROUNDS == 0:
					if self.background_num < NUM_OF_BGS-1:
						self.background_num+=1
						self.st_counter+=1 
					else:
						self.background_num = 0
						self.st_counter = 0

	      				#Change to next song. 
					pygame.mixer.music.load(self.soundtrack[self.st_counter])
					pygame.mixer.music.play(-1)
					pygame.mixer.music.set_volume(0.3)


				self.level+=1			
			
			for event in pygame.event.get():
				if event.type == QUIT:
					exit()
	
			self.screen.blit(self.backgrounds[self.background_num],(0,0))
			pos = pygame.mouse.get_pos()
			self.player.move(pos)
			
			for ent in self.entities:
				ent.move()
				#if enemy touches player
				if ent.is_touching(self.player.get_position(), self.player.get_size()) and self.imune == 0:
					if self.lives > 1:
						self.play_sound("hurt")
					self.lives-=1
					self.imune = STD_FRAME_RATE				
					
				ent.render(self.screen)
	
			for fd in self.food:
				#if player surface covers food surface
				if fd.is_covered(self.player.get_position(), self.player.get_size()):
					self.play_sound("eat")					
					self.score+=10
					self.food.remove(fd)
				fd.render(self.screen)
	
			self.player.render(self.screen)
			self.render_board()
	
			pygame.display.update()
		
	def game_over(self):
		"""The Game Over screen"""

		pygame.mouse.set_visible(True)	
		back_button_position = 5, 400
		exit_button_position = 5, 440
		
		score_txt = "Score: "+str(self.score)
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
				
				self.play_sound("select")

			for event in pygame.event.get():
					if event.type == QUIT:
						exit()
					if event.type == MOUSEBUTTONDOWN:
						self.play_sound("click")
						
						sleep(1)
						if self.gui.what_is_clicked() == "back":

							self.gui.remove_button("back")
							self.gui.remove_button("exit")
							return
						elif self.gui.what_is_clicked() == "exit":
							exit()
			pygame.display.update()



