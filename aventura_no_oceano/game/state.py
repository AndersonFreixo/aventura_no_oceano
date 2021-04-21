from ..common.constants import *
from ..data import levels
from ..game import entity
import random

class State:
    def __init__(self):
        self.entities = []
        self.food = []
        self.lives = 3
        self.level = 0
        self.score = 0
        self.imune = 0        #a counter that specifies immunity period
        self.round = 0

    def populate(self):
        self.entities = levels.get_level(self.level)
        self.food = [entity.Food((random.randint(1, int(SCREEN_WIDTH/FOOD_STD_WIDTH))*FOOD_STD_WIDTH,
                    random.randint(1, int(SCREEN_HEIGHT/FOOD_STD_HEIGHT)*FOOD_STD_HEIGHT))) for _ in range(FOOD_NUM)]

    def update_level(self):
        """This function resets entities and food for each level."""
        self.level+=1
        self.populate()
        self.imune = STD_FRAME_RATE
        if self.level !=0:
            #Each level adds 50pts to the score
            self.score+= 50
            if self.level%2 == 0:
                #Adds 1 life for each 2 levels
                self.lives+=1


#        if self.level//MAX_LEVELS > 0 and self.level%MAX_LEVELS == 0:
        self.round = (self.level//MAX_LEVELS)%NUM_OF_ROUNDS


    def reset(self):
        self.food = []
        self.lives = 3
        self.level = 0
        self.score = 0
        self.imune = 0
        self.round = 0


    def update(self):
        #When imune > 0 hero doesn't lose life points when touching an enemy.
        if self.imune > 0:
            self.imune-=1

        #Finished the level! Go to the next one!
        if len(self.food) == 0:
            self.update_level()

        for ent in self.entities:
            ent.move()
