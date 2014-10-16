#!/usr/bin/python
import sys
sys.path.extend(['.', '..'])
import tinygame as tg

def main():
	tg.initialize()
	try:
		screen = tg.character_display.CharacterDisplay(40, 30) # create a small 40x30 screen to display stuff
		screen.write_text(5, 10, "Hello, World!") # write Hello World! around the middle of the display. This is hello world afterall
		timer = tg.Metronome(1.0/10) # continue at 10 frames per second
		while True:
			k = tg.keyboard.getch() # this will return a character from the keyboard if one is pressed otherwise None		
			if k != None:
				break # go until a user presses a key

			screen.scroll_left() # keep scrolling the display left (it loops around)
			timer.wait_for_tick() # wait until the 1.0/10 second tick happens
			screen.show() # show the next frame
	finally:
		tg.quit()

if __name__ == "__main__":
	main()
