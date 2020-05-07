import sys
import random
sys.path.extend(['.', '..'])
import tinygame as tg

class Pipe():
	"""
	Class to represent the pipes which come at the player.
	They are regularly created at a position on the right of the screen and scrolled leftward.
	They may draw themselves on a buffer, as well as draw their solid cells on a collision mask.
	"""
	HEAD = tg.character_map.parse(	".======." + "\n" + 
	                                "||     |" + "\n" +
	                                " ====== " )
	BODY = tg.character_map.parse(  " ||   | " )

	HEAD_MASK = tg.character_map.parse( 	" ###### " + "\n" + # A map of cells for collision detection with a pipe
	                                        "########" + "\n" + # Blank is empty and '#' are on and may collide
                                                " ###### " )
	BODY_MASK = tg.character_map.parse(	" ###### " )

	def __init__(self, x, gap_y, gap_height, height):
		"""
		Constructor for a pipe at position x (usually right side of the screen) with a 
		gap at gap_y, and a given total height (usually the height of the screen)

		x: position coordinate (usually right side of the screen)
		gap_y: position coordinate of the start of the gap
		gap_height: the size of the gap in the pipes. Hopefully enough for the bird to fly through
		height: the total length of the pipe  (usually the whole height of the screen)
		"""
		self.x = x # Start at the given x position on the screen
		self.width = Pipe.HEAD.width # width is given by the appearance sprite
		self.gap_y, self.gap_height, self.height = gap_y, gap_height, height # the pipe extends a height, has a gap, and then to the bottom of the screen
		self.age = 0 # track the age of the pipe so it dies and is scored when the bird passes (its appearance continues to be scrolled off to the left until it leaves)
		self.scored = False # It is on the right of the screen and has not been scored

	def draw(self, character_map, solid_mask_map):
		"""
		Draws this pipe on the given CharacterMap.
		Pipes are only drawn at the very right hand side of the buffer. 
		The buffer continues to scroll so the pipe travels toward the left of the screen

		character_map: A CharacterMap buffer to draw the appearance of the pipe
		solid_mask_map: An identical size CharacterMap containing collision information. Draw the pipe's mask on for collision detection
		"""
		for y in range(0, self.height): # Draw all the way down the pipe
			if self.gap_y < y and y <= self.gap_y + self.gap_height: continue # No need to draw anything between the vertical gaps
			character_map.draw_image(self.x, y, Pipe.BODY) # Draw a body segment at each point
			solid_mask_map.draw_image(self.x, y, Pipe.BODY_MASK) # Same on the mask

		character_map.draw_image(self.x, self.gap_y - Pipe.HEAD.height+1, Pipe.HEAD) # Draw the upper pipe head
		character_map.draw_image(self.x, self.gap_y + self.gap_height, Pipe.HEAD) # Draw the lower pipe head

		solid_mask_map.draw_image(self.x, self.gap_y - Pipe.HEAD.height+1, Pipe.HEAD_MASK) # Draw the heads on the collision mask too
		solid_mask_map.draw_image(self.x, self.gap_y + self.gap_height, Pipe.HEAD_MASK)

	def tick(self):
		"""
		Call for every frame of a pipe. Moves it leftward and ages the pipe
		"""
		self.x -= 1 # Move left one unit every frame
		if self.x < 80: self.age += 1 # Increase our age while we are on screen

