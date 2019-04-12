import pygame

from pygame.locals import *

class MiniGui:
	def __init__(self):
		self.txt_size = 25
		self.txt_font = None
		self.txt_font_name = None

		self.button_color = 100, 180, 255
		self.over_button_color = 0, 130, 255
		self.text_color = 255, 255, 255


	def run(self):
		self.txt_font = pygame.font.Font(self.txt_font_name, self.txt_size)
		
	def get_text(self, text_str, color = None):
		if color == None:
			color = self.text_color 
		return self.txt_font.render(text_str, 1, color)
	
	def get_button(self, text_str, size, bg_color, color = None):
		button = pygame.Surface(size)
		button.fill(bg_color)
		text = self.get_text(text_str, color)
		text_size = text.get_size()
		button.blit(text, ((size[0]-text_size[0])/2, (size[1]-text_size[1])/2))
		return button
	
	def get_txt_size(self, str):
		return self.txt_font.size(str)
		
		