import pygame
from constants import *

class Entity:

	def __init__(self, image_file_name, position):
		self.x, self.y = position
		self.surface = pygame.image.load(image_file_name).convert_alpha()

	def get_position(self):
		return self.x, self.y

	def get_size(self):
		return self.surface.get_width(), self.surface.get_height()

	def move(self):
		pass

	def render(self, screen):
		screen.blit(self.surface, (self.x-self.surface.get_width()/2, self.y-self.surface.get_height()/2))


class Enemy(Entity):
	def __init__(self, image_file_name, position, direction, speed):
		#Direction (x, y) x = -1 LEFT, 1 RIGHT y = -1 UP, 1 DOWN
		self.horizontal_dir, self.vertical_dir = direction 
		self.speed = speed 
		super().__init__(image_file_name, position)

	def is_touching(self, pos, entity_size):

		return pygame.Rect((self.x, self.y), self.get_size()).colliderect(pygame.Rect((pos),(entity_size)))


	def render(self, screen):
		if self.horizontal_dir <=0:
			screen.blit(self.surface, (self.x-self.surface.get_width()/2, self.y-self.surface.get_height()/2))
		else:
			screen.blit(pygame.transform.flip(self.surface, True, False), (self.x-self.surface.get_width()/2, self.y-self.surface.get_height()/2))
class KillerWhale(Enemy):
	def __init__(self, position, direction, speed):
		super().__init__(KILLER_WHALE_IMG, position,direction, speed)
			
	def move(self):
		"""The entity move function. This entity has a bouncing movement in all directions."""
		#The goal here is to have a bouncing movement. 
		#So the first part of the code checks if the entity has
		#reached any of the screen's edges. If so, it changes to
		#the opposite direction.
		width, height = self.get_size()
		if self.x - width/2 <=0 and self.horizontal_dir == -1:
			self.horizontal_dir = 1
		elif self.x + width/2 >= SCREEN_WIDTH and self.horizontal_dir == 1:
			self.horizontal_dir = -1
		if self.y - height/2 <=0 and self.vertical_dir == -1:
			self.vertical_dir = 1
		elif self.y + height/2 >= SCREEN_HEIGHT and self.vertical_dir == 1:
			self.vertical_dir = -1

		#This is the movement part.
		self.x+=self.horizontal_dir*self.speed
		self.y+=self.vertical_dir*self.speed		

class ScubaDiver(Enemy):
	def __init__(self, position, direction, speed):
		super().__init__(SCUBA_DIVER_IMG, position,direction, speed)
			
	def move(self):
		"""The entity's move function."""
		#This entity moves only horizontally from one side to the other
		width, height = self.get_size()
		if self.x - width/2 <=0 and self.horizontal_dir == -1:
			self.horizontal_dir = 1
		elif self.x + width/2 >= SCREEN_WIDTH and self.horizontal_dir == 1:
			self.horizontal_dir = -1

		#This is the movement part.
		self.x+=self.horizontal_dir*self.speed

class Narwal(Enemy):
	def __init__(self, position, direction, speed):
		super().__init__(NARWAL_IMG, position,direction, speed)
			
	def move(self):
		"""The entity move function. """
		#This entity moves from the bottom of the screen to above and repeats
		#after disappearing from the screen
		_, height = self.get_size()
		if self.y < -height/2:
			self.y = SCREEN_HEIGHT

		#This is the movement part.
		self.y-=self.speed
			
			

class Player(Entity):
	def __init__(self, position):
		super().__init__(PLAYER_IMG, position)

	def move(self, coord):
		self.x = coord[0]
		self.y = coord[1]


class Food(Entity):
	def __init__(self, position):
		super().__init__(KRILL_IMG, position)

	def is_covered(self, pos, entity_size):
		
		return pygame.Rect((pos[0]-entity_size[0]//2,
						   pos[1]-entity_size[1]//2),
						   entity_size).contains(pygame.Rect((self.x-self.surface.get_width()//2,
													 self.y-self.surface.get_height()//2), self.get_size()))

