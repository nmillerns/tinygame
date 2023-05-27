import sys
import random
sys.path.extend(['.', '..'])
import tinygame as tg

class TileUI():
	def __init__(self):
		self.tileset = [
			tg.character_map.parse(	".===. " + "\n" + 
	                                		"|   ||" + "\n" +
	                                		"|___L|" ),
	                                		
			tg.character_map.parse(	"/++++#" + "\n" + 
	                                		"\++++/" + "\n" +
	                                		" |||| " ),

			tg.character_map.parse(	"  .  ." + "\n" + 
	                                		" : .  " + "\n" +
	                                		".  ., " ),

			tg.character_map.parse(	"~~~~~~" + "\n" + 
	                                		"~~~~~~" + "\n" +
	                                		"~~~~~~" )]
	                                		
		self.map = tg.character_map.parse(	"0000000000000000000000" + "\n" +
							"0111122222122211122110" + "\n" +
							"0112222222122221222210" + "\n" +
							"0222222122222222111110" + "\n" +
							"0222222000000000000000" + "\n" +
							"0222212000000000000000" + "\n" +
							"0221222002222222222222" + "\n" +
							"0222222002223322233333" + "\n" +
							"0221222002323333333333" + "\n" +
							"0222222002323333223333" + "\n" +
							"0112222002333333223333" + "\n" +
							"0112222002333333223233" + "\n" +
							"0112222002333333323333" + "\n" +
							"0112222002233333323333" + "\n" +
							"0112222002233333212333" + "\n" +
							"0111122002333332212233" + "\n" +
							"0112222002322322112233" + "\n" +
							"0112222002222333222223" + "\n" +
							"0112122002233333333333" + "\n" +
							"0112222002233333333333" + "\n" +
							"0112222002233332233333" + "\n" +
							"0112221002333333333333" + "\n" +
							"0111112002333333333333" + "\n" +
							"0000000002333332333333")

	def play(self):
		metronome = tg.Metronome(1/15) # Use a metronome to maintain specified fps

		tilemap = tg.character_map.CharacterMap(6*self.map.width, 3*self.map.height)
		for x in range(self.map.width):
			for y in range(self.map.height):
				src = int(self.map[x, y])
				
				tilemap.draw_image(6*x, 3*y, self.tileset[src])

		screen = tg.character_display.CharacterDisplay(6*8, 3*8)
		x, y = 0, 0
		dx, dy = 0, 0
		while True:
			k = tg.keyboard.getch() # Read key presses
			if k == tg.keyboard.KEY_ESCAPE:
				break
			if k == tg.keyboard.KEY_LEFT and x > 0:
				dx = -2
			elif k == tg.keyboard.KEY_RIGHT and x + screen.width < tilemap.width:
				dx = 2
			elif k == tg.keyboard.KEY_UP and y > 0:
				dy = -1
			elif k == tg.keyboard.KEY_DOWN and y + screen.height < tilemap.height:
				dy = 1
			else:
				if x % 6 == 0: dx = 0
				if y % 3 == 0: dy = 0
				
			if dx == -2: tilemap.scroll_right(2)
			if dx ==  2: tilemap.scroll_left(2)
			if dy == -1: tilemap.scroll_down()
			if dy == 1: tilemap.scroll_up()
			x += dx
			y += dy

			screen.draw_image(0, 0, tilemap)
			metronome.wait_for_tick()
			screen.show() # Update the display with the newest frame

		
def main():
	tg.initialize()
	try:
		gameui = TileUI()
		gameui.play() # simply start playing
	finally:
		tg.quit()

if __name__ == "__main__":
	main()
