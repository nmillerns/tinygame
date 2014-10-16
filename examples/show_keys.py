#!/usr/bin/python
import sys
sys.path.extend(['.', '..'])
import tinygame as tg

tg.initialize()

try:
	screen = tg.character_display.CharacterDisplay(80, 10) # create a small 40x30 screen to display stuff
	k = ""

	while True:
		if k != None:
			if k == "q": break
			screen.fill(' ')
			screen.write_text( 2, 5, "Key code: " + str([ord(c) for c in k]))
			screen.show()
		k = tg.keyboard.getch() 

finally:
	tg.quit()

