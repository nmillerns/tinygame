"""
character_display
A submodule of tinygame for a virtual video game display consisting of only characters
You may manipulate it and change character cells. Typically as the your game takes place it will update the data in the screen character map showing the current state of the game UI.
You continually update the character map and show it once per time slice / frame of game time or whenever you want to show an update.
"""

import os
import sys
from character_map import *

# This submodule makes use of ANSI control sequences to position characters on the terminal display
# See http://en.wikipedia.org/wiki/ANSI_escape_code
ESCAPE = chr(27)

"""control sequences are started by writing a special sequence of characters to the terminal known as a Control Sequebce Introducer (CSI)"""
CSI = ESCAPE + "[" # control sequences are started by writing a special sequence of characters to the terminal known as a Control Sequebce Introducer (CSI)
HIDE_CURSOR_SEQUENCE = CSI + "?25l" # the control sequence which hides the console cursor
SHOW_CURSOR_SEQUENCE = CSI + "?25h" # the control sequence which shows the console cursor
MOVE_HOME_SEQUENCE = CSI + "H" # the control sequence which moves the cursorback home to the top left corner of the console


def initialize():
	os.system("clear") # first clear the screen using the os command
	sys.stdout.write(HIDE_CURSOR_SEQUENCE) # hide the cursor because it is annoying and would get in the way of a game's display screen. Uses ANSI escape sequences

def quit():
	os.system("clear") # clear the console to put show a clean console to the user when we leave
	sys.stdout.write(SHOW_CURSOR_SEQUENCE) # turn the user's cursor back on like they expect. Uses ANSI escape sequences

class CharacterDisplay(CharacterMap): # Inherit from the CharacterMap class.
	"""
	A class representing a virtual video game display consisting of only characters (it extends the CharacterMap class)
	it can have a user specified width and height
	It is a special form of CharacterMap which can be showed on screen by calling show(). When shown it appears on the user's console
	You may manipulate it and change cells like any regular CharacterMap. See character_map.py
	Typically as your game takes place it will update the data in the screen CharacterMap showing the current state of the game UI.
	You continually update the character map and .show() it once per time slice / frame of game time. You generally only want to .show() once per frame to avoid flickering
	"""

	def __init__(self, width = 80, height = 24):
		"""
		Creates a character display screen of specified width and height

		width: a positive integer representing the desired width of the display
		height: a positive integer representing the desired height of the display
		"""
		CharacterMap.__init__(self, width, height)
		self.dirty = True # use a dirty bit to track if the user's console view is up to date. That way we only refresh if necessary

	def show(self):
		"""
		Updates the user's console with the current state of the screen

		You should do this exactly once per time slice. There is no cost to calling this many times if there is no change in the display as the dirty bit tracks if it needs to actually be pushed on screen.
		WARNING! If you change and show the screen too oftern flickering may result. Only .show() when you finalize how the screen should look.
		"""
		if self.dirty: # use a dirty bit to track if the user's console view is up to date. That way we only refresh if necessary
			sys.stdout.write(MOVE_HOME_SEQUENCE) # start off at the top left and draw everything. Uses ANSI escape sequences
			# We want to convert the character map into a single string for easy printing
			sys.stdout.write(str(self)) #simply print a string version of the whole characte map with newline characters for each row etc. See CharacterMap.__str__() in character_map.py
			sys.stdout.flush() # flush the output so it is shown by the OS immediately instead of waiting for enough data
			self.dirty = False # We have just updated the console so obviously the screen is not dirty

	def __setitem__(self, (x, y), value):
		"""
		Same as setting a value in a normal character map. See CharacterMap
		"""
		if self[x,y] != value:
			CharacterMap.__setitem__(self, (x, y), value)
			self.dirty = True # same except we now know the screen data is now different so set the dirty bit

	def fill(self, character):
		"""
		Same as filling a normal character map. See CharacterMap
		"""
		CharacterMap.fill(self, character)
		self.dirty = True # same except we now know the screen data is now different so set the dirty bit

	def scroll_up(self, amount = 1):
		"""
		Same as scrolling a normal character map. See CharacterMap
		"""
		CharacterMap.scroll_up(self, amount)
		self.dirty = True # same except we now know the screen data is now different so set the dirty bit

	def scroll_left(self, amount = 1):
		"""
		Same as scrolling a normal character map. See CharacterMap
		"""
		CharacterMap.scroll_left(self, amount)
		self.dirty = True # same except we now know the screen data is now different so set the dirty bit

	def draw(self, x, y, other, chromakey = None):
		"""
		Same as drawing onto a a normal character map. See CharacterMap
		"""
		CharacterMap.draw(self, x, y, other, chromakey)
		self.dirty = True # same except we now know the screen data is now different so set the dirty bit

	def write_text(self, x, y, text):
		"""
		Same as write_text on a normal character map. See CharacterMap
		"""
		CharacterMap.write_text(self, x, y, text)
		self.dirty = True # same except we now know the screen data is now different so set the dirty bit

