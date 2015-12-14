import sys
import random
sys.path.extend(['.', '..'])
import tinygame as tg

class Paddle():
	"""
	Simple class for the user's paddle. It has a location and can draw itself onto any character map, in particular the screen
	"""
	def __init__(self, x, y, width):
		self.x = x # sets initial location
		self.y = y
		self.width = width # sets the width
		self.appearance = ''.join(['=' for i in xrange(0, self.width)]) # sets the appearance of the paddle as a sequence of ='s
	def draw(self, character_map):
		"""
		Draws the appearance of the paddle (a sequence of='s) on the given character map
		"""
		character_map.write_text(self.x - self.width / 2, self.y, self.appearance)

class FallingBrick():
	"""
	Class to handle the broken bricks that fall
	"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def draw(self, character_map):
		"""
		Draws a falling brick at its current location on the given character_map
		"""
		iy = int(round(self.y))
		if iy < character_map.height:
			character_map[self.x, iy] = '"'

	def tick(self, character_map):
		"""
		Tick a falling brick one frame... keeps falling and detects collision with the player paddle
		"""
		self.y += .1 + 1.3*random.random()
		hit = False
		int_y = int(self.y)
		if int_y < character_map.height and character_map[self.x, int_y] == '=': hit = True  # Check for collision with the paddle
		return hit

def sign(x):
	return -1 if x < 0 else 1

class Ball():
	"""
	The ball in breakout. Follows simple linear motion with perfectly elastic collisions
	"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.stuck = True
	def tick(self, character_map):
		if self.stuck: return
		hit = None  # for detecting collisions with solid surfaces in the play area
		next_x = self.x + self.dx
		next_y = self.y + self.dy
		bounce_horizontal = False
		bounce_vertical = False

		if self.dx != 0:
			# check the next positions on the playing grid for collisions
			ix = int(round(next_x + 0.5*sign(self.dx)))
			iy = int(round(next_y))
			if character_map[ix, iy] not in [' ', None]:
				if character_map[ix, iy] == '#': hit = (ix, iy)
				bounce_horizontal = True

		if self.dy != 0:
			# check the next positions on the playing grid for collisions
			ix = int(round(next_x))
			iy = int(round(next_y + 0.5*sign(self.dy)))
			if character_map[ix, iy] not in [' ', None]:
				if character_map[ix, iy] == '#': hit = (ix, iy)
				bounce_vertical = True
		if bounce_horizontal and bounce_vertical:
			# Choose between horizontal and vertical bounce based on which direction is faster
			ix = int(round(next_x + 0.5*sign(self.dx)))
			iy = int(round(next_y + 0.5*sign(self.dy)))
			if abs(ix - self.x) > abs(iy - self.y): bounce_horizontal = False
			else: bounce_vertical = False

		# reverse directions for perfectly elastic collisions
		if bounce_horizontal:
			next_x = self.x
			self.dx *= -1
		if bounce_vertical:
			next_y = self.y
			self.dy *= -1

		self.x, self.y = next_x, next_y
		return hit

	def draw(self, character_map):
		"""
		Draws an O for the ball
		"""
		character_map[int(round(self.x)), int(round(self.y))] = 'O'

class BreakoutGameUI():
	background_string = """\
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
		self.screen = tg.character_display.CharacterDisplay(80, 23)
		self.done = False
		self.bg = tg.character_map.parse(BreakoutGameUI.background_string)
		self.total_bricks = len([1 for c in BreakoutGameUI.background_string if c == '#'])
		self.score = 0
		self.lives = 10
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
				self.screen.draw_image(0, 0, cm)
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
		paddle = Paddle(40, 22, 8)
		ball = Ball(5.0, 21.0)
		metronome = tg.Metronome(1/30.0)
		ball.dx, ball.dy = .45, -.3
		falling_bricks = []
		while True:
			k = tg.keyboard.getch()
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

			self.screen.draw_image(0, 0, self.bg)
			
			paddle.draw(self.screen)
			hit = ball.tick(self.screen)
			if ball.stuck: ball.x = paddle.x  # The ball can travel with the paddle
			if hit != None:
				# Score a bick remove it from the background and replace it with a falling brick
				self.total_bricks -= 1
				self.score += 10
				x, y = hit
				self.bg[x,y] = ' '
				falling_bricks.append(FallingBrick(x,y))

			self.screen.write_text(5, 0, "Score: " + str(self.score))
			self.screen.write_text(68,0, "Bricks: " + str(self.total_bricks))
			for fbrick in falling_bricks:
				if fbrick.tick(self.screen): self.score += 15
				fbrick.draw(self.screen)
			falling_bricks = [f for f in falling_bricks if f.y < self.screen.height]

			if int(round(ball.y)) >= self.screen.height + 5:
				self.lives -= 1
				break
			ball.draw(self.screen)
			self.screen.show()
			metronome.wait_for_tick()

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
