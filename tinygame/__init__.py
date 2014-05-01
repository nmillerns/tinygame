"""
tinygame
A verylightweight educational library for creating simple text based games.
It is intended to be useful while being fully understandable in terms of the details on how it works.
Games can be programmed making use of CharacterMaps and CharacterDisplays (See character_map.py and character_display.py) 
as well as user input from the keyboard. (See keyboard.py). Unfortunately sound and music is not supported since it is not considered as simple.
Example games reside in the examples/ directory
"""

import keyboard # import the keyboard submodule. See keyboard.py
import character_display # import the character_display submodule. See character_display.py
import character_map # import the character_map submodule. See character_map.py
import time

class Metronome():
	"""
	A class that behaves like the name suggests. It is a metronome that ticks with a regular beat.

	The peroid of the beat is specified by the user.
	This is useful for having a consistent frame rate in a game eg 24 frames per second (period 1.0/24)
	Typically you would set up a Metronome with your desired framerate and calculate your game logic and
	show a new frame after wait_for_tick()

	eg

	metronome = Metronome(1.0/24)
	while True:
		... # handle user input
		... # game logic
		metronome.wait_for_tick()
		myscreen.show()

	Just a warning. You should also use a delay of the same or nearly equal length in keyboard.getch() in you main loop. 
	The reason for this is because you want to be spending as much time as possible allowing the user to input keys and not idling
	waiting for the next frame. They work best in combination since wait_for_tick() will return immediately if the time period of a frame
	has already passed. It is simply a way to ensure a whole period is respected if a key hit registers early on and returns from getch() early.
	See keyboard.py and examples/snake.py
	"""
	def __init__(self, period):
		"""
		Creates a metronome with the specified tick rate as a floating point peroid between ticks

		period: a float representing the amount of time (in seconds) between beats. eg 0.1 for 10 beats a second
		"""
		self.period = period
		self.reset()

	def reset(self):
		"""
		Resets the since tick in the metronome. The time of the most recent tick is set to now.
		"""
		self.previous = time.time() # use the current time now as the most recent tick

	def wait_for_tick(self):
		"""
		Sleeps until the next tick of the metronome. If a tick has already occured since last calling wait_for_tick() an exception is caught and it returns immediately
		"""
		try: # use the time.sleep to sleep until the next tick
			time.sleep(self.period - (time.time() - self.previous))
		except (IOError, TypeError), e: # simply catch the exceptions when we have to seleep negative time (tick already passed) or no previous time was specified
			pass
		finally:
			self.reset() # always set the time of last tick to now

def initialize():
	"""
	Initializes the whole tinygame library.

	This should be called exactly once at the beginning of your game program when you are ready to use it.
	It should always be complimented with a corresponding call to tinygame.quit() when your program quits.
	If you fail to call tinygame.quit() you may get terminal printing issues.
	Hence you should ensure you always call tinygame.quit() even when you leave on error using a try block:

	eg

	tinygame.initialize()
	try:
		... # game code
	finally:
		tinygame.quit()
	"""
	keyboard.initialize()
	character_display.initialize()

def quit():
	"""
	De-initializes the whole tinygame library.

	It restores the screen and keyboard control modes.
	If you fail to call tinygame.quit() you may get terminal printing issues.
	Hence you should ensure you always call tinygame.quit() even when you leave on error using a try block:

	eg

	tinygame.initialize()
	try:
		... # game code
	finally:
		tinygame.quit()
	"""
	keyboard.quit()
	character_display.quit()

class HighScoresDB():
	"""
	A class implementing a Database (DB) for awarding the top scores and storing them.

	Each score is stored as a pair of [name], [score]. There are N top scores where N is specified by the programmer. The scores are stored in increasing order. You may check if the ranking of
	any given score. Thr ranking lies in 0 to N-1, or N if it does not fall in the top N scores. 
	"""
	def __init__(self, filename, N = 10):
		"""
		Constructor for a High Score Database. It will be stored as plain text in filename. It will contain the top N scores (default N = 10)
		
		filename: a sting containing  path and filename of a plaintext file that will store the simple high scroes database
		N: a positive integer representing the number of top entries you would like to store in the database
		"""
		self.filename = filename
		self.N = N
		self.data = [("None", 0) for i in xrange(0, self.N)]

	def save(self):
		"""
		Saves this High Scores Database to a plaintext file. It uses self.filename provided at construction
		"""
		f = open(self.filename, "w")
		for name, score in self.data:
			f.write("%s, %d\n"%(name, score))
		f.close()

	def restore(self):
		"""
		Loads the High Scores Database back in from its plaintext file. If the file doesn't exist an empty high scores list results with N blank names and scores of 0
		"""
		try:
			self.data = []
			f = open(self.filename, "r")
			lines = [line for line in f.read().split('\n') if line != ""]
			for line in lines:
				name, score_string = line.split(',')
				self.data.append( (name, int(score_string)) )
			f.close()

		except IOError, e:
			self.data = [("None", 0) for i in xrange(0, self.N)]
			
	def ranking(self, score):
		"""
		Determine the ranking of a new score in this database. In 0..N-1 if it ranks in the top N or N
		"""
		return len([s for n,s in self.data if score <= s])

	def insert(self, name, score):
		self.data.append((name, score))
		self.data.sort(key = lambda pair:-pair[1])
		self.data = self.data[0:-1]

