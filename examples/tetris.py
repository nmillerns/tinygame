"""
Tetris
"""
import sys
import random # use this module to get random next blocks
import copy # use this module to make copies of the canonical Tetrominos
sys.path.append('.')
import tinygame as tg

class Tetromino():
	"""
	Class representing the Tetromino, the basic unit of Tetris. See http://en.wikipedia.org/wiki/Tetromino
	"""
	ADVANCE_SPEED = 0.25
	ALL = [] # All canonical Tetrominos. Populated below

	def __init__(self, x, y, appearance_string):
		"""
		Constructs a Tetromino from a character map like string describing its appearance. eg "[][][][]"
		It starts at location x,y. We get the appearance and pre-calculate all 4 rotated appearance to speed up rotating at run time
		Tetrominos can be translated (left or right) or rotat_cw or rotate_ccw (rotated clocl wise or counter clock wise).
		You can also undo the most recent action on it.
		"""
		self.x, self.y = x, y # set location of the center
		appearance0 = tg.character_map.parse(appearance_string) # make a character map of the appearance
		appearance90 = rotated(appearance0) # use the special rotation function (see below) to get 90 degree rotated appearance
		appearance180 = rotated(appearance90)
		appearance270 = rotated(appearance180)
		self.appearances = [appearance0, appearance90, appearance180, appearance270] # store all 4 of the pre-calculated rotations in a list
		self.angle_index = 0 # simply track the angle in increments of 90 degrees
		self.undo = self.do_nothing # start our undo action as nothing. It points to a function to call to undo the last action

	def do_nothing(self):
		pass # does nothing

	def appearance(self):
		return self.appearances[self.angle_index] # use the pre-rotated list to get the Tetromino's appearance

	def draw(self, character_map):
		"""
		Draws the Tetromino on the given CharacterMap. The ' ' blanks are drawn transparent
		"""
		x,y, w, h = self.bounding_box() # find the bounding box
		character_map.draw(x, y, self.appearance(), ' ') # draw from the bounding box (as related to the x,y location of the center)

	def bounding_box(self):
		# the box around this Tetromino is starts half width back and half height back from the center.
		x0, y0 = 2*int(self.x - self.appearance().width/2) + 1, int(self.y - self.appearance().height/2) # use 2*x + 1 because the character map has a grid 2 characters wide, and a border of 1
		return (x0, y0, x0 + self.appearance().width, y0 + self.appearance().height)
	
	def fits_in(self, character_map):
		"""
		Check of the given Tetromino fits inside the given character map if it were draw there using its current bounding box
		"""
		x0, y0, x1, y1 = self.bounding_box()
		for yi in xrange(y0, y1): # check all points inside the bounding box
			for xi in xrange(x0, x1, 2):
				if self.appearance()[xi-x0, yi-y0] != ' ' and character_map[xi+1, yi] != '.': return False # if it is not a transparent character but the map does not have a grid point there, then we don't fit
		return True # no points have collided so we fit

	def rotate_ccw(self):
		self.angle_index = (self.angle_index + 1) % 4 # rotates the Tetromino counter clockwise simply by changing the pre rotated index
		self.undo = self.rotate_cw # to undo this rotate it back clockwise

	def rotate_cw(self):
		self.angle_index = (self.angle_index - 1) % 4 # rotates the Tetromino clockwise simply by changing the pre rotated index
		self.undo = self.rotate_ccw # to undo this rotate it back counter clockwise

	def translate_left(self):
		self.x -= 1 # shifts the Tetromino one unit left
		self.undo = self.translate_right # to undo this shift it back right

	def translate_right(self):
		self.x += 1 # shifts the Tetromino one unit right
		self.undo = self.translate_left # to undo this shift it back left

	def advance(self):
		self.y += Tetromino.ADVANCE_SPEED  # advances the Tetromino down at the current speed
		self.undo = self.retreat # the opposite is to retreat back up

	def retreat(self):
		self.y -= Tetromino.ADVANCE_SPEED # moves the Tetromino back up at the current speed
		self.undo = self.advance # the opposite is to continue back down

def rotated(appearance):
	"""
	Calculates and returns the character map of a the given block if it is rotated 90 degrees ccw.
	This is a little tricky since the blocks have t characters for every square. ie "[]"
	"""
	r = tg.character_map.CharacterMap(2*appearance.height, appearance.width/2) # the rotated one exchanges height and width stretching appropriately for 2 characters for every square
	for i in xrange(0, appearance.height): # go through rows
		for j in xrange(0, appearance.width/2): # go through columns
			if appearance[2*j, i] != ' ': # only set a new rotated block if there was a block at this row and column
				r[2*i, r.height - 1 - j] = '[' # use rotation matrix  [0 1; -1 0] ie col i row j to col -j row i
				r[2*i + 1, r.height - 1 - j] = ']'
	return r

