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
		self.scored = False

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

	def __init__(self, width, height, cheat=False):
		self.width = width
		self.height = height
		self.highscore = tg.HighScoresGUI(tg.HighScoresDB("examples/data/flappy/scores.txt")) # Load a GUI object for high scores with data from file
		self.screen = tg.character_display.CharacterDisplay(self.width, self.height)
		self.bg = tg.character_map.load("examples/data/flappy/bg.txt" )
		if random.randint(1, 10) < 4:
			self.bg.fill(' ')
			coords = []
			for x in xrange(0, self.bg.width):
				for y in xrange(0, self.bg.height-7):
					coords.append((x,y))
			random.shuffle(coords)
			for star in xrange(0, 30):
				self.bg[coords[star]] = '.'
			
		self.fg = tg.character_map.CharacterMap(self.width, self.height)
		self.fgmask = tg.character_display.CharacterMap(self.width, self.height)
		self.done = False
		self.exit = False
		self.cheat = cheat
		self.faby = Bird(23, 9)
		ground_tile = tg.character_map.parse('____\n/   ')
		ground_mask = tg.character_map.parse('####\n####')

		self.fg.fill('\x00')
		self.fgmask.fill(' ')
		for x in xrange(0, self.width, 4):
			self.fg.draw(x, self.height-ground_tile.height, ground_tile)
			self.fgmask.draw(x, self.height-ground_tile.height, ground_mask)
		self.next_pipe = Pipe(160, random.randint(2,self.height-14), 8, self.height-2)
		self.old_pipes = [self.next_pipe]
		self.score = 0

	def intro(self):
		title = tg.character_map.parse("""\
 ______________________________________________________
| ______ _                           ____  _         _ ||
||  ____| |                         |  _ \(_)       | |||
|| |__  | | __ _ _ __  _ __  _   _  | |_) |_ _ __ __| |||
||  __| | |/ _` | '_ \| '_ \| | | | |  _ <| | '__/ _` |||
|| |    | | (_| | |_) | |_) | |_| | | |_) | | | | (_| |||
||_|    |_|\__,_| .__/| .__/ \__, | |____/|_|_|  \__,_|||
|               | |   | |     __/ |                    ||
|               |_|   |_|    |___/                     ||
|                                                      ||
|                                        Presented in  ||
|                                            tinygame  ||
|                                                      ||
|                 Nick Miller 2014                     ||
|                                                      ||
|       Press any key to start.   ESC to quit          ||
|              Tap SPACE to flap wings                 ||
'______________________________________________________''
 ------------------------------------------------------'
""")
		tg.keyboard.getch(0)
		metronome = tg.Metronome(1/self.FPS) # Use a metronome to maintain specified fps
		d = 0
		while True:
			k = tg.keyboard.getch(1/self.FPS)
			if k == tg.keyboard.KEY_ESCAPE:
				self.done = True
				self.exit = True
			if k: break
			self.screen.draw(0, 0, self.bg) # draw the background first -- the first layer

			self.screen.draw(0, 0, self.fg, '\x00') # place the fg image on the screen as the next layer. Spaces ' ' are transpearant
			self.faby.tick()
			self.faby.y = max(0, min(self.faby.y, self.height-1)) # constrain the bird inside the screen

			self.screen.draw(self.width/2-title.width/2, 0, title)
			self.faby.draw(self.screen)

			metronome.wait_for_tick() # wait for a metronome tick to keep the pace of the game at one rate. This will keep pase even if we get key presses that exit keyboard.getch() early
			self.screen.show()

			self.fg.scroll_left()
			self.fgmask.scroll_left()
			d += 1
			if (d >= 4*self.FPS):
				self.highscore.scroll_on(self.screen)
				d = 0
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
				self.exit = True
				break

			if self.next_pipe.x + self.next_pipe.width >= self.fg.width: # Draw the pipe if it is at the right margin of the screen. Otherwise it has been drawn already and is scrolling along (see scroll_left below)
				self.next_pipe.draw(self.fg, self.fgmask)
			else:
				for y in xrange(0, self.fg.height-2): # Othwewise draw a clear column on the right to clear scrolled off pipes which would wrap around to the right column
					self.fg[self.fg.width-1, y] = '\x00'
					self.fgmask[self.fgmask.width-1, y] = ' '

			self.screen.draw(0, 0, self.bg) # draw the background first -- the first layer

			self.screen.draw(0, 0, self.fg, '\x00') # place the fg image on the screen as the next layer. Spaces ' ' are transpearant
			if self.next_pipe.age >= self.ARRIVAL_RATE*self.FPS: # Keep new pipes generated at the arrival rate
				self.next_pipe = Pipe(self.width, random.randint(2, self.height-13), 8, self.height-2)
				self.old_pipes.append(self.next_pipe) # store the next pipe in the set of old pipes unti it is scored


			self.faby.accelerate((0, self.GRAVITY)) # Apply acceleration due to gravity

			for pipe in self.old_pipes:
				pipe.tick()
				if pipe.x < self.faby.x: # Score for a pipe when the bird passes it
					self.score += 1
					pipe.scored = True
			self.old_pipes = [pipe for pipe in self.old_pipes if not pipe.scored]

			self.faby.tick()
			self.faby.y = max(0, min(self.faby.y, self.height-1)) # constrain the bird inside the screen
			self.screen.write_text(5,1, "Score: %d"%(self.score))

			collision = self.faby.collision(self.fgmask)
			if collision:
				cx, cy = collision
				self.faby.draw(self.screen)
				self.screen[cx,cy] = 'X'
				self.screen.show()
				tg.time.sleep(1 if not self.cheat else .25)
				if not self.cheat:
					self.done = True

			self.faby.draw(self.screen)
			metronome.wait_for_tick() # wait for a metronome tick to keep the pace of the game at one rate. This will keep pase even if we get key presses that exit keyboard.getch() early
			self.screen.show()

			self.fg.scroll_left()
			self.fgmask.scroll_left()

		self.highscore.handle_new_score(self.score, self.screen)

	def finalize(self):
		self.highscore.handle_new_score(self.score, self.screen)


def main():
	"""
	The main entrypoint to the Flappy Bird game. It initializes librarys including tinygame and creates the Game UI
	"""
	tg.initialize()
	try:
		while True:
			gameui = FlappyUI(80, 23, len(sys.argv) == 2 and sys.argv[1] == '--cheat')
			gameui.intro()
			gameui.play() # simply start playing
			if gameui.exit: break

	finally:
		tg.quit()

if __name__ == "__main__":
	main()
