import entity
from constants import *

def get_level(lvl):
	"""Returns the entities from each level. Also defines the speed of the game, based on the level"""
	 
	speed = (lvl//MAX_ROUNDS)+2
	lvl%= 5	
	#print("Level ", lvl, "Speed", speed)

	levels = {	0: [entity.KillerWhale((1,1),(1,1), speed), 
			entity.KillerWhale((SCREEN_WIDTH, SCREEN_HEIGHT),(-1,-1), speed)],

			1: [entity.KillerWhale((1,1),(1,1), speed), 
			entity.KillerWhale((SCREEN_WIDTH, SCREEN_HEIGHT),(-1,-1), speed), 
			entity.ScubaDiver((160,240),(1,1), speed)],

			2: [entity.KillerWhale((1,1),(1,1), speed), 
			entity.KillerWhale((SCREEN_WIDTH, SCREEN_HEIGHT),(-1,-1), speed), 
			entity.ScubaDiver((0,140),(1,1), speed), 
			entity.ScubaDiver((320,240),(-1,1), speed)],

			3: [entity.KillerWhale((1,1),(1,1), speed), 
			entity.KillerWhale((SCREEN_WIDTH, SCREEN_HEIGHT),(-1,-1), speed),
			entity.KillerWhale((100,1),(-1,1), speed), 
			entity.KillerWhale((1,100),(-1,1), speed), 
			entity.ScubaDiver((0,140),(1,1), speed), 
			entity.ScubaDiver((320,240),(-1,1), speed)],

			4: [entity.KillerWhale((1,1),(1,1), speed), 
			entity.KillerWhale((SCREEN_WIDTH, SCREEN_HEIGHT),(-1,-1), speed),
			entity.KillerWhale((100,1),(-1,1), speed), 
			entity.KillerWhale((1,100),(-1,1), speed), 
			entity.ScubaDiver((0,140),(1,1), speed), 
			entity.ScubaDiver((320,240),(-1,1), speed),
		        entity.Narwal((SCREEN_WIDTH//2, SCREEN_HEIGHT),(0,0), speed)]

	}
	return levels[lvl]



