import pygame

BUTTON_COLOR = 100, 180, 255        #Light blue
OVER_BUTTON_COLOR =  0, 130, 255    #A darker blue
TXT_COLOR = 255,255,255             #White

TXT_SIZE = 25
TXT_FONT = None
TXT_NAME = None

from pygame.locals import *

class MiniGui:
	def __init__(self):

		self.buttons = dict()
		self.active = dict()
		self.txt_font = pygame.font.Font(TXT_NAME, TXT_SIZE)
		

	def run(self, surface):
		"""This method checks if the mouse is over the buttons and blits them."""
	
		for name, position in self.active.items():
				
			if Rect((position), self.buttons[name][0].get_size()).collidepoint(pygame.mouse.get_pos()):
			
				clicked = 1
			else: clicked = 0

			surface.blit(self.buttons[name][clicked], position)
		

	def remove_button(self, name):
		self.active.pop(name)

	def what_is_clicked(self):

		for name, position in self.active.items():
			if Rect((position, self.buttons[name][0].get_size())).collidepoint(pygame.mouse.get_pos()):
				return name

	def create_button(self, name, text_str, size):

		"""This method is used to create a button. It works creating a tuple of two different buttons.
                    One to be used when the mouse is over the button, and the other to be used otherwise."""
		button = pygame.Surface(size)
		button_over = pygame.Surface(size)

		button.fill(BUTTON_COLOR)
		button_over.fill(OVER_BUTTON_COLOR)

		text = self.get_text(text_str, TXT_COLOR)
		text_size = text.get_size()

		button.blit(text, ((size[0]-text_size[0])/2, (size[1]-text_size[1])/2))
		button_over.blit(text, ((size[0]-text_size[0])/2, (size[1]-text_size[1])/2))
		self.buttons[name] = (button, button_over)

	def put_button(self, name, position):
		self.active[name] = position


	def get_text(self, text_str, color = TXT_COLOR):

		return self.txt_font.render(text_str, 1, TXT_COLOR)
	
	def get_button(self, name):

		return self.buttons[name]
	
	def get_txt_size(self, str):
		return self.txt_font.size(str)
		
		
