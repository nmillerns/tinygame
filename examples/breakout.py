import sys
import random
sys.path.append('.')
import tinygame as tg

class Paddle():
	"""
	"""
	def __init__(self, x, y, width):
		self.x = x
		self.y = y
		self.width = width
		self.appearance = ''.join(['=' for i in xrange(0, self.width)])
	def draw(self, character_map):
		"""
		"""
		character_map.write_text(self.x - self.width / 2, self.y, self.appearance)

class FallingBrick():
	"""
	"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def draw(self, character_map):
		"""
		"""
		iy = int(round(self.y))
		if iy < character_map.height:
			if  character_map[self.x, iy] == '=': hit = True
			character_map[self.x, iy] = '"'

	def tick(self, character_map):
		self.y += .1 + 1.3*random.random()
		hit = False
		iy = int(self.y)
		if iy < character_map.height and character_map[self.x, iy] == '=': hit = True
		return hit

def sign(x):
	return -1 if x < 0 else 1

class Ball():
	"""
	"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.stuck = True
	def tick(self, character_map):
		if self.stuck: return
		hit = None
		x1 = self.x + self.dx
		y1 = self.y + self.dy
		bounce_horizontal = False
		bounce_vertical = False

		if self.dx != 0:
			ix = int(round(x1 + 0.5*sign(self.dx)))
			iy = int(round(y1))
			if character_map[ix, iy] not in [' ', None]:
				if character_map[ix, iy] == '#': hit = (ix, iy)
				bounce_horizontal = True

		if self.dy != 0:
			ix = int(round(x1))
			iy = int(round(y1 + 0.5*sign(self.dy)))
			if character_map[ix, iy] not in [' ', None]:
				if character_map[ix, iy] == '#': hit = (ix, iy)
				bounce_vertical = True
		if bounce_horizontal and bounce_vertical:
			ix = int(round(x1 + 0.5*sign(self.dx)))
			iy = int(round(y1 + 0.5*sign(self.dy)))
			if abs(ix - self.x) > abs(iy - self.y): bounce_horizontal = False
			else: bounce_vertical = False

		if bounce_horizontal:
			x1 = self.x
			self.dx *= -1
		if bounce_vertical:
			y1 = self.y
			self.dy *= -1

		self.x, self.y = x1, y1
		return hit

	def draw(self, character_map):
		"""
		"""
		character_map[int(round(self.x)), int(round(self.y))] = 'O'

class BreakoutGameUI():
	background_string = """
 ______________________________________________________________________________ 
|                                                                              |
|      ##################################################################      |
|                                                                              |
|                                                                              |
|  ##########################################################################  |
|                                                                              |
|                                                                              |
|##############################################################################|
|##############################################################################|
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
|                                                                              |
"""
	def __init__(self):
		self.screen = tg.character_display.CharacterDisplay(80, 24)
		self.done = False
		self.bg = tg.character_map.parse(BreakoutGameUI.background_string)
		self.total_bricks = len([1 for c in BreakoutGameUI.background_string if c == '#'])
		self.score = 0
		self.lives = 5
		self.highscore = tg.HighScoresGUI(tg.HighScoresDB("examples/data/breakout/scores.txt"))

	def show_stats(self):
		self.screen.fill(' ')
		self.screen.write_text(30, 10, "Lives: " + str(self.lives) )
		self.screen.show()
		tg.time.sleep(1.5)
		tg.keyboard.getch(1.0)

	def intro(self):

		try:
			title_card = """
################################################################################
##                                                                            ##
##                                                                            ##
##                                                                            ##
##                                                                            ##
##                                                                            ##
##                 ______ ___         _____ __        ____ __                 ##
##                _______/ _ )_______ ___ _/ /_____  __ __/ /_                ##
##               ______ / _  / __/ -_) _ `/  '_/ _ \/ // / __/                ##
##            ________ /____/_/__\__/\_,_/_/\_\-___/\_,_/\__/                 ##
##               ___________ _ _ _  __ _ _   __   __  _                       ##
##                                                                            ##
##                                                                            ##
##                                                                            ##
##                                                                            ##
##                                                                            ##
##                                                                            ##
##                                                    Presented in            ##
##                                                        tinygame            ##
##                                                                            ##
##                           Nick Miller 2013                                 ##
################################################################################
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
		self.screen.fill(' ')
		self.screen.write_text(30, 10, "Game Over!")
		self.screen.show()
		tg.time.sleep(1.5)
		tg.keyboard.getch(1.0)
		
	def show_win(self):
		self.screen.fill(' ')
		self.screen.write_text(30, 10, "You Win!\nCongratulations!")
		self.screen.show()
		tg.time.sleep(1.5)
		tg.keyboard.getch(1.0)

	def play_round(self):
		paddle = Paddle(40, 23, 6)
		ball = Ball(5.0, 22.0)
		metronome = tg.Metronome(1/30.0)
		ball.dx, ball.dy = .45, -.3
		falling = []
		while True:
			k = tg.keyboard.getch(1/30.0)
			if k == tg.keyboard.KEY_LEFT:
				paddle.x -= 1
			if k == tg.keyboard.KEY_RIGHT:
				paddle.x += 1
			if k == ' ' and ball.stuck:
				ball.stuck = False
			if k == tg.keyboard.KEY_ESCAPE:
				self.done = True
				break
			if paddle.x - paddle.width/2 < 1: paddle.x = 1 + paddle.width/2
			if paddle.x + paddle.width/2 > self.screen.width - 1: paddle.x = self.screen.width - 1 - paddle.width/2

			self.screen.draw(0, 0, self.bg)
			
			paddle.draw(self.screen)
			hit = ball.tick(self.screen)
			if ball.stuck: ball.x = paddle.x
			if hit != None:
				self.total_bricks -= 1
				self.score += 10
				x, y = hit
				self.bg[x,y] = ' '
				falling.append(FallingBrick(x,y))

			self.screen.write_text(5, 0, "Score: " + str(self.score))
			self.screen.write_text(70,0, "Lives: " + str(self.total_bricks))
			for f in falling:
				if f.tick(self.screen): self.score += 15
				f.draw(self.screen)
			falling = [f for f in falling if f.y < self.screen.height]

			if int(round(ball.y)) >= self.screen.height + 5:
				self.lives -= 1
				break
			ball.draw(self.screen)
			metronome.wait_for_tick()
			self.screen.show()

	def finalize(self):
		self.highscore.handle_new_score(self.score, self.screen)


def main():
	"""
	The main entrypoint to the Breakout game. It initializes librarys including tinygame and creates the Game UI
	"""
	tg.initialize()
	try:
		gameui = BreakoutGameUI()
		gameui.intro()
		while not gameui.done:
			gameui.show_stats()
			gameui.play_round()
			if gameui.lives < 1:
				gameui.show_gameover()
				gameui.done = True

		gameui.finalize()

	finally:
		tg.quit()

if __name__ == "__main__":
	main()
