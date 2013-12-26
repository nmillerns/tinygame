import sys
import random
sys.path.append('.')
import tinygame as tg

class Apple():
	"""
	A class repesenting a simple apple that a snake can eat to grow and gain points.
	It doesn't do much but one method is responsible for drawing the apple corrctly on a given character map
	"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def draw(self, character_map):
		"""
		Draws the apple as () on the given CharacterMap
		"""
		character_map[2*self.x, self.y] = '(' # we do 2*x because we use 2 character per coordinate to make a square grid since characters are wider than tall
		character_map[2*self.x + 1, self.y] = ')'

class Snake():
	"""
	A class represinting a snake that moves along. It has a length and can grow in length.
	It has a head which moves and a tail which follows.
	It uses linked lists (see http://en.wikipedia.org/wiki/Linked_list) to track the head and have the trailing body parts to the tail.
	The list consists of linked segments. See the Segment inner class.
	"""
	def __init__(self, x0, y0, x1, y1, dx, dy):
		"""
		Starts of a snake of length 5 at the specified location in the specified location. It initalli has 2 segments but grows until 5.
		The two segments are exactly the head and the tail only. The tail starts out at x0,y0 and the head at x1,y1. It moves in the direction dx,dy
		"""
		self.head = SnakeSegment(x1, y1) # creates a head segment. The head is the newest segment so it has no successor link
		self.tail = SnakeSegment(x0, y0, self.head) # creates the tail. There are only 2 segments so the head is the direct successor of the tail
		self.current_length = 2 # it is currently length 2
		self.length = 5 # we want length 5
		self.x, self.y = x1, y1 # its head location is x1, y1
		self.dx, self.dy = dx, dy # point in the specified direction

	def tick(self):
		"""
		Handles the snakes dynamics for one time slice of the game. It is basically just moving in direction dx, dy and growing/rolling the snake along
		"""
		self.x += self.dx # step the position in the direction dx, dy
		self.y += self.dy
		new_segment = SnakeSegment(self.x, self.y) # create a new segment at its new location
		self.head.next = new_segment # link up the new segment as the successor to the old head and it will become the new head
		self.head = new_segment # becomes the new head
		self.current_length += 1 # this new segment necessarily increases the current length by 1
		while self.current_length > self.length: # we don't want the snake to grow forever so we should "eat up" old segments until it is the desired length
			self.tail = self.tail.next # by following and re-pointing the tail to the successor we "lose" or "eat up" the old tail
			self.current_length -= 1 # since we lost a segment the current size necessairly decreases by 1
		
	def draw_body(self, character_map):
		"""
		Draws the body segments of the Snake on a given character map. Not the head which is a special case
		"""
		s = self.tail # we start at the tail and follow the link structure to draw all the segments
		while s != self.head: # go until we reach the head but don't draw it. See draw_head
			s.draw(character_map) # each segment can draw itself see Snake.Segment.draw()
			s = s.next # follow the current point to its successor

	def draw_head(self, character_map):
		"""
		Draws the head only of the Snake. This is a special last case since we want to check special conditions of game logic before drawing the head.
		For example we must check that the head isn't colliding with another body segment so we must pre-draw the body and check the screen first
		"""
		self.head.draw(character_map)

class SnakeSegment():
	"""
	A single segment as part of a Snake. Each segment points to its successor linking up a whole Snake. Starting with the tail, each next piece is a successor. The head has no successor.
	They lie in a certain position x,y and have a method to draw themselves
	"""
	def __init__(self, x, y, next = None):
		self.x = x
		self.y = y
		self.next = next

	def draw(self,character_map):
		"""
		Draws the segment onto a CharacterMap at the specified location appearing as []
		"""
		character_map[2*self.x, self.y] = '[' # we do 2*x because we use 2 character per coordinate to make a square grid since characters are wider than tall
		character_map[2*self.x + 1, self.y] = ']'


class SnakeGameUI():
	"""
	A User Interface class to handle all the game logic and rendering of the Snake game. It uses the classes defined above
	"""
	def __init__(self):
		self.score = 0 # the game UI tracks the score
		self.lives = 10 # the game UI tracks the players number of lives
		self.level = 1 # the game UI what stage the player is in
		self.screen = tg.character_display.CharacterDisplay(80, 24) # the game UI creates a 80 x 24 character screen to draw the game upon
		self.done = False # the game UI if we are done playing
		self.highscore = tg.HighScoresGUI(tg.HighScoresDB("examples/data/snake/scores.txt"))
		
	def show_stats(self):
		"""
		The UI shows the players stats on screen for 2.5 seconds
		"""
		self.screen.fill(' ') # clears the screen
		self.screen.write_text(30, 10, "Lives: " + str(self.lives) +"\n\nLevel: " + str(self.level) ) # Write the stats
		self.screen.show() # make sure to .show() so the stats are visible on the console
		tg.time.sleep(1.5) # sleep with no key presses
		tg.keyboard.getch(1.0) # wait for a key press for the last second. Also clears the keypresses for the next screen

	def intro(self):
		try:
			title_card = """
  ============================================================================  



                        .----..-. .-.  .--.  .-. .-..----.                    
                       { {__  |  `| | / {} \ | |/ / | {_                      
                       .-._} }| |\  |/  /\  \| |\ \ | {__                     
                       `----' `-' `-'`-'  `-'`-' `-'`----'                    

                      [][][][][][][][][][][][][][][][][][][]







                                                                                
                                                      Presented in            
                                                          tinygame            
                                                                              
                             Nick Miller 2013                                 
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

	def play_round(self):
		"""
		The UI plays a round of Snake game. It plays at the current level until you die or progress
		"""
		nibbles = Snake(4, 5, 5, 5, 1, 0) # Create the users snake named nibbles
		metronome = tg.Metronome(1/10.0) # Use a metronome to maintain 10 fps

		bg = tg.character_map.load("examples/data/snake/level" + str(self.level) + ".txt") # load the level background from a text file into the bg CharacterMap
		aapple = None # For no we dont have a apple. One will be created during play
		apples_eaten = 0 # track how many apples have been eaten this round so we know when we can progress a level

		while True: # play forever until something happens
			k = tg.keyboard.getch(1/10.0) # get the keypress and set nibbles direction (nibbles.dx, nibbles.dy) accordingly. Wait 1/10 of a second so the game progresses if no key is pressed
			if k == tg.keyboard.KEY_UP:
				nibbles.dx, nibbles.dy = 0, -1
			if k == tg.keyboard.KEY_DOWN:
				nibbles.dx, nibbles.dy = 0, 1
			if k == tg.keyboard.KEY_LEFT:
				nibbles.dx, nibbles.dy = -1, 0
			if k == tg.keyboard.KEY_RIGHT:
				nibbles.dx, nibbles.dy = 1, 0
			if k == tg.keyboard.KEY_ESCAPE:
				self.done = True
				break

			nibbles.tick() # nibbles handles his own movement. See the Snake.tick() method

			self.screen.draw(0, 0, bg) # first redraw the background on screen
			self.screen.write_text(5,0, "Lives: " + str(self.lives)) # write the stats at the top
			self.screen.write_text(40,0, "Level: " + str(self.level))
			self.screen.write_text(70,0, "Score: " + str(self.score))

			nibbles.draw_body(self.screen) # draw the body of the snake first. This way we can place the apple anwhere not on the body, and check that the head does not run into the body
			if aapple: aapple.draw(self.screen) # draw the apple if it exists

			if self.screen[2*nibbles.x,nibbles.y] == '(':  # check to see if the head is at the location of the apple
				nibbles.length += 5 # if so, eat it and grow nibbles
				aapple = None # no more apple. It was eaten. It will be recreated later
				self.score += 10 # get 10 pts for eating an apple
				apples_eaten += 1 # track how many nibbles has eaten
			elif self.screen[2*nibbles.x,nibbles.y] in ['|' , '[']: # check if the head has run into a wall or a body part
				self.lives -= 1 # if so lose a life
				break # and leave the round

			nibbles.draw_head(self.screen) # now draw the head

			if aapple == None: # check if there is no apple. If there isn't it must be regenerated
				while True: # go forever until we find a place for the apple
					ax = 2+random.randint(0, 39) # propose a random place
					ay = 2+random.randint(0, 21)
					if self.screen[2*ax,ay] == ' ': # check if it is an empty space with no head or body
						aapple = Apple(ax,ay) # this is the new apple
						break # we are done finding a place for the apple

			if apples_eaten >= 8: # check if we've eaten enough apples
				self.level += 1 # if so progress to the next stage
				break # and stop the round
			metronome.wait_for_tick() # wait for a metronome tick to keep the pace of the game at one rate. This will keep pase even if we get key presses that exit keyboard.getch() early
			self.screen.show() # show the updated screen to the user once per frame -- now

	def finalize(self):
		self.highscore.handle_new_score(self.score, self.screen)

def main():
	"""
	The main entrypoint to the snake game. It initializes librarys including tinygame and creates the Game UI
	"""
	tg.initialize() # initialize tinygame for use in the Snake game
	try:
		gameui = SnakeGameUI() # create a UI
		gameui.intro()
		while not gameui.done: # loop forever until the UI says it is done
			gameui.show_stats() # first show the player stats
			gameui.play_round() # then play a round of Snake game
			if gameui.lives < 1:  #  check that the user has lives left
				gameui.show_gameover() # if not show the game over screen
				gameui.done = True # then we are done
			if gameui.level > 5: # check if the user has passed level 5
				gameui.show_win() # if so show the user the winners screen
				gameui.level = 1 # go back to the beginning

		gameui.finalize()

	finally:
		tg.quit()

if __name__ == "__main__":
	main()
