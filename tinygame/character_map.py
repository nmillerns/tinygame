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
		self.offset_y = 0
		self.rows = [CharacterRow(self.width) for i in xrange(0, self.height)] # The data is constructed as a series of rows. See CharacterRow inner class below

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
		for i in xrange(0, len(lines)): # go throught each line
			for j in xrange(0, len(lines[i])): # write all the characters in the line in the appropriate row, and column
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
		ck = ord(chromakey) if chromakey != None else None # we use the 8bit ASCII value (ord()) of the chromakey since our data is 8bit. It is allowed to be None
		for yi in xrange(y0, y1): # go through the clipped rows and columns and draw
			for xi in xrange(x0, x1):
				lookup_y = (yi - y + character_map.offset_y) % character_map.height
				lookup_x = (xi - x + character_map.rows[lookup_y].offset) % character_map.width
				c = character_map.rows[lookup_y].data[lookup_x] # we get the character to draw from other at the correct offset
				if c != ck: 
					row = self.rows[(yi + self.offset_y) % self.height]
					row.data[(xi + row.offset) % row.width] = c # place the character on self unless it matches the chromakey character "colour"


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
		Rolls the rows of this chacter map up amount rows. 

		The rows which were "scrolled off" the top roll around and appear on the bottom

		amount: a positive integer less than self.height specifying how many rows to scroll off the top
		"""
		self.offset_y = (self.offset_y + amount) % self.height

	def scroll_down(self, amount = 1):
		"""
		Rolls the rows of this chacter map down amount rows. 

		The rows which were "scrolled off" the bottom roll around and appear on the top

		amount: a positive integer less than self.height specifying how many rows to scroll off the top
		"""
		self.offset_y = (self.offset_y - amount) % self.height

	def scroll_left(self, amount = 1):
		"""
		Rolls the colums of this chacter map left amount columns. 
		
		The columns which were "scrolled off" the legt roll around and appear on the right.
		amount: a positive integer less than self.width specifying how many rows to scroll off the left
		"""
		for row in self.rows:
			row.scroll_left(amount)

	def scroll_right(self, amount = 1):
		"""
		Rolls the colums of this chacter map left amount columns. 
		
		The columns which were "scrolled off" the legt roll around and appear on the right.
		amount: a positive integer less than self.width specifying how many rows to scroll off the left
		"""
		for row in self.rows:
			row.scroll_right(amount)

	def __setitem__(self, (x, y), value):
		"""
		An item setter operator override.  It overrides the square bracket index operator. 

		The (x,y) pair argument lets you call it with a coordinate in the brackets.
		eg
		mymap[10,12] = '*' # calls this method with x=10,y=12 and value = '*'

		(x,y): an integer pair specifing the target coordinate
		value: a single character string representing the desired value to set. eg '*'
		"""
		try: # simply try and draw and catch exceptions so nothing happens if we try to draw off the map
			y_lookup = (y + self.offset_y) % self.height
			self.rows[y_lookup][x] = value # this in turn calls the setter in CharacterRow class. See CharacterRow.__setitem__
		except IndexError, e:
			pass # we just ignore when a character is drawn completely out of bounds

	def __getitem__(self, (x,y)):
		"""
		An item getter operator override.  It overrides the square bracket index operator. 

		The (x,y) pair argument lets you call it with a coordinate in the brackets.
		eg
		peek = mymap[10,12] # calls this method with x=10,y=12

		(x,y): an integer pair specifing the coordinate you want to get
		return: a single character string representing the value in the character map. eg '*'
		"""
		try:
			y_lookup = (y + self.offset_y) % self.height
			return self.rows[y_lookup][x] # this in turn calls the getter in CharacterRow class. See CharacterRow.__getitem__
		except IndexError, e:
			return None # return None when character is completely out of bounds

	def __str__(self):
		"""
		String operator overload. Converts the content of the character map to a string.

		Use newline characters to seperate the rows
		This is called whenever you call:
			str(my_charactermap)

		return: a string representation of this map
		"""
		s = "" # create a string to build
		for row in self.rows[self.offset_y:]:
			s += str(row) + "\n" # the new line puts each row of characters on a new line. In turn the __str__ overload is called on each row. See CharacterRow.__str__()
		for row in self.rows[:self.offset_y]:
			s += str(row) + "\n" # the new line puts each row of characters on a new line. In turn the __str__ overload is called on each row. See CharacterRow.__str__()
		return s

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
		self.offset = 0
		self.data = [ord(' ') for i in xrange(0, width)]
	def __getitem__(self, i):
		lookup = (i + self.offset) % self.width
		return chr(self.data[lookup]) # turn the 8bit value back to a string for users
	def __setitem__(self, i, character):
		lookup = (i + self.offset) % self.width
		self.data[lookup] = ord(character) # we store the 8bit value (ord()) to save space
	def __str__(self):
		return ''.join([chr(val) for val in self.data[self.offset:]]) + ''.join([chr(val) for val in self.data[:self.offset]]) #just joing the characters together to form a row string
	def __eq__(self, other):
		return str(self) == str(other)
	def scroll_left(self, amount):
		self.offset = (self.offset - amount) % self.width
	def scroll_left(self, amount):
		self.offset = (self.offset + amount) % self.width
	def fill(self, character):
		self.data = [ord(character) for i in xrange(0, self.width)] # set each item in the row to the 8bit value given

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
