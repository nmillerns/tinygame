"""
2048
"""
import sys
import random
sys.path.extend(['.', '..'])
import tinygame as tg

TILES = [
    tg.character_map.parse(" ---- " + "\n"
                           "|  2 |" + "\n"
                           " ---- " + "\n"
                          ),
    tg.character_map.parse(" ---- " + "\n"
                           "|  4 |" + "\n"
                           " ---- " + "\n"
                          ),
    tg.character_map.parse(" ---- " + "\n"
                           "|  8 |" + "\n"
                           " ---- " + "\n"
                          ),
    tg.character_map.parse(" ---- " + "\n"
                           "| 16 |" + "\n"
                           " ---- " + "\n"
                         ),
    tg.character_map.parse(" ---- " + "\n"
                           "| 32 |" + "\n"
                           " ---- " + "\n"
                         ),
    tg.character_map.parse(" ---- " + "\n"
                           "| 64 |" + "\n"
                           " ---- " + "\n"
                         ),
    tg.character_map.parse(" ---- " + "\n"
                           "| 128|" + "\n"
                           " ---- " + "\n"
                        ),
    tg.character_map.parse(" ---- " + "\n"
                           "| 256|" + "\n"
                           " ---- " + "\n"
                        ),
    tg.character_map.parse(" ---- " + "\n"
                           "| 512|" + "\n"
                           " ---- " + "\n"
                        ),
    tg.character_map.parse(" ---- " + "\n"
                           "|1024|" + "\n"
                           " ---- " + "\n"
                       ),
    tg.character_map.parse(" ---- " + "\n"
                           "|2048|" + "\n"
                           " ---- " + "\n"
                       )
]

