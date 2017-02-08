"""
Dringle?
"""
import sys
sys.path.extend(['.', '..'])
import tinygame as tg

class Player():
	LEFT = "<"
	RIGHT = ">"
	UP = "^"
	DOWN ="V"

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.image = self.DOWN

	def draw(self, screen):
		screen[self.x, self.y] = self.image


class Board():
	NEIGHBOURHOOD = [(0, -1), (0, 1), (-1, 0), (1, 0)]
	def __init__(self, data_map):
		self.data = data_map
		self.start_x, self.start_y = None, None
		self.__find_start()
		self.data[self.start_x, self.start_y] = "."

	def get_start(self):
		return (self.start_x, self.start_y)

	def draw(self, screen):
		screen.draw_image(0, 0, self.data)

	def __find_start(self):
		for y in xrange(0, self.data.height):
			for x in xrange(0, self.data.width):
				if self.data[x, y] == 'S':
					self.start_x, self.start_y = x, y

	def in_bounds(self, x, y):
		return 0 <= x and x < self.data.width and 0 <= y and  y < self.data.height

	def valid_move(self, start, direction):
		x, y = start
		dx, dy = direction
		x += dx
		y += dy
		if not self.in_bounds(x, y): return False
		if self.data[x, y] == '#': return False
		if self.is_empty(x, y): return True
		# Otherwise it must be a block to be pushed, look at another step forward to see if it can be moved into an empty space
		x += dx
		y += dy
		if not self.in_bounds(x, y) or self.data[x, y] != '.': return False
		return True

	def is_empty(self, x, y):
		return self.data[x, y] == '.' or self.data[x, y] == 'X'


	def eliminate_matches(self, x, y):
		if self.is_empty(x, y): return
		target = self.data[x, y]
		if target == '#': return
		for direction in self.NEIGHBOURHOOD:
			dx, dy = direction
			if self.in_bounds(x + dx, y + dy) and self.data[x + dx, y + dy] == target:
				self.data[x, y] = '.'
				self.data[x + dx, y + dy] = '.'
	def change(self, x, y):
		if self.is_empty(x, y): return
		for direction in self.NEIGHBOURHOOD:
			dx, dy = direction
			if self.in_bounds(x + dx, y + dy) and self.data[x + dx, y + dy] == '#':
				self.data[x, y] = '#'

class DringleUI():
	def __init__(self):
		self.level = 0
		self.board = None
		self.player = None
		self.screen = tg.character_display.CharacterDisplay(16, 8)
		self.done = False
		self.exit = False

	def move_player(self, direction):
		position = self.player.x, self.player.y
		x, y = position
		if self.board.valid_move(position, direction):
			dx, dy = direction
			self.player.x += dx
			self.player.y += dy
		# check to see if you are oushing a block too
		x, y = self.player.x, self.player.y
		if not self.board.is_empty(x, y):
			self.board.data[x + dx, y + dy] = self.board.data[x, y]
			self.board.data[x, y] = '.'
			self.board.change(x + dx, y + dy)
			self.board.eliminate_matches(x + dx, y + dy)
		
	def up_pressed(self):
		self.player.image = Player.UP
		self.move_player((0, -1))

	def down_pressed(self):
		self.player.image = Player.DOWN
		self.move_player((0, 1))

	def left_pressed(self):
		self.player.image = Player.LEFT
		self.move_player((-1, 0))

	def right_pressed(self):
		self.player.image = Player.RIGHT
		self.move_player((1, 0))

	def play_round(self):
		self.load_level()
		x,y = self.board.get_start()
		self.player = Player(x, y)
		self.done = False
		while not self.done:
			self.screen.fill(' ')
			self.board.draw(self.screen)
			self.player.draw(self.screen)
			self.screen.show()
			k = tg.keyboard.getch(10.0)
			if k == tg.keyboard.KEY_UP:
				self.up_pressed()
			if k == tg.keyboard.KEY_DOWN:
				self.down_pressed()
			if k == tg.keyboard.KEY_LEFT:
				self.left_pressed()
			if k == tg.keyboard.KEY_RIGHT:
				self.right_pressed()
			if k == tg.keyboard.KEY_ESCAPE:
				self.done = True
				self.exit = True
			x, y = self.player.x, self.player.y
			if self.board.data[x, y] == 'X': self.done = True

			

	def load_level(self):
		board_data = tg.character_map.load("examples/data/dringle/level" + str(self.level) + ".txt")
		self.board = Board(board_data)


def main():
	"""
	The main entrypoint to the Dringle game. It initializes librarys including tinygame and creates the Game UI
	"""
	tg.initialize()
	try:
		gameui = DringleUI()
		while True:
			gameui.play_round()
			if gameui.exit: break
			gameui.level += 1

	finally:
		tg.quit()

if __name__ == "__main__":
	main()
