import sys
sys.path.append('.')
import tinygame as tg

tg.initialize()
try:
	screen = tg.character_display.CharacterDisplay(40, 20)
	cmap = tg.character_map.load(sys.argv[1])
	x, y = 0, 0
	while True:
		k = tg.keyboard.getch(1/10.0)
		if k == tg.keyboard.KEY_LEFT:
			x -= 1
		if k == tg.keyboard.KEY_RIGHT:
			x += 1
		if k == tg.keyboard.KEY_UP:
			y -= 1
		if k == tg.keyboard.KEY_DOWN:
			y += 1
		if k == tg.keyboard.KEY_ESCAPE:
			break
		screen.fill(' ')
		screen.draw(20-x, 10-y, cmap)
		screen.show()

finally:
	tg.quit()
