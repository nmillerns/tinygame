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
	A User Interface class to handle all the game logic and rendering of the 2048
	"""
	def __init__(self):
		self.screen = tg.character_display.CharacterDisplay(80, 23) # the game UI creates a 80 x 24 character screen to draw the game upon
		self.grid = tg.character_map.CharacterMap(4,4)
		self.grid.fill(' ')
		self.prev = self.grid.clone()
		self.done = False
		self.delay = 1/8.0
		self.score = 0
		self.won = False
		self.highscore = tg.HighScoresGUI(tg.HighScoresDB("examples/data/2048/scores.txt"))
		self.coords = []
		for x in xrange(0, 4):
			for y in xrange(0, 4):
				self.coords.append((x,y))
				self.grid[x,y] = ' '
		self.insert_random()
		self.insert_random()

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
		self.render_grid()
		self.screen.write_text(6, 13, "Game Over!") # write Game Over!
		self.screen.show() # make sure to .show() so its visible on the console
		tg.time.sleep(1.5) # sleep with no key presses
		tg.keyboard.getch(10.0) # wait for a key press for the last second. Also clears the keypresses for the next screen
		
	def score_tile(self, tile):
		self.score += 2**(ord(tile)+1+1) # score the power of two just achived... +1 for 0 offeset

	def slide_up(self):
		for x in xrange(0, 4):
			col = [self.grid[x, y] for y in xrange(0,4) if self.grid[x, y] != ' ' ]
			for y in xrange(0, 4):
				self.grid[x, y] = ' '
			for i in xrange(0, len(col)):
				self.grid[x, i] = col[i]
	def slide_down(self):
		for x in xrange(0, 4):
			col = [self.grid[x, y] for y in xrange(0,4) if self.grid[x, y] != ' ' ]
			for y in xrange(0, 4):
				self.grid[x, y] = ' '
			for i in xrange(0, len(col)):
				self.grid[x, 4-len(col)+i] = col[i]

	def combine_down(self):
		for x in xrange(0, 4):
			for y in xrange(2, -1, -1):
				me = self.grid[x,y]
				if me == ' ': continue
				below = self.grid[x, y+1]
				if me == below:
					self.grid[x, y + 1] = chr(ord(me) + 1)
					self.grid[x,y] = ' '
					self.score_tile(me)
	def combine_up(self):
		for x in xrange(0, 4):
			for y in xrange(1, 4):
				me = self.grid[x,y]
				if me == ' ': continue
				above = self.grid[x, y-1]
				if me == above:
					self.grid[x, y - 1] = chr(ord(me) + 1)
					self.grid[x,y] = ' '
					self.score_tile(me)

	def slide_left(self):
		for y in xrange(0, 4):
			row = [self.grid[x, y] for x in xrange(0,4) if self.grid[x, y] != ' ' ]
			for x in xrange(0, 4):
				self.grid[x, y] = ' '
			for i in xrange(0, len(row)):
				self.grid[i, y] = row[i]

	def slide_right(self):
		for y in xrange(0, 4):
			row = [self.grid[x, y] for x in xrange(0,4) if self.grid[x, y] != ' ' ]
			for x in xrange(0, 4):
				self.grid[x, y] = ' '
			for i in xrange(0, len(row)):
				self.grid[4-len(row)+i, y] = row[i]

	def combine_right(self):
		for y in xrange(0, 4):
			for x in xrange(2, -1, -1):
				me = self.grid[x,y]
				if me == ' ': continue
				right = self.grid[x+1, y]
				if me == right:
					self.grid[x + 1, y] = chr(ord(me) + 1)
					self.grid[x,y] = ' '
					self.score_tile(me)

	def combine_left(self):
		for y in xrange(0, 4):
			for x in xrange(1, 4):
				me = self.grid[x,y]
				if me == ' ': continue
				left = self.grid[x - 1, y]
				if me == left:
					self.grid[x - 1, y] = chr(ord(me) + 1)
					self.grid[x,y] = ' '
					self.score_tile(me)

	def insert_random(self):
		empty = [c for c in self.coords if self.grid[c] == ' ']
		random.shuffle(empty)
		rtype = random.randint(1,10) # pick a random new tile based on a random number from 1 to 10. 
		if empty != []: self.grid[empty[0]] = '\x01' if rtype == 1 else '\x00'  #random tile... 10% of the time use tile 4 otherwise use tile 2

	def move_exists(self):
		for x in xrange(0, 4):
			for y in xrange(0, 4):
				if self.grid[x,y] == ' ': return True
				if x < 4-1 and self.grid[x,y] == self.grid[x+1,y]: return True
				if y < 4-1 and self.grid[x,y] == self.grid[x,y+1]: return True
		return False

	def up(self):
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
		self.screen.fill(' ')

		for x in xrange(0, 4):
			for y in xrange(0, 4):
				b = self.grid[x, y]
				if b == ' ': continue
				if ord(b) >= 9: self.win = True
				Bxy = TILES[ord(b)]
				self.screen.draw(5*x, 2*y+2 , Bxy)
		self.screen.write_text(1, 0, "Score: %d"%self.score)
		self.screen.write_text(1, 1, "Best:  %d"%max(self.highscore.highscoresDB.best(), self.score))
		if self.won: self.screen.write_text(4, 12, "2048! You Win!")

	def play(self):
		"""
		The UI plays a round of 2048 game. 
		"""
		self.done = False

		while not self.done: # play forever until something happens
			for c in self.coords:
				if self.grid[c] != ' ' and ord(self.grid[c]) >= 10: self.won = True
			self.render_grid()
			self.screen.show()
			if not self.move_exists():
				self.show_gameover()
				self.done = True
				break

			self.prev.draw(0, 0, self.grid)

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
				break

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