class TwentyFourtyEightGameUI():
	"""
	A User Interface class to handle all the game logic and rendering of the 2048 game
	"""
	def __init__(self):
		self.screen = tg.character_display.CharacterDisplay(80, 23) # the game UI creates a 80 x 24 character screen to draw the game upon
		self.grid = tg.character_map.CharacterMap(4,4) # A character map to store a representation of the internal 4x4 grid 
		self.grid.fill(' ') # clear the grid -- fill it with empty tiles
		self.prev = self.grid.clone() # have a previous copy of the grid to check for differences
		self.delay = 1/8.0 # A dilay pause time to time animations
		self.done = False
		self.score = 0
		self.win = False
		self.highscore = tg.HighScoresGUI(tg.HighScoresDB("examples/data/2048/scores.txt")) # Load a GUI object for high scores with data from file
		self.coords = [] # the set of all coordinates pointing into the internal 4x4 grid
		for x in xrange(0, self.grid.width):
			for y in xrange(0, self.grid.height):
				self.coords.append((x,y)) 

	def intro(self):
		try:
			title_card = """
  ---------------------------------------------------------------------------- 
  ----------------------------------------------------------------------------

 .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. |
| |    _____     | || |     ____     | || |   _    _     | || |     ____     | |
| |   / ___ `.   | || |   .'    '.   | || |  | |  | |    | || |   .' __ '.   | |
| |  |_/___) |   | || |  |  .--.  |  | || |  | |__| |_   | || |   | (__) |   | |
| |   .'____.'   | || |  | |    | |  | || |  |____   _|  | || |   .`____'.   | |
| |  / /____     | || |  |  `--'  |  | || |      _| |_   | || |  | (____) |  | |
| |  |_______|   | || |   '.____.'   | || |     |_____|  | || |  `.______.'  | |
| |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------' 

                                                      Presented in            
                                                          tinygame            
                                                                              
                             Nick Miller 2014                                 

  ---------------------------------------------------------------------------- 
  ----------------------------------------------------------------------------
"""
			while True:
				ch = tg.keyboard.getch(0)
				cm = tg.character_map.parse(title_card)
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
		self.render_grid()
		self.screen.write_text(6, 13, "Game Over!") # write Game Over!
		self.screen.show() # make sure to .show() so its visible on the console
		tg.time.sleep(1.5) # sleep with no key presses
		tg.keyboard.getch(10.0) # wait for a key press for the last second. Also clears the keypresses for the next screen
		
	def score_tile(self, tile):
		"""
		Scores a gicen tile according to this game's rules
		"""
		self.score += 2*2**(ord(tile)+1) # score the power of two just achived... +1 for 0 offeset

	def slide_up(self):
		for x in xrange(0, self.grid.width):
			col = [self.grid[x, y] for y in xrange(0,self.grid.height) if self.grid[x, y] != ' ' ]
			for y in xrange(0, self.grid.height):
				self.grid[x, y] = ' '
			for i in xrange(0, len(col)):
				self.grid[x, i] = col[i]
	def slide_down(self):
		for x in xrange(0, self.grid.width):
			col = [self.grid[x, y] for y in xrange(0,self.grid.height) if self.grid[x, y] != ' ' ]
			for y in xrange(0, self.grid.height):
				self.grid[x, y] = ' '
			for i in xrange(0, len(col)):
				self.grid[x, self.grid.height-len(col)+i] = col[i]

	def combine_down(self):
		for x in xrange(0, self.grid.width):
			for y in xrange(self.grid.height-1 -1, -1, -1):
				me = self.grid[x,y]
				if me == ' ': continue
				below = self.grid[x, y+1]
				if me == below:
					self.grid[x, y + 1] = chr(ord(me) + 1)
					self.grid[x,y] = ' '
					self.score_tile(me)
	def combine_up(self):
		for x in xrange(0, self.grid.width):
			for y in xrange(1, self.grid.height):
				me = self.grid[x,y]
				if me == ' ': continue
				above = self.grid[x, y-1]
				if me == above:
					self.grid[x, y - 1] = chr(ord(me) + 1)
					self.grid[x,y] = ' '
					self.score_tile(me)

	def slide_left(self):
		for y in xrange(0, self.grid.height):
			row = [self.grid[x, y] for x in xrange(0,self.grid.width) if self.grid[x, y] != ' ' ]
			for x in xrange(0, self.grid.width):
				self.grid[x, y] = ' '
			for i in xrange(0, len(row)):
				self.grid[i, y] = row[i]

	def slide_right(self):
		for y in xrange(0, self.grid.height):
			row = [self.grid[x, y] for x in xrange(0,self.grid.width) if self.grid[x, y] != ' ' ]
			for x in xrange(0, self.grid.width):
				self.grid[x, y] = ' '
			for i in xrange(0, len(row)):
				self.grid[self.grid.width-len(row)+i, y] = row[i]

	def combine_right(self):
		for y in xrange(0, self.grid.height):
			for x in xrange(self.grid.width-1 - 1, -1, -1):
				me = self.grid[x,y]
				if me == ' ': continue
				right = self.grid[x+1, y]
				if me == right:
					self.grid[x + 1, y] = chr(ord(me) + 1)
					self.grid[x,y] = ' '
					self.score_tile(me)

	def combine_left(self):
		for y in xrange(0, self.grid.height):
			for x in xrange(1, self.grid.width):
				me = self.grid[x,y]
				if me == ' ': continue
				left = self.grid[x - 1, y]
				if me == left:
					self.grid[x - 1, y] = chr(ord(me) + 1)
					self.grid[x,y] = ' '
					self.score_tile(me)

	def insert_random(self):
		"""
		Inserts a random tile onto a currently empty slace in this game's grid. No result if the grid is full
		The random tile is value 2 (i.e. '\x00') with probability 0.9 and value 4 (i.e. '\x01') with probability 0.1
		"""
		empty = [c for c in self.coords if self.grid[c] == ' '] # the set of all empty spaces remaining in the grid
		random.shuffle(empty) # shuffle them to chose a random empty space
		rtype = random.randint(1,10) # pick a random new tile based on a random number from 1 to 10. 
		if empty != []: self.grid[empty[0]] = '\x01' if rtype == 1 else '\x00'  #random tile... 10% of the time use tile 4 otherwise use tile 2

	def move_exists(self):
		"""
		Returns True iff a valid move exists on this game's grid which would change the grid.
		This is true when there is at least one empty tile which could be slid into. Otherwise there must be adjacent values to combine
		"""
		for x in xrange(0, self.grid.width):
			for y in xrange(0, self.grid.height):
				if self.grid[x,y] == ' ': return True # if there is an empty tile, sliding another aligned tile through that space is a valid move
				if x < self.grid.width-1 and self.grid[x,y] == self.grid[x+1,y]: return True # if we can check to the right, do so and see if there are adjacent tiles that could be combinded
				if y < self.grid.height-1 and self.grid[x,y] == self.grid[x,y+1]: return True # if we can check up one, do so and see if there are adjacent tiles that could be combinded
		return False

	def up(self):
		"""
		Applies an up grid slide and combines tiles upward
		"""
		self.slide_up()
		self.render_grid()
		self.screen.show()
		tg.time.sleep(self.delay)
		self.combine_up()
		self.render_grid()
		self.screen.show()
		tg.time.sleep(self.delay)
		self.slide_up()
		
	def down(self):
		"""
		Applies a down grid slide and combines tiles downward
		"""
		self.slide_down()
		self.render_grid()
		self.screen.show()
		tg.time.sleep(self.delay)
		self.combine_down()
		self.render_grid()
		self.screen.show()
		tg.time.sleep(self.delay)
		self.slide_down()

	def left(self):
		"""
		Applies a left grid slide and combines tiles left
		"""
		self.slide_left()
		self.render_grid()
		self.screen.show()
		tg.time.sleep(self.delay)
		self.combine_left()
		self.render_grid()
		self.screen.show()
		tg.time.sleep(self.delay)
		self.slide_left()

	def right(self):
		"""
		Applies a right grid slide and combines tiles right
		"""
		self.slide_right()
		self.render_grid()
		self.screen.show()
		tg.time.sleep(self.delay)
		self.combine_right()
		self.render_grid()
		self.screen.show()
		tg.time.sleep(self.delay)
		self.slide_right()

	def render_grid(self):
		"""
		Draws the tiles of the grid on this game UI screen
		"""
		self.screen.fill(' ') # clear out the screen
		for x in xrange(0, self.grid.width):
			for y in xrange(0, self.grid.height):
				b = self.grid[x, y]
				if b == ' ': continue
				if ord(b) >= 10: self.win = True
				self.screen.draw(5*x, 2*y+2 , TILES[ord(b)])
		self.screen.write_text(1, 0, "Score: %d"%self.score)
		self.screen.write_text(1, 1, "Best:  %d"%max(self.highscore.highscoresDB.best(), self.score))
		if self.win: self.screen.write_text(4, 12, "2048! You Win!")

	def play(self):
		"""
		The UI plays a round of 2048 game. 
		"""
		self.done = False
		for i in xrange(0, 2): self.insert_random() # start with 2 random tiles

		while not self.done: # play forever until something happens
			self.render_grid() # render the grid to the screeen
			self.screen.show() # show the screen to the user
			if not self.move_exists():
				self.show_gameover()
				break

			self.prev.draw(0, 0, self.grid) # copy the grid onto the previous for storage

			k = tg.keyboard.getch(10.0) # get the keypress and slide tiles accordingly.
			if k == tg.keyboard.KEY_UP:
				self.up()
			if k == tg.keyboard.KEY_DOWN:
				self.down()
			if k == tg.keyboard.KEY_LEFT:
				self.left()
			if k == tg.keyboard.KEY_RIGHT:
				self.right()
			if k == tg.keyboard.KEY_ESCAPE:
				self.done = True

			if self.grid != self.prev: self.insert_random()

		self.highscore.handle_new_score(self.score, self.screen)



def main():
	"""
	The main entrypoint to the Tetris game. It initializes librarys including tinygame and creates the Game UI
	"""
	tg.initialize()
	try:
		gameui = TwentyFourtyEightGameUI()
		gameui.intro()
		gameui.play() # simply start playing

	finally:
		tg.quit()

if __name__ == "__main__":
	main()
