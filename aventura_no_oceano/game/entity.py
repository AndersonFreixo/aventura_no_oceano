import pygame
from common.constants import *

class Entity:

    def __init__(self, path, frames_num, position):
        self.x, self.y = position
        self.framecounter = 0
        self.frames_num = frames_num
        self.surfaces = []
        for n in range(frames_num):
            self.surfaces.append(pygame.image.load(path+str(n)+".png").convert_alpha())

    def get_position(self):
        return self.x, self.y

    def get_size(self):
        return self.surfaces[0].get_width(), self.surfaces[0].get_height()

    def move(self):
        pass

    def render(self, screen):
        #framecounter is incremented by one in each iteration of game loop
        #and goes back to 0 when framecounter == STD_FRAME_RATE
        self.framecounter = (self.framecounter+1) % STD_FRAME_RATE

        #all frames of the animation should run once per second
        #so to check which animation frame must be rendered we should
        #split the number of frames/seconds in a number of parts equal
        #to movements.
        frame = self.framecounter // (STD_FRAME_RATE // self.frames_num)

        screen.blit(self.surfaces[frame], (self.x-self.surfaces[frame].get_width()/2,
                                            self.y-self.surfaces[frame].get_height()/2))
        

class Enemy(Entity):
    def __init__(self, path, frames_num, position, direction, speed):
        #Direction (x, y) x = -1 LEFT, 1 RIGHT y = -1 UP, 1 DOWN
        self.horizontal_dir, self.vertical_dir = direction
        self.speed = speed
        super().__init__(path, frames_num, position)

    def is_touching(self, pos, entity_size):

        return pygame.Rect((self.x, self.y), self.get_size()).colliderect(pygame.Rect((pos),(entity_size)))


    def render(self, screen):
        #framecounter is incremented by one in each iteration of game loop
        #and goes back to 0 when framecounter == STD_FRAME_RATE
        self.framecounter = (self.framecounter+1) % STD_FRAME_RATE

        #all frames of the animation should run once per second
        #so to check which animation frame must be rendered we should
        #split the number of frames/seconds in a number of parts equal
        #to movements.
        frame = self.framecounter // (STD_FRAME_RATE // self.frames_num)
        surface = self.surfaces[frame]
        if self.horizontal_dir > 0:
            surface = pygame.transform.flip(surface, True, False)

        screen.blit(surface, (self.x-self.surfaces[frame].get_width()/2,
                                            self.y-self.surfaces[frame].get_height()/2))


class KillerWhale(Enemy):
    def __init__(self, position, direction, speed):
        super().__init__(KILLER_WHALE_IMG, 2, position,direction, speed)

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
        super().__init__(SCUBA_DIVER_IMG, 4, position,direction, speed)

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
        super().__init__(NARWAL_IMG, 1, position,direction, speed)

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
        super().__init__(PLAYER_IMG, 4, position)
        self.lastx = 0
        self.direction = -1
        self.last_dir = 0
    def move(self, coord):
        self.lastx = self.x
        self.x = coord[0]
        self.y = coord[1]
    def render(self, screen):
        #framecounter is incremented by one in each iteration of game loop
        #and goes back to 0 when framecounter == STD_FRAME_RATE
        self.framecounter = (self.framecounter+1) % STD_FRAME_RATE

        #all frames of the animation should run once per second
        #so to check which animation frame must be rendered we should
        #split the number of frames/seconds in a number of parts equal
        #to movements.
        frame = self.framecounter // (STD_FRAME_RATE // self.frames_num)
        player_surface = self.surfaces[frame]
        if self.x - self.lastx != 0:
            self.direction = 1 if self.x - self.lastx > 0 else -1

        if self.direction == 1:
            player_surface = pygame.transform.flip(player_surface, True, False)
        screen.blit(player_surface, (self.x-self.surfaces[frame].get_width()/2,
                                            self.y-self.surfaces[frame].get_height()/2))
    


class Food(Entity):
    def __init__(self, position):
        super().__init__(KRILL_IMG, 1, position)

    def is_covered(self, pos, entity_size):

        return pygame.Rect((pos[0]-entity_size[0]//2,
                           pos[1]-entity_size[1]//2),
                           entity_size).contains(pygame.Rect((self.x-self.surfaces[0].get_width()//2,
                                                     self.y-self.surfaces[0].get_height()//2), self.get_size()))
