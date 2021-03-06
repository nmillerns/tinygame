"""
character_map
This submodule contains a specification of character map data and useful text drawing functions
A character map is a mutable rectangular array of characters akin to a bitmap. Basically you have characters instead of pixels. Drawing fuhctions render
text and shapes onto character maps and can draw one character map onto another
"""

class CharacterMap():
	"""
	A class representing a rectangular array of characters akin to a bitmap.

	It provides various drawing and manupulation fuhctions to render text and shapes onto character maps 
	and can copy one character map onto another
	"""
	def __init__(self, width, height):
		"""
		Constructor for the CharacterMap. The width and height must be specified. 

		The data is constructed and filled with ' ' blanks

		width: a positive integer representing the desired width of the map
		height: a positive integer representing the desired height of the map
		"""
		self.width = width
		self.height = height
		self.rows = [CharacterRow(self.width) for i in range(0, self.height)] # The data is constructed as a series of rows. See CharacterRow inner class below

	def fill(self, character):
		"""
		Fills the entire character_map with the specified character repeated over and over

		character: a single character string representing the derired character to fill the map. eg 'x'
		"""
		for row in self.rows:
			row.fill(character) # do the filling work row wise. See CharacterRow.fill()

	def write_text(self, x, y, text):
		"""
		Writes the given text at a given location

		This is for writing (possibly multiple lines) text onto this map. If it is multiple lines the text continues on the next row (y + 1) starting at the same column (x). The message is clipped so there is no problem if it runs off the character map.

		x: an integer representing the left position to start the text message
		y: an integer representing the top position to start the text message
		text: a string the message to write into the map. It could be multiple lines. eg 'Hello,\nWorld!'
		"""
		lines = text.split('\n') # first split the text by the newline character into multiple lines
		for i in range(0, len(lines)): # go throught each line
			for j in range(0, len(lines[i])): # write all the characters in the line in the appropriate row, and column
				self[x + j, y + i] = lines[i][j] if lines[i][j] not in ['\t'] else ' ' # draw only printable characters

	def draw_image(self, x, y, character_map, chromakey = None):
		"""
		Draws the other CharacterMap character_map on self.

		Composited the given CharacterMap, character_map onto this CharacterMap at posion x, y (which are allowed to be negative, in which case the other character_map is properly clipped)
		Chromakey provides an (optional) character designated as "transparent". Like the blue in "blue-screening". Any instance of this character in character_map means transparecy and the original self data shows through
		It is made for readable strings to use ' ' as a chromakey but any unused character is possible.

		x: an integer representing the x coordinate where the top left character of other appears
		y: an integer representing the y coordinate where the top left character of other appears
		character_map: a CharacterMap to be composited onto this CharacterMap
		chromakey: a single character string representing the transparent characters in other. Typically None or ' '
		"""
		x0 = max(0, x) # start drawing at column x but clip it to 0 if we are drawing starting off the screen
		y0 = max(0, y) # start drawing at row y but clip it to 0 if we are drawing starting off the screen
		x1 = min(self.width, x + character_map.width) # clip right
		y1 = min(self.height, y + character_map.height) # clip the bottom
		ck = chromakey # It is allowed to be None
		for yi in range(y0, y1): # go through the clipped rows and columns and draw
			for xi in range(x0, x1):
				c = character_map.rows[yi-y].characters[xi-x] # we get the character to draw from other at the correct offset
				if c != ck: self.rows[yi].characters[xi] = c # place the character on self unless it matches the chromakey character "colour"

	def clone(self):
		"""
		Creates a new copy of this CharacterMap of the same width and height. 

		A new CharacterMap of the same heght and width returned and all the data of self is copied to it
		"""
		cmap = CharacterMap(self.width, self.height)
		cmap.draw_image(0, 0, self) # simply draw yourself on the new map
		return cmap

	def scroll_up(self, amount = 1):
		"""
		Rolls the rows of this chacter map up amount rows by changing the offset of the "top" row

		The rows which were "scrolled off" the top roll around and appear on the bottom 

		amount: a positive integer less than self.height specifying how many rows to scroll off the top
		"""
		amount = amount % self.height
		temp = self.rows
		self.rows = temp[amount:]
		self.rows.extend(temp[0:amount])

	def scroll_down(self, amount = 1):
		"""
		Rolls the rows of this chacter map down amount rows by changing the offset of the "top" row

		The rows which were "scrolled off" the bottom roll around and appear on the top

		amount: a positive integer less than self.height specifying how many rows to scroll off the top
		"""
		amount = amount % self.height
		temp = self.rows
		self.rows = temp[self.height-amount:]
		self.rows.extend(temp[0:self.height - amount])

	def scroll_left(self, amount = 1):
		"""
		Rolls the colums of this chacter map left amount columns. 
		
		The columns which were "scrolled off" the left roll around and appear on the right.
		amount: a positive integer less than self.width specifying how many rows to scroll off the left
		"""
		amount = amount % self.width
		for row in self.rows:
			temp = row.characters
			row.characters = temp[amount:]
			row.characters.extend(temp[0:amount])

	def scroll_right(self, amount = 1):
		"""
		Rolls the colums of this chacter map right amount columns. 
		
		The columns which were "scrolled off" the right roll around and appear on the left.
		amount: a positive integer less than self.width specifying how many rows to scroll off the right
		"""
		amount = amount % self.width
		for row in self.rows:
			temp = row.characters
			row.characters = temp[self.width-amount:]
			row.characters.extend(temp[0:self.width - amount])

	def __setitem__(self, x_y, value):
		"""
		An item setter operator override.  It overrides the square bracket index operator. 

		The x_y pair argument lets you call it with a coordinate in the brackets.
		eg
		mymap[10,12] = '*' # calls this method with x=10,y=12 and value = '*'

		x_y: an integer pair specifing the target coordinate
		value: a single character string representing the desired value to set. eg '*'
		"""
		x, y = x_y
		try: # simply try and draw and catch exceptions so nothing happens if we try to draw off the map
			self.rows[y][x] = value # this in turn calls the setter in CharacterRow class. See CharacterRow.__setitem__
		except IndexError as e:
			pass # we just ignore when a character is drawn completely out of bounds

	def __getitem__(self, x_y):
		"""
		An item getter operator override.  It overrides the square bracket index operator. 

		The (x,y) pair argument lets you call it with a coordinate in the brackets.
		eg
		peek = mymap[10,12] # calls this method with x=10,y=12

		x_y: an integer pair specifing the coordinate you want to get
		return: a single character string representing the value in the character map. eg '*'
		"""
		x, y = x_y
		try:
			return self.rows[y][x] # this in turn calls the getter in CharacterRow class. See CharacterRow.__getitem__
		except IndexError as e:
			return None # return None when character is completely out of bounds

	def __str__(self):
		"""
		String operator overload. Converts the content of the character map to a string.

		Use newline characters to seperate the rows
		This is called whenever you call:
			str(my_charactermap)

		return: a string representation of this map
		"""
		return '\n'.join([str(row) for row in self.rows]) # the new line puts each row of characters on a new line. In turn the __str__ overload is called on each row. See CharacterRow.__str__()

	def __eq__(self, other):
		"""
		Compares the content of two character maps to see if they are identical
		"""
		if (self.width, self.height) != (other.width, other.height): return False # must be the same dimensions
		return all([r == s for r,s in zip(self.rows, other.rows)]) # check content row by row

	def __ne__(self, other):
		"""
		Compares the content of two character maps to see if they are identical
		"""
		return not self.__eq__(other)

