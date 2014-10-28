import sys
import random
sys.path.extend(['.', '..'])
import tinygame as tg

class Pipe():
	HEAD = tg.character_map.parse(	".======." + "\n" +
	                                "||     |" + "\n" +
	                                " ====== " )
	BODY = tg.character_map.parse(  " ||   | " )

	HEAD_MASK = tg.character_map.parse( 	" ###### " + "\n" +
	                                        "########" + "\n" +
                                                " ###### " )
	BODY_MASK = tg.character_map.parse(	" ###### " )

	def __init__(self, x, gap_y, gap_height, height):
		self.x = x
		self.width = Pipe.HEAD.width
		self.gap_y, self.gap_height, self.height = gap_y, gap_height, height
		self.age = 0

	def draw(self, character_map, mask_map):
		for y in xrange(0, self.height):
			if self.gap_y < y and y <= self.gap_y + self.gap_height: continue
			character_map.draw(self.x, y, Pipe.BODY)
			mask_map.draw(self.x, y, Pipe.BODY_MASK)

		character_map.draw(self.x, self.gap_y - Pipe.HEAD.height+1, Pipe.HEAD)
		mask_map.draw(self.x, self.gap_y - Pipe.HEAD.height+1, Pipe.HEAD_MASK)

		character_map.draw(self.x, self.gap_y + self.gap_height, Pipe.HEAD)
		mask_map.draw(self.x, self.gap_y + self.gap_height, Pipe.HEAD_MASK)

	def tick(self):
		self.x -= 1
		if self.x < 80: self.age += 1

class Bird():
	FLAP_IMPULSE = -1.0
	SPRITE0 = tg.character_map.parse("_/0=" + "\n"
                                       "\\v/ ")
	SPRITE1 = tg.character_map.parse("_/0=" + "\n"
                                        "\-/ ")
	SPRITE2 = tg.character_map.parse("_/0=" + "\n"
                                        "\^/ ")

	def __init__(self, x, y):
		self.x, self.y = x,y
		self.dy = 0
		self.animation = [self.SPRITE0, self.SPRITE1, self.SPRITE2, self.SPRITE1]
		self.age = 0

	def animated_current_sprite(self):
		return self.animation[self.age/2 % len(self.animation)]

	def draw(self, character_map):
		character_map.draw(int(self.x), int(self.y), self.animated_current_sprite(), ' ')

	def flap(self):
		self.dy = Bird.FLAP_IMPULSE
		self.age = 0

	def accelerate(self, (ax,ay)):
		self.dy += ay

	def tick(self):
		self.y += self.dy
		self.age += 1

	def collision(self, character_map):
		sprite = self.animated_current_sprite()
		for y in xrange(0, sprite.height):
			for x in xrange(sprite.width-1,0,-1):
				if sprite[x,y] != ' ' and character_map[int(self.x)+x,int(self.y)+y] != ' ':
					return int(self.x)+x,int(self.y)+y
		return None
			
class FlappyUI():
	"""
	A User Interface class to handle all the game logic and rendering of the game Flappy Bird
	"""

	GRAVITY = 0.08 # Rate of downward acceleration due to gravity
	FPS = 24.0 # Frame rate in frames per second
	ARRIVAL_RATE = 1.8 # The time (in seconds) between each pipe that arrives on the right of the screen

	def __init__(self):
		self.screen = tg.character_display.CharacterDisplay(80, 35)
		self.fg = tg.character_display.CharacterMap(80, 35)
		self.fgmask = tg.character_display.CharacterMap(80, 35)
		self.done = False
		self.faby = Bird(25, 20)
		ground_tile = tg.character_map.parse('____\n/   ')
		ground_mask = tg.character_map.parse('####\n####')
		self.fg.fill(' ')
		self.fgmask.fill(' ')
		for x in xrange(0, 80, 4):
			self.fg.draw(x, 33, ground_tile)
			self.fgmask.draw(x, 33, ground_mask)
		self.next_pipe = Pipe(160, random.randint(2,22), 8, 33)
		self.old_pipes = [self.next_pipe]
		self.score = 0

	def intro(self):
		pass

	def play(self):
		"""
		The UI plays a round of Flappy Bird until the user hits something 
		"""
		metronome = tg.Metronome(1/self.FPS) # Use a metronome to maintain specified fps

		while not self.done:
			k = tg.keyboard.getch(1/self.FPS)
			if k == ' ':
				self.faby.flap() # Use the space key to flap the bird wings
			if k == tg.keyboard.KEY_ESCAPE:
				self.done = True
				break

			if self.next_pipe.x + self.next_pipe.width >= self.fg.width: # Draw the pipe if it is at the right margin of the screen. Otherwise it has been drawn already and is scrolling along (see scroll_left below)
				self.next_pipe.draw(self.fg, self.fgmask)
			else:
				for y in xrange(0, 33): # Othwewise draw a clear column on the right to clear scrolled off pipes which would wrap around to the right column
					self.fg[self.fg.width-1, y] = ' '
					self.fgmask[self.fgmask.width-1, y] = ' '

			self.screen.draw(0, 0, self.fg, ' ') # place the fg image on the screen as the next layer. Spaces ' ' are transpearant
			if self.next_pipe.age >= self.ARRIVAL_RATE*self.FPS: # Keep new pipes generated at the arrival rate
				self.next_pipe = Pipe(80, random.randint(2, 22), 8, 33)
				self.old_pipes.append(self.next_pipe) # store the next pipe in the set of old pipes unti it is scored


			self.faby.accelerate((0, self.GRAVITY)) # Apply acceleration due to gravity

			next_old_pipes = []
			for pipe in self.old_pipes:
				pipe.tick()
				if pipe.x < self.faby.x: # Score for a pipe when the bird passes it
					self.score += 1l
				else: # The scored pipe is implicitly lost, as we only read non-scored pipes here
					next_old_pipes.append(pipe)
			self.old_pipes = next_old_pipes

			self.faby.tick()
			self.faby.y = max(0, min(self.faby.y, self.fg.height-1)) # constrain the bird inside the screen
			collision = self.faby.collision(self.fgmask)
			if collision:
				cx, cy = collision
				self.faby.draw(self.screen)
				self.screen[cx,cy] = 'X'
				self.screen.show()
				tg.time.sleep(1)
				self.done = True

			self.faby.draw(self.screen)
			self.screen.write_text(5,1, "Score=%d"%self.score)
			metronome.wait_for_tick() # wait for a metronome tick to keep the pace of the game at one rate. This will keep pase even if we get key presses that exit keyboard.getch() early
			self.screen.show()

			self.fg.scroll_left()
			self.fgmask.scroll_left()


	def finalize(self):
		self.highscore.handle_new_score(self.score, self.screen)


def main():
	"""
	The main entrypoint to the Flappy Bird game. It initializes librarys including tinygame and creates the Game UI
	"""
	tg.initialize()
	try:
		gameui = FlappyUI()
		gameui.intro()
		gameui.play() # simply start playing

	finally:
		tg.quit()

if __name__ == "__main__":
	main()
