"""
2048
"""
import sys
import random
sys.path.extend(['.', '..'])
import tinygame as tg

B2 = tg.character_map.parse(" ---- " + "\n"\
                            "|  2 |" + "\n"\
                            " ---- " + "\n"\
                           )
B4 = tg.character_map.parse(" ---- " + "\n"\
                            "|  4 |" + "\n"\
                            " ---- " + "\n"\
                           )
B8 = tg.character_map.parse(" ---- " + "\n"\
                            "|  8 |" + "\n"\
                            " ---- " + "\n"\
                           )
B16 = tg.character_map.parse(" ---- " + "\n"\
                             "| 16 |" + "\n"\
                             " ---- " + "\n"\
                           )
B32 = tg.character_map.parse(" ---- " + "\n"\
                             "| 32 |" + "\n"\
                             " ---- " + "\n"\
                           )
B64 = tg.character_map.parse(" ---- " + "\n"\
                             "| 64 |" + "\n"\
                             " ---- " + "\n"\
                           )
B128 = tg.character_map.parse(" ---- " + "\n"\
                              "| 128|" + "\n"\
                              " ---- " + "\n"\
                           )
B256 = tg.character_map.parse(" ---- " + "\n"\
                              "| 256|" + "\n"\
                              " ---- " + "\n"\
                           )
B512 = tg.character_map.parse(" ---- " + "\n"\
                              "| 512|" + "\n"\
                              " ---- " + "\n"\
                           )
B1024 = tg.character_map.parse(" ---- " + "\n"\
                               "|1024|" + "\n"\
                               " ---- " + "\n"\
                           )
B2048 = tg.character_map.parse(" ---- " + "\n"\
                               "|2048|" + "\n"\
                               " ---- " + "\n"\
                           )
B = [B2, B4, B8, B16, B32, B64, B128, B256, B512, B1024, B2048]

class TwentyFourtyEightGameUI():
	"""
	A User Interface class to handle all the game logic and rendering of the 2048
	"""
	def __init__(self):
		self.screen = tg.character_display.CharacterDisplay(80, 24) # the game UI creates a 80 x 24 character screen to draw the game upon
		self.grid = tg.character_map.parse( "1123" + "\n"\
		                                    "4567" + "\n"\
		                                    "89 1" + "\n"\
		                                    "2  5")
		self.done = False
		self.highscore = tg.HighScoresGUI(tg.HighScoresDB("examples/data/snake/scores.txt"))

	def intro(self):
		try:
			title_card = """
  ============================================================================  


                                       2048






                                                                                
                                                      Presented in            
                                                          tinygame            
                                                                              
                             Nick Miller 2014                                 
  ============================================================================  
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
		self.screen.write_text(30, 10, "Game Over!") # write Game Over!
		self.screen.show() # make sure to .show() so its visible on the console
		tg.time.sleep(1.5) # sleep with no key presses
		tg.keyboard.getch(1.0) # wait for a key press for the last second. Also clears the keypresses for the next screen
		
	def show_win(self):
		"""
		The UI shows game winner screen for 2.5 seconds
		"""
		self.screen.fill(' ')
		self.screen.write_text(30, 10, "You Win!\nCongratulations!") # Write you win
		self.screen.show() # make sure to .show() so its visible on the console
		tg.time.sleep(1.5) # sleep with no key presses
		tg.keyboard.getch(1.0) # wait for a key press for the last second. Also clears the keypresses for the next screen

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

	def combine_updown(self):
		for x in xrange(0, 4):
			for y in xrange(0, 3):
				me = self.grid[x,y]
				if me == ' ': continue
				below = self.grid[x, y+1]
				if me == below:
					self.grid[x, y + 1] = chr(int(me) +1 + ord('0'))
					self.grid[x,y] = ' '

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

	def combine_leftright(self):
		for y in xrange(0, 4):
			for x in xrange(0, 3):
				me = self.grid[x,y]
				if me == ' ': continue
				right = self.grid[x+1, y]
				if me == right:
					self.grid[x+1, y] = chr(int(me) +1 + ord('0'))
					self.grid[x,y] = ' '

	def up(self):
		self.slide_up()
		self.screen.show()
		self.render_grid()
		tg.keyboard.getch(1/10.0)
		self.combine_updown()
		self.screen.show()
		self.render_grid()
		tg.keyboard.getch(1/10.0)
		self.slide_up()
		
	def down(self):
		self.slide_down()
		self.screen.show()
		self.render_grid()
		tg.keyboard.getch(1/10.0)
		self.combine_updown()
		self.screen.show()
		self.render_grid()
		tg.keyboard.getch(1/10.0)
		self.slide_down()

	def left(self):
		self.slide_left()
		self.screen.show()
		self.render_grid()
		tg.keyboard.getch(1/10.0)
		self.combine_leftright()
		self.screen.show()
		self.render_grid()
		tg.keyboard.getch(1/10.0)
		self.slide_left()
	def right(self):
		self.slide_right()
		self.screen.show()
		self.render_grid()
		tg.keyboard.getch(1/10.0)
		self.combine_leftright()
		self.screen.show()
		self.render_grid()
		tg.keyboard.getch(1/10.0)
		self.slide_right()

	def render_grid(self):
		self.screen.fill(' ')
		for x in xrange(0, 4):
			for y in xrange(0, 4):
				b = self.grid[x, y]
				if b == ' ': continue
				Bxy = B[int(b)]
				self.screen.draw(5*x+1, 2*y+1, Bxy)

	def play(self):
		"""
		The UI plays a round of 2048 game. 
		"""
		self.done = False
		while True: # play forever until something happens
			self.render_grid()
			self.screen.show() # show the updated screen to the user once per frame -- now

			k = tg.keyboard.getch(10.0) # get the keypress and set nibbles direction (nibbles.dx, nibbles.dy) accordingly. Wait 1/10 of a second so the game progresses if no key is pressed
			if k == 'r':
				mall = "   012"
				for x in xrange(0, 4):
					for y in xrange(0, 4):
						self.grid[x,y] = mall[random.randint(0, len(mall)-1)]
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

	def finalize(self):
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