class CharacterRow():
	"""
	A class representing one row of character data.

	A CharacterMap is actually broken down into a series of rows
	"""
	def __init__(self, width):
		self.width = width
		self.characters = [' ' for i in range(0, width)]
	def __getitem__(self, i):
		return self.characters[i]
	def __setitem__(self, i, character):
		self.characters[i] = character
	def __str__(self):
		return ''.join(self.characters) #just joining the characters together to form a row string
	def __eq__(self, other):
		return self.width == other.width and all([d == e for d, e in zip(self.characters, other.characters)])
	def fill(self, character):
		self.characters = [character for i in range(0, self.width)] # set each item in the row to the char value given

def load(filename):
	"""
	Loads a CharacterMap from the given textfile

	filename: a string path to a text file
	returm: a CharacterMap loaded with content from the file
	"""
	f = open(filename) #open the file
	cm = parse(f.read()) # simply read in the content as a string and reuse the parse(string) function to do the work
	f.close() # close now the we're finished
	return cm

def parse(s):
	"""
	Parses a CharacterMap from a string.

	The string should contain a set of rows separated by new lines. Ideally it is rectangular (ie each line the same length), 
	but irregular lines are supported (in which case the map is the width of the longest line and the remainders are filled with blanks ' '

	s: a string. eg '#########\nA map!\n#########'
	return: a CharacterMap loaded with content from the string
	"""
	lines = s.split('\n') # split by newline into a series of rows
	if len(lines[-1]) == 0: lines = lines[0:-1] #somtimes strings from file have a final newline with no row at the end. Simply discard the empty one
	width = max([len(line) for line in lines]) if len(lines) else 0# if the rows are irregular we can use the max row and fill the rest with ' ' blanks
	height = len(lines) 
	cm = CharacterMap(width, height) # this fills a whole map with ' 'blanks using the max row and height
	cm.write_text(0, 0, s) # the text writing function is handy to actually fill in the data using a string
	return cm