# Construct this canonical instance of a tetromino and store it in the Tetromino class labelled I
Tetromino.I = Tetromino(7, 2, "        " + "\n" +\
                              "[][][][]" + "\n" +\
                              "        ")
# Construct this canonical instance of a tetromino and store it in the Tetromino class labelled O
Tetromino.O = Tetromino(7, 2, "[][]" + "\n" +\
                              "[][]")
# Construct this canonical instance of a tetromino and store it in the Tetromino class labelled T
Tetromino.T = Tetromino(7, 2, "      " + "\n" +\
                              "[][][]" + "\n" +\
                              "  []  ")
# Construct this canonical instance of a tetromino and store it in the Tetromino class labelled J
Tetromino.J = Tetromino(7, 2, "      " + "\n" +\
                              "[][][]" + "\n" +\
                              "    []")
# Construct this canonical instance of a tetromino and store it in the Tetromino class labelled L
Tetromino.L = Tetromino(7, 2, "      " + "\n" +\

                              "[][][]" + "\n" +\
                              "[]    ")
# Construct this canonical instance of a tetromino and store it in the Tetromino class labelled S
Tetromino.S = Tetromino(7, 2, "  [][]" + "\n" +\
                              "[][]  " + "\n" +\
                              "      ")
# Construct this canonical instance of a tetromino and store it in the Tetromino class labelled Z
Tetromino.Z = Tetromino(7, 2, "[][]  " + "\n" +\
                              "  [][]" + "\n" +\
                              "      " )
# Put all the canonical Tetrominos in the ALL list
Tetromino.ALL = [Tetromino.I, Tetromino.O, Tetromino.T, Tetromino.J, Tetromino.L, Tetromino.S, Tetromino.Z]

def random_tetromino():
	"""
	Creates a new random Tetromino
	"""
	return copy.copy(Tetromino.ALL[random.randint(0, len(Tetromino.ALL)-1)])

