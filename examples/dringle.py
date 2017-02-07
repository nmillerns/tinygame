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

	def can_go_up(self, x, y):
		y -= 1
		if y < 0: return False
		if self.data[x, y] == '#': return False
		if self.data[x, y] == '.': return True
		if self.data[x, y] == '0': return True
		if y < 1 or self.data[x, y - 1] != '.': return False
		return True

	def can_go_down(self, x, y):
		y += 1
		if y >= self.data.height: return False
		if self.data[x, y] == '#': return False
		if self.data[x, y] == '.': return True
		if self.data[x, y] == '0': return True
		if y >= self.data.height - 1 or self.data[x, y + 1] != '.': return False
		return True

	def can_go_left(self, x, y):
		x -= 1
		if x < 0: return False
		if self.data[x, y] == '#': return False
		if self.data[x, y] == '.': return True
		if self.data[x, y] == '0': return True
		if x < 1 or self.data[x - 1, y] != '.': return False
		return True

	def can_go_right(self, x, y):
		x += 1
		if x >= self.data.width: return False
		if self.data[x, y] == '#': return False
		if self.data[x, y] == '.': return True
		if self.data[x, y] == '0': return True
		if x >= self.data.width - 1 or self.data[x + 1, y] != '.': return False
		return True

	def eliminate_matches(self, x, y):
		target = self.data[x, y]
		if target == '#': return
		if y > 0 and self.data[x, y - 1] == target: 
			self.data[x, y] = '.'
			self.data[x, y - 1] = '.'
		if y < self.data.height - 1 and self.data[x, y + 1] == target: 
			self.data[x, y] = '.'
			self.data[x, y + 1] = '.'

		if x > 0 and self.data[x - 1, y] == target: 
			self.data[x, y] = '.'
			self.data[x - 1, y] = '.'

		if x < self.data.width - 1 and self.data[x + 1, y] == target: 
			self.data[x, y] = '.'
			self.data[x + 1, y] = '.'

	def change(self, x, y):
		if y > 0 and self.data[x, y - 1] == '#': 
			self.data[x, y] = '#'
		if y < self.data.height - 1 and self.data[x, y + 1] == '#': 
			self.data[x, y] = '#'
		if x > 0 and self.data[x - 1, y] == '#': 
			self.data[x, y] = '#'
		if x < self.data.width - 1 and self.data[x + 1, y] == '#': 
			self.data[x, y] = '#'


class DringleUI():
	def __init__(self):
		self.level = 0
		self.board = None
		self.player = None
		self.screen = tg.character_display.CharacterDisplay(16, 8)
		self.done = False
		self.exit = False

	def up_pressed(self):
		self.player.image = Player.UP
		x, y = self.player.x, self.player.y
		if self.board.can_go_up(x, y): self.player.y -= 1
		x, y = self.player.x, self.player.y
		if self.board.data[x, y] not in ['.', '0']:
			self.board.data[x, y - 1] = self.board.data[x, y]
			self.board.data[x, y] = '.'
			self.board.change(x, y - 1)
			self.board.eliminate_matches(x, y - 1)

	def down_pressed(self):
		self.player.image = Player.DOWN
		x, y = self.player.x, self.player.y
		if self.board.can_go_down(x, y): self.player.y += 1
		x, y = self.player.x, self.player.y
		if self.board.data[x, y] not in ['.', '0']:
			self.board.data[x, y + 1] = self.board.data[x, y]
			self.board.data[x, y] = '.'
			self.board.change(x, y + 1)
			self.board.eliminate_matches(x, y + 1)

	def left_pressed(self):
		self.player.image = Player.LEFT
		x, y = self.player.x, self.player.y
		if self.board.can_go_left(x, y): self.player.x -= 1
		x, y = self.player.x, self.player.y
		if self.board.data[x, y] not in ['.', '0']:
			self.board.data[x - 1, y] = self.board.data[x, y]
			self.board.data[x, y] = '.'
			self.board.change(x - 1, y)
			self.board.eliminate_matches(x - 1, y)

	def right_pressed(self):
		self.player.image = Player.RIGHT
		x, y = self.player.x, self.player.y
		if self.board.can_go_right(x, y): self.player.x += 1
		x, y = self.player.x, self.player.y
		if self.board.data[x, y] not in ['.', '0']:
			self.board.data[x + 1, y] = self.board.data[x, y]
			self.board.data[x, y] = '.'
			self.board.change(x + 1, y)
			self.board.eliminate_matches(x + 1, y)

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
			if self.board.data[x, y] == '0': self.done = True

			

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