class HighScoresGUI():
	"""
	"""
	def __init__(self, highscoresDB):
		"""
		"""
		self.highscoresDB = highscoresDB
		self.highscoresDB.restore()

	def scroll_on(self, screen, scroll_off = True):
		"""
		Scrolls the rankings on to the screen to reveal the top scores one at a time

		It scrolls until the last ranking appears at the bottom of the screen. If specified it will also.
		If it is interrupted with a keypress the slow scrolling high scores screen showing is aborted
		wait for 2 seconds and scroll back off the sreen revealing whatever was on the previous screen before showing the high scores screen
		
		scroll_off: boolean if true the high scores screen will wait 2 seconds and scroll back off (unless interrupted by a key hit)
		"""
		keyboard.getch(0) # clear all keys
		plate = character_map.CharacterMap( screen.width, max(screen.height, self.highscoresDB.N+2) )
		prev = screen.clone() # store the previous screen to restore it when we are done
		text = "" # put the high score names and scores into text
		maxlen = 0
		i = 0
		for name, score in self.highscoresDB.data: # put each line in text
			i += 1
			line = "%2d: %s ...... %d\n"%(i, name, score)
			text += line
			maxlen = max(maxlen, len(line))
		x = plate.width / 2 - 9
		plate.write_text(x, 0, "*** High Scores ***") # write the text into a high scores screen
		x = plate.width / 2 - maxlen / 2
		plate.write_text(x, 2, text)

		for i in xrange(0, plate.height): # scroll the plate on one name at a time from the top
			screen.scroll_down()
			screen.draw(0, i-plate.height+1, plate) # draw the names plate in the gap you just scrolled off
			screen.show()
			if keyboard.getch(.07) != None: return # tick at 1/.07 = 14.286 fps

		if keyboard.getch(2) != None: return # wait 2 seconds

		if scroll_off: # scroll back off
			for i in xrange(0, screen.height):
				screen.scroll_down()
				screen.draw(0, i-screen.height+1, prev)
				screen.show()
				if keyboard.getch(.07) != None: return
	def handle_new_score(self, score, screen):
		"""
		Takes in a new score and chacks if it ranks, and if so get the user's name and show the new list including the new user's name
		
		score: a number representing the score the user achieved
		screen: the screen to show stuff on 
		"""
		if self.highscoresDB.ranking(score) < self.highscoresDB.N: # determine the ranking and if it should be entered
			name = self.input_name(screen) # get the name from the user
			self.highscoresDB.insert(name, score) # subit the name in the database... It bumps off the old bottom ranker
			self.highscoresDB.save() # re-save the scores in the database file
			self.scroll_on(screen, scroll_off = False) # scroll away the name input screen to show the scores
			keyboard.getch(4) # wait for a key hit for 4 seconds
			# then we go back and normal gui control flow is resumed

	def input_name(self, screen, maxlen=10):
		"""
		Type in the name for entry for high score
		
		screen: the screen to show stuff on
		maxlen: the maximum number of characters allowed in the name (default 10)
		"""
		def update_display():
			"""
			An inner helper function to refresh the screen display as the name is typed
			"""
			x = screen.width/2 - 7
			screen.fill(' ')
			screen.write_text(x, 1, "New High Score!")
			x = screen.width/2 - (maxlen + 12)/2
			screen.write_text(x,3, "Enter Name: " + name)
			screen.show()

		name = ""
		ch = None
		update_display()

		while True:
			ch = keyboard.getch(10000)
			if ch == '\n': break
			elif ch == keyboard.KEY_BACKSPACE: name = name[0:len(name)-1]
			elif ch not in [',', ' ', None] and len(ch) == 1 and len(name) < maxlen: name += ch
			update_display()

		return name