class TetrisGameUI():
	# Just fill our the game screen background manually in a string to easily load and draw it as a character map
	BACKGROUND_STRING = """
| . . . . . . . . . .| Score:
| . . . . . . . . . .|
| . . . . . . . . . .|
| . . . . . . . . . .| 
| . . . . . . . . . .| Level:
| . . . . . . . . . .|   
| . . . . . . . . . .|
| . . . . . . . . . .| 
| . . . . . . . . . .| Lines:
| . . . . . . . . . .|
| . . . . . . . . . .|
| . . . . . . . . . .|
| . . . . . . . . . .|
| . . . . . . . . . .|
| . . . . . . . . . .|
| . . . . . . . . . .| Next:   
| . . . . . . . . . .|
| . . . . . . . . . .|
| . . . . . . . . . .|
| . . . . . . . . . .|
 ==================== 
"""

	def __init__(self):
		self.screen = tg.character_display.CharacterDisplay(48, 24) # the game UI creates a 32 x 24 character screen to draw the game upon
		self.score = 0 # the game UI tracks the score
		self.lines = 0 # the game UI tracks number of completed lines
		self.level = 0 # the game UI the player level
		self.highscore = tg.HighScoresGUI(tg.HighScoresDB("examples/data/tetris/scores.txt"))

	def intro(self):
		try:
			title_card = """
[][][][][][][][][][][][][][][][][][][][][][][][]
[]                                            []
[]_____  ______  ______  ______   __   ______ []   
/\__  _\/\  ___\/\__  _\/\  == \ /\ \ /\  ___\[]   
\/_/\ \/\ \  ___\/_/\ \/\ \  __<_\ \ \. \___  \]  
[] \ \_\ \ \_____\ \ \_\ \ \_\_\_\. \_\./\_____\ 
[]  \/_/  \/_____/  \/_/  \/_/ /_/ \/_/ \/_____/ 
[]                                            []
[]                                            []
[]                                            []
[]                                            []
[]                                            [] 
[]                                            []
[]                                            []
[]                                            []
[]                                            []
[]                  Presented in              []
[]                      tinygame              []
[]                                            []
[]              Nick Miller 2013              []
[][][][][][][][][][][][][][][][][][][][][][][][]
"""
			while True:
				ch = tg.keyboard.getch(0)
				cm = tg.character_map.parse(title_card)
				self.screen.fill(' ')
				self.screen.draw(0, 0, cm)
				self.screen.show()
				if tg.keyboard.getch(3) != None: return
				self.highscore.scroll_on(self.screen)
		finally:
			self.screen.fill(' ')

	def show_gameover(self):
		"""
		The UI shows game over screen for 2.5 seconds
		"""
		self.screen.fill(' ')
		self.screen.write_text(10, 5, "Game Over!") # write Game Over!
		self.screen.show() # make sure to .show() so its visible on the console
		tg.time.sleep(1.5) # sleep with no key presses
		tg.keyboard.getch(1.0) # wait for a key press for the last second. Also clears the keypresses for the next screen
		
	def get_rows_score(self, number_of_rows):
		"""
		Calculates the score for a given number of rows completed. See http://tetris.wikia.com/wiki/Scoring
		"""
		ROW_SCORES = {0:0, 1:40, 2:100, 3:300} # Use a dictionary to look up the score
		if number_of_rows in ROW_SCORES.keys():
			return ROW_SCORES[number_of_rows] 
		return 1200 # All other higher scores truncate at 1200

	def play(self):
		"""
		Plays the game of Tetris
		"""
		bg = tg.character_map.parse(TetrisGameUI.BACKGROUND_STRING) # load the background from the string into the bg CharacterMap

		t = None # There is no current Tetromino it will be generated
		next = random_tetromino() # decide the next Tetromino

		while True: # Play forever until the game is over
			if t == None: # check if there is no current Tetromino
				t = next # if so use the Tetromino up next
				next = random_tetromino() # now redecide what is next after that
				if not t.fits_in(bg): # check if the new Tetromino at the top fits in the screen
					t.draw(self.screen) # if not we dont have any more room and the game is over
					self.screen.show() # show the user the problem
					tg.time.sleep(.5)
					tg.keyboard.getch(.5)
					self.show_gameover() # show the user game over
					break # leave

			k = tg.keyboard.getch(1/10.0) # get the keypress and change the Tetromino accordingly. Wait 1/10 of a second so the game progresses if no key is pressed
			if k == tg.keyboard.KEY_LEFT:
				t.translate_left()
			elif k == tg.keyboard.KEY_RIGHT:
				t.translate_right()
			elif k == tg.keyboard.KEY_UP or k == 'x':
				t.rotate_ccw()
			elif k == 'z':
				t.rotate_cw()
			elif k == tg.keyboard.KEY_DOWN:
				t.advance()
			elif k == tg.keyboard.KEY_ESCAPE:
				break

			if not t.fits_in(bg): # check if the move we did on the Tetromino allows it to fit
				t.undo() # if not undo the move

			t.advance() # The current Tetromino always advances down once per frame
			if not t.fits_in(bg): # check if it fits after moving down
				t.undo() # if not it must have gone through the floor. So it is done moving
				t.draw(bg) # commit the current Tetromino to the background
				self.score += int(round(t.y/2.0)) # score the Tetromino
				t = None # No more Tetromino. We will move on to the next Tetromino

			self.screen.draw(0, 0, bg) # Refresh the screen using background
			if t: t.draw(self.screen) # Draw the current Tetromino on the screen (note: not on the backgond)

			self.screen.draw(23, 18, next.appearance()) # preview the next Tetromino at the side at 23,10
			self.screen.write_text(24,2, str(self.score)) # Write stats on the side of the screen
			self.screen.write_text(25,6, str(self.level))
			self.screen.write_text(25,10, str(self.lines))
			self.screen.show() # show the updated screen to the user once per frame -- now

			# now that we have handled the current Tetromino, we do the check for completed rows (lines) in the commited background
			number_completed_rows = 0 # count the complete rows this turn
			for y in xrange(1, bg.height-1): # run through all rows
				complete = True # assume it is complete and check otherwise
				for x in range(2, 22, 2): # go through the row
					if bg[x, y] == '.': # check to see if we see through to the grid
						complete = False # if so this can not be a complete row
						break
				if complete: # was it a complete row indeed?
					number_completed_rows += 1 # if so increment the complete rows
					self.screen.write_text(1, y, "********************") # draw a little piece of animation on screen of the row collapsing
					for z in xrange(y, 2, -1): # go back up the rows above in the background and shift everything down one
						for x in range(1, 22-1):
							bg[x, z] = bg[x, z-1] # shifted down (z->z-1)
					bg.write_text(1, 1, " . . . . . . . . . .") # since everything is shifted down we push in an empty row at the top

			if number_completed_rows > 0:
				self.score += self.get_rows_score(number_completed_rows) # score the completed rows
				self.lines += number_completed_rows # track number of lines
				self.screen.show() # show the animation for row completion on screen and pause for effect
				tg.time.sleep(.4)

		self.highscore.handle_new_score(self.score, self.screen)
def main():
	"""
	The main entrypoint to the Tetris game. It initializes librarys including tinygame and creates the Game UI
	"""
	tg.initialize()
	try:
		gameui = TetrisGameUI()
		gameui.intro()
		gameui.play() # simply start playing

	finally:
		tg.quit()

if __name__ == "__main__":
	main()