class Bird():
	"""
	A class representing the user as a Bird. It follows physical laws of acceleration.
	The user may flap the wings and impart an impulse upward to keep it up in the air.
	"""
	FLAP_IMPULSE = -1.0 # The velocity of the bird when a flap impulse is imparted. Negative for up
	SPRITE0 = tg.character_map.parse("_/0=" + "\n"
                                       "\\v/ ")
	SPRITE1 = tg.character_map.parse("_/0=" + "\n"
                                        "\-/ ")
	SPRITE2 = tg.character_map.parse("_/0=" + "\n"
                                        "\^/ ")

	def __init__(self, x, y):
		"""
		Constructs a Bird at a given position

		x: x position of the Bird on the screen. The x position does not actually ever change, but the world scrolls by
		y: y position of the Bird on the screen
		"""
		self.x, self.y = x,y # Set the desited position
		self.dy = 0 # The derivitive of the y position (velocity). Note dx is always 0. See self.x
		self.animation = [self.SPRITE0, self.SPRITE1, self.SPRITE2, self.SPRITE1] # Stick the appearances togther in a list for an animation
		self.age = 0 # Track the age of the Bird in frames

	def animated_current_sprite(self):
		"""
		Get the current sprite (CharacterMap) to draw for animating the Bird

		return: CharacterMap you may use to draw the animated Bird
		"""
		return self.animation[self.age//2 % len(self.animation)] # The animation moves along with age. The image changes every 2 frames. Mod operator % loops the animation

	def draw(self, character_map):
		"""
		Draws the animated Bird on the given CharacterMap

		character_map: A CharacterMap on which to draw the current animation image of the Bird	
		"""
		character_map.draw_image(int(self.x), int(self.y), self.animated_current_sprite(), ' ') # Draw the current Bird animation image at the current position

	def flap(self):
		"""
		Flaps the Bird's wings and imparts an upward velocity
		"""
		self.dy = Bird.FLAP_IMPULSE # Set the velocity using the impulse
		self.age = 0 # Reset the animation age to zero, so the wings appear down on every flap

	def apply_force(self, Fx_Fy):
		"""
		Applies the given force to accelerate the Bird. In particular the force of gravity can accelerate it downward.
		Note the flapping the wings imparts an impulse. See Bitd.flap(...)

		Fx_Fy: a pair. The x, and y component of the force. Note x is usually 0 since the Bird should maintain a fixed x position as the world scrolls by
		"""
		Fx, Fy = Fx_Fy
		self.dy += Fy # Change the velocity by acceleration. Note assume mass m = 1. F = ma. So a = F/m = F

	def tick(self):
		"""
		Call every frame to advance the state of the Bird
		"""
		self.y += self.dy # Go one step according to velocity
		self.age += 1 # Advance age one step for animation

	def collision(self, character_map):
		"""
		Determines if the Bird would collide with any of the non-blank characters on the given CharacterMap.
		In particular, the character_map should be a collision mask with pipes and ground drawn on.

		character_map: A CharacterMap with objects drawn on it to check collision on. Should be just a collision mask with on cells and blank where there is nothing
		"""
		sprite = self.animated_current_sprite() # Determine the sprite to be drawn next
		for y in range(0, sprite.height): # Go through each cell in the sprite
			for x in range(sprite.width-1,0,-1): # Go throgh from right to left since we want to find the rightmost collision as the Bird travels rightward
				if sprite[x,y] != ' ' and character_map[int(self.x)+x,int(self.y)+y] != ' ': # If it is non-blank on the collision mask we have a collision
					return int(self.x)+x,int(self.y)+y # return the point of collision
		return None # Return None for no collision
			
class FlappyUI():
	"""
	A User Interface class to handle all the game logic and rendering of the game Flappy Bird
	"""

	GRAVITY = 0.08 # Rate of downward acceleration due to gravity
	FPS = 24.0 # Frame rate in frames per second
	ARRIVAL_RATE = 1.8 # The time (in seconds) between each pipe that arrives on the right of the screen

	def __init__(self, width, height, cheat=False):
		"""
		Constructor for a FlappyUI with a given screen width and height

		width: UI width
		height: UI height
		cheat: A boolean defaulting to False. If cheating is on, the game doesn't end when Faby hits a pipe
		"""
		self.width = width # Set the width and height
		self.height = height
		self.highscore = tg.HighScoresGUI(tg.HighScoresDB("examples/data/flappy/scores.txt")) # Load a GUI object for high scores with data from file
		self.screen = tg.character_display.CharacterDisplay(self.width, self.height) # Create a character display screen
		self.bg = tg.character_map.load("examples/data/flappy/bg.txt" ) # Loads the beautiful hills in the background previously drawn. See file
		if random.randint(1, 10) < 4: # 40% of the time, randomly, we change the background to nighttime stars
			self.bg.fill(' ') # Start with a black night background
			coords = [] # Fill in all the possible coordinates for stars
			for x in range(0, self.bg.width):
				for y in range(0, self.bg.height-7): # Stars can reach all the way down to height-7
					coords.append((x,y))
			random.shuffle(coords) # Randomize coordinates for random stars
			for star in range(0, 30): # Place 30 stars at the coordinates
				self.bg[coords[star]] = '.'
			
		self.fg = tg.character_map.CharacterMap(self.width, self.height) # Create CharacterMap to draw foreground objects (ground and pipe)
		self.fg_collision_mask = tg.character_display.CharacterMap(self.width, self.height) # Create a corresponding collision map to detect collisions with foreground objects
		self.done = False # Not done
		self.exit = False # Not ready to exit the program
		self.cheat = cheat # Set the desired cheat flag
		self.faby = Bird(23, 9) # The Bird is named Faby
		ground_tile = tg.character_map.parse('____\n/   ') # A repeated ground segment
		ground_mask = tg.character_map.parse('####\n####') # It is solid in the collision mask

		self.fg.fill('\x00') # Fill the foreground with '\x00' which we will use as the transparent characters. This will show the background behind
		self.fg_collision_mask.fill(' ')  # Empty collision mask
		for x in range(0, self.width, ground_tile.width): # Repeatedly draw the piece of ground pattern to fill the whole screen
			self.fg.draw_image(x, self.height-ground_tile.height, ground_tile) 
			self.fg_collision_mask.draw_image(x, self.height-ground_tile.height, ground_mask) # Also fill in the ground on the collision mask
		self.next_pipe = Pipe(self.width + 80, random.randint(2,self.height-14), 8, self.height-2) # The first pipe is very far away to give the user time
		self.old_pipes = [self.next_pipe] # old_pipes is all existing pipes that have yet to be scored
		self.score = 0

	def intro(self):
		"""
		Shows the intro title, with animated Bird and ground and waits for a key press
		"""
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
		tg.keyboard.getch(0) # Clear key presses
		metronome = tg.Metronome(1/self.FPS) # Use a metronome to maintain specified fps
		idle = 0 # Track idle time to show high scores
		while True: # Show the title until a kep press
			k = tg.keyboard.getch() # Read the key press
			if k == tg.keyboard.KEY_ESCAPE: # ESCAPE is special. Stop the title, but also exit the program
				self.done = True
				self.exit = True # make sure to exit
			if k: break # Until a key is press
			self.screen.draw_image(0, 0, self.bg) # draw the background first -- the first layer

			self.screen.draw_image(0, 0, self.fg, '\x00') # place the fg image on the screen as the next layer. Zeros '\x00' are transpearant
			self.faby.tick() # Keep the Bird ticking for animation

			self.screen.draw_image(self.width//2-title.width//2, 0, title) # Draw the title card
			self.faby.draw(self.screen) # Draw the animated Bird in front

			metronome.wait_for_tick() # wait for a metronome tick to keep the pace of the game at one rate. This will keep pase with FPS
			self.screen.show() # Update the newest image on screen

			self.fg.scroll_left() # Keep the ground scrolling
			self.fg_collision_mask.scroll_left() # Scroll the collision mask along side it and keep in sync
			idle += 1 # Track the idle time
			if (idle >= 4*self.FPS): # If idle for 4 seconds
				self.highscore.scroll_on(self.screen) # Show high scores
				idle = 0
	def play(self):
		"""
		The UI plays a round of Flappy Bird until the user hits something 
		"""
		metronome = tg.Metronome(1/self.FPS) # Use a metronome to maintain specified fps

		while not self.done:
			k = tg.keyboard.getch() # Read key presses
			if k == ' ':
				self.faby.flap() # Use the space key to flap the bird wings
			if k == tg.keyboard.KEY_ESCAPE:
				self.done = True
				self.exit = True
				break

			if self.next_pipe.x + self.next_pipe.width >= self.fg.width: # Draw the pipe if it is exactly at the right margin of the screen. Otherwise it has been drawn already and is scrolling along (see scroll_left below)
				self.next_pipe.draw(self.fg, self.fg_collision_mask)
			else:
				for y in range(0, self.fg.height-2): # Draw a blank column on the right to clear scrolled off pipes which have just wrapped around
					self.fg[self.fg.width-1, y] = '\x00'
					self.fg_collision_mask[self.fg_collision_mask.width-1, y] = ' '

			self.screen.draw_image(0, 0, self.bg) # draw the background first -- the first layer

			self.screen.draw_image(0, 0, self.fg, '\x00') # place the fg image on the screen as the next layer. Spaces ' ' are transpearant
			if self.next_pipe.age >= self.ARRIVAL_RATE*self.FPS: # Keep new pipes generated at the arrival rate
				self.next_pipe = Pipe(self.width, random.randint(2, self.height-13), 8, self.height-2)
				self.old_pipes.append(self.next_pipe) # store the next pipe in the set of old pipes unti it is scored


			self.faby.apply_force((0, self.GRAVITY)) # Apply acceleration due to gravity

			for pipe in self.old_pipes: # Go through all existing pipes
				pipe.tick() # Tick every pipe to keep it moving
				if pipe.x < self.faby.x: # Score for a pipe when the bird passes it
					self.score += 1
					pipe.scored = True
			self.old_pipes = [pipe for pipe in self.old_pipes if not pipe.scored] # Delete pipes that have been scored. Their appearance continues to scroll off to the left in the scrolling self.fg CharacterMap

			self.faby.tick() # Tick faby so he keeps animating
			self.faby.y = max(0, min(self.faby.y, self.height-1)) # constrain the bird inside the screen
			self.screen.write_text(5,1, "Score: %d"%(self.score)) # Present the score to the user

			collision = self.faby.collision(self.fg_collision_mask) # See if the Bird collids with foreground using our collision mask
			if collision: # If a collision is returned
				cx, cy = collision
				self.faby.draw(self.screen) # Draw the Bird with an X on it at the collision point
				self.screen[cx,cy] = 'X'
				self.screen.show() # Show the collision to the user
				tg.time.sleep(1 if not self.cheat else .25) # Delay for a bit so the user sees it
				if not self.cheat: # If you are not cheating
					self.done = True # Then the game if over

			self.faby.draw(self.screen) # Draw the animated Bird on screen  buffer
			metronome.wait_for_tick() # wait for a metronome tick to keep the pace of the game at one rate. This will keep pase at FPS
			self.screen.show() # Update the display with the newest frame

			self.fg.scroll_left() # Keep the foreground scrolling leftward
			self.fg_collision_mask.scroll_left() # Scroll the foreground in lock step

		self.highscore.handle_new_score(self.score, self.screen) # As the game is over, record a high score if necessary

def main():
	"""
	The main entrypoint to the Flappy Bird game. It initializes librarys including tinygame and creates the Game UI
	"""
	tg.initialize()
	try:
		while True:
			gameui = FlappyUI(80, 23, len(sys.argv) == 2 and sys.argv[1] == '--cheat')
			gameui.intro() # Show the title
			gameui.play() # simply start playing
			if gameui.exit: break # Keep playing till the user wants to exit
	finally:
		tg.quit()

if __name__ == "__main__":
	main()
