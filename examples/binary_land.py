import sys
import random
sys.path.extend(['.', '..'])
import tinygame as tg


class Penguin():
	DIRECTION_OFFSET_UP = 0
	DIRECTION_OFFSET_DOWN = 2
	DIRECTION_OFFSET_RIGHT = 4
	DIRECTION_OFFSET_LEFT = 6

	def __init__(self, animation_filename, x, y):
		"""
		"""
		self.animation_character_map = tg.character_map.load(animation_filename)
		self.x, self.y = x,y # Set the desited position
		self.dx, self.dy = 0, 0
		self.direction_offset = self.DIRECTION_OFFSET_UP
		self.animation_offset = 0
		self.age = 0
		self.animate = True

	def animated_current_sprite(self):
		"""
		Get the current sprite (CharacterMap) to draw for animating the Bird

		return: CharacterMap you may use to draw the animated Bird
		"""
		offset = -4*(self.direction_offset + self.animation_offset)
		cm = tg.character_map.CharacterMap(4, 3)
		cm.draw_image(0, offset, self.animation_character_map)
		return cm

	def draw(self, character_map):
		"""
		Draws the animated Bird on the given CharacterMap

		character_map: A CharacterMap on which to draw the current animation image of the Bird	
		"""
		character_map.draw_image(2+self.x/12, 1+self.y/12, self.animated_current_sprite(), '#') # Draw the current Bird animation image at the current position

	def collides(self, x0, y0, level_map):
		for y in xrange(y0, y0 + 3*12):
			for x in xrange(x0, x0 + 4*12):
				x_map, y_map = x / 12 / 4, y / 12 / 3
				if x_map < 0 or y_map < 0 or x_map >= 15 or y_map >= 10 or level_map[x_map, y_map] == '#':
					return True
		return False
				

	def tick(self, level_map):
		if self.animate:
			self.age += 1
			self.animation_offset = self.age / 4 % 2
		next_x, next_y = self.x + self.dx, self.y + self.dy
		if not self.collides(next_x, next_y, level_map):
			self.x, self.y = next_x, next_y
		self.dx, self.dy = 0, 0
		self.animate = False
					
	def up(self):
		self.direction_offset = self.DIRECTION_OFFSET_UP
		self.dx, self.dy = 0, -6
		self.animate = True

	def down(self):
		self.direction_offset = self.DIRECTION_OFFSET_DOWN
		self.dx, self.dy = 0, 6
		self.animate = True

	def left(self):
		self.direction_offset = self.DIRECTION_OFFSET_LEFT
		self.dx, self.dy = -8, 0
		self.animate = True

	def right(self):
		self.direction_offset = self.DIRECTION_OFFSET_RIGHT
		self.dx, self.dy = 8, 0
		self.animate = True

			
class BinaryLandUI():
	"""
	A User Interface class to handle all the game logic and rendering of the game Binary Land
	"""

	FPS = 25.0 # Frame rate in frames per second


	BRICK = tg.character_map.parse("[]")

	BLOCK = tg.character_map.parse("|  |" + "\n" +\
                                       "|  |" + "\n" +\
                                       "|__|")
	GOAL = tg.character_map.parse("/\\/\\" + "\n" +\
                                      "\\0 /" + "\n" +\
                                      " \\/ ")

	BLOCK_TOP = tg.character_map.parse('|""|' + "\n" +\
                                           '|  |' + "\n" +\
                                           '|__|')

	def __init__(self):
		"""
		"""
		self.width = 4*15
		self.height =3*10
		self.boy = Penguin("examples/data/binary_land/boy.txt", 12*8*4, 12*9*3)
		self.girl = Penguin("examples/data/binary_land/girl.txt", 12*6*4, 12*9*3)
		self.screen = tg.character_display.CharacterDisplay(self.width+4, self.height+2)
		self.bg = tg.character_display.CharacterDisplay(self.width+4, self.height+2)
		self.done = False
		self.level_map = tg.character_map.load("examples/data/binary_land/level1.txt")

	def draw_level(self):
		self.bg.fill(' ')
		for x in xrange(0, self.width+4, 2):
			self.bg.draw_image(x, 0, self.BRICK)
			self.bg.draw_image(x, 1 + 3*10, self.BRICK)
		for y in xrange(0, self.height):
			self.bg.draw_image(0, 1+y, self.BRICK)
			self.bg.draw_image(2+15*4, 1+y, self.BRICK)

		self.bg.draw_image(2 + 4*7, 1, self.GOAL)
		self.bg.draw_image(2 + 4*7, 1+3*2, self.BLOCK_TOP)
		for y in xrange(3, self.height-6, 3):
			self.bg.draw_image(2+4*7, 1+3*2+y, self.BLOCK)
		for i in xrange(0, 10):
			for j in xrange(0, 15):
				if self.level_map[j, i] == '#':
					is_top = True
					if i > 0 and self.level_map[j, i - 1] == '#': is_top = False
					self.bg.draw_image(2 + j*4, 1 + i*3, self.BLOCK_TOP if is_top else self.BLOCK)
		self.bg.write_text(2 + 4 *8 - 6, 1 + 10*3, " ( START  ) ")
		self.bg.write_text(2 + 4 *8 - 6, 0, " ( GOAL  ) ")

	def play(self):
		"""
		"""
		metronome = tg.Metronome(1/self.FPS) # Use a metronome to maintain specified fps
		self.draw_level()
		while not self.done:
			k = tg.keyboard.getch() # Read key presses
			if k == tg.keyboard.KEY_UP:
				self.boy.up()
				self.girl.up()
			if k == tg.keyboard.KEY_DOWN:
				self.boy.down()
				self.girl.down()
			if k == tg.keyboard.KEY_LEFT:
				self.girl.right()
				self.boy.left()
			if k == tg.keyboard.KEY_RIGHT:
				self.girl.left()
				self.boy.right()
			if k == tg.keyboard.KEY_ESCAPE:
				self.done = True
				break

			self.screen.draw_image(0, 0, self.bg)
			self.boy.draw(self.screen) #
			self.boy.tick(self.level_map) 
			self.girl.draw(self.screen) #
			self.girl.tick(self.level_map) 
			metronome.wait_for_tick() # wait for a metronome tick to keep the pace of the game at one rate. This will keep pase at FPS
			self.screen.show() # Update the display with the newest frame

def main():
	"""
	The main entrypoint to the Flappy Bird game. It initializes librarys including tinygame and creates the Game UI
	"""
	tg.initialize()
	try:
		while True:
			gameui = BinaryLandUI()
			gameui.play() # simply start playing
			if gameui.exit: break # Keep playing till the user wants to exit
	finally:
		tg.quit()

if __name__ == "__main__":
	main()
