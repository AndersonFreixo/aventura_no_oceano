import pygame
import random 
from pygame.locals import *
from sys import exit

import entity
import levels
import minigui
from constants import *

class Engine:
	def __init__(self):
		self.entities = []
		self.food = []
		self.backgrounds = []
		self.lives = 3
		self.level = 0
		self.score = 0
		self.imune = 0			#a counter that specifies immunity period
		self.background_num = 0 #active background id
		self.state = "game"
	
		self.game_font = None # initialized in init_pygame method
		self.screen = None    #
		self.clock = None     #


		self.init_pygame()
		self.init_backgrounds()
		self.gui = minigui.MiniGui()
		self.gui.run()
		self.player = entity.Player((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

	def reset(self):
		"""This method resets all variables to their initial values."""
		self.food = []
		self.lives = 3
		self.level = 0
		self.score = 0
		self.imune = 0			
		self.background_num = 0;
		
	def init_pygame(self):
		"""This method initializes Pygame, the game font, screen and clock and configures some other stuff."""
		pygame.init()
		
		pygame.display.set_caption("Aventura no oceano")
		#self.game_font = pygame.font.Font(None, STD_FONT_SIZE)
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT+INFO_BOARD_HEIGHT),0,16)
		self.clock = pygame.time.Clock()
		
	def init_backgrounds(self):
		"This method loads the background picture files into a list."
		for num in range(0, NUM_OF_BGS):
			self.backgrounds.append(pygame.image.load("img/bg"+str(num+1)+".png").convert())
	
	def run(self):
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
		
		#self.screen.blit(level_txt,(0, SCREEN_HEIGHT))
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

		start_screen = pygame.image.load(START_SCREEN_IMG).convert_alpha()
		
		start_button= self.gui.get_button("INICIAR", (100,30), (100,180,255))
		start_button_over = self.gui.get_button("INICIAR", (100,30), (0, 130, 255))
		
		exit_button = self.gui.get_button("SAIR", (100,30), (100,180,255))
		exit_button_over = self.gui.get_button("SAIR", (100,30), (0, 130, 255))

		start_button_position = 5, 400
		exit_button_position = 5, 440	
		
		while True:
			start = start_button
			exit_b = exit_button
			
			if Rect((start_button_position), start.get_size()).collidepoint(pygame.mouse.get_pos()):
				start = start_button_over
			if Rect((exit_button_position), exit_b.get_size()).collidepoint(pygame.mouse.get_pos()):
				exit_b = exit_button_over

			self.screen.fill((0,0,255))
			self.screen.blit(start_screen, (0,0))
			self.screen.blit(start,start_button_position)
			self.screen.blit(exit_b,exit_button_position)
			self.screen.blit(self.gui.get_text("Criado por Anderson S. Freixo"), (0, SCREEN_HEIGHT))
			self.screen.blit(self.gui.get_text("anderson.freixo@gmail.com"), (0, SCREEN_HEIGHT+20))
				

			for event in pygame.event.get():
					if event.type == QUIT:
						exit()
					if event.type == MOUSEBUTTONDOWN:
						if pygame.Rect((start_button_position), start.get_size()).collidepoint(pygame.mouse.get_pos()):
							return
						elif pygame.Rect((exit_button_position), exit_b.get_size()).collidepoint(pygame.mouse.get_pos()):
							exit()
			pygame.display.update()
			
	def game_loop(self):
		"""This is the game engine's main loop"""		
		pygame.mouse.set_visible(False)	
		while True:
			self.clock.tick(STD_FRAME_RATE)
			if self.lives <= 0:
				return
			
			if self.imune > 0: self.imune-=1 #When imune > 0 hero doesn't lose life points when touching an enemy.
			if len(self.food) == 0: #Finished the level! Go to the next one!
				
				self.reset_level()
				self.imune = STD_FRAME_RATE 
				if self.level !=0: #Each level adds 50pts to the score
					self.score+= 50
					if self.level%2 == 0: #Adds 1 life for each 2 levels
						self.lives+=1
	
				
				if self.level//MAX_ROUNDS > 0 and self.level%MAX_ROUNDS == 0 and self.background_num < NUM_OF_BGS-1:
					self.background_num+=1
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
					self.lives-=1
					self.imune = STD_FRAME_RATE				
					
				ent.render(self.screen)
	
			for fd in self.food:
				#if player surface covers food surface
				if fd.is_covered(self.player.get_position(), self.player.get_size()):
					
					self.score+=10
					self.food.remove(fd)
				fd.render(self.screen)
	
			self.player.render(self.screen)
			self.render_board()
	
			pygame.display.update()
		
	def game_over(self):
		pygame.mouse.set_visible(True)	
		back_button_position = 5, 400
		exit_button_position = 5, 440
		
		score_txt = "Score: "+str(self.score)
		score_surface = self.gui.get_text(score_txt)
		go_screen = pygame.image.load(GAMEOVER_SCREEN_IMG).convert_alpha()
	
		back_button= self.gui.get_button("VOLTAR", (100,30), (100,180,255))
		back_button_over = self.gui.get_button("VOLTAR", (100,30), (0, 130, 255))
		
		exit_button = self.gui.get_button("SAIR", (100,30), (100,180,255))
		exit_button_over = self.gui.get_button("SAIR", (100,30), (0, 130, 255))
		
		while True:
			back = back_button
			exit_b = exit_button
			if Rect((back_button_position), back_button.get_size()).collidepoint(pygame.mouse.get_pos()):
				back = back_button_over
			if Rect((exit_button_position), exit_button.get_size()).collidepoint(pygame.mouse.get_pos()):
				exit_b = exit_button_over	
			self.screen.fill((0,0,255))
			self.screen.blit(go_screen, (0,0))
			self.screen.blit(score_surface,(0,0))
			self.screen.blit(back,back_button_position)
			self.screen.blit(exit_b,exit_button_position)
			

			for event in pygame.event.get():
					if event.type == QUIT:
						exit()
					if event.type == MOUSEBUTTONDOWN:
						if pygame.Rect((back_button_position), back_button.get_size()).collidepoint(pygame.mouse.get_pos()):
							return
						elif pygame.Rect((exit_button_position), exit_button.get_size()).collidepoint(pygame.mouse.get_pos()):
							exit()
			pygame.display.update()