#!/usr/bin/python
import sys
sys.path.extend(['.', '..'])
import tinygame as tg

def main():
    tg.initialize()
    try:
        level = tg.character_map.load("examples/data/ray_caster/square.txt")
        bg = tg.character_map.load("examples/data/ray_caster/bg.txt")
        screen = tg.character_display.CharacterDisplay(bg.width, bg.height)
        timer = tg.Metronome(1.0/25) # continue at 10 frames per second
	pos = (level.width/2/2.0, level.height/2.0)
	d = (0.01, 0.01)
	polygons = {}
	for y in xrange(0, level.height):
		for x2 in xrange(0, level.width, 2):
			x = x2/2
			first = level[x2,  y]
			second = level[x2+1, y]
			if first != ' ':
				index = ord(first) - ord('A')
				offset = ord(second) - ord('a')
				if index not in polygons.keys():
					polygons[index] = {}
				polygons[index][offset] = (x, y)

	walls = []				
	
	for i in polygons.keys():
		p = polygons[i]
		Q = []
		for j in sorted(p.keys()):
			x, y = p[j]
			Q.append((x, y))
		for j in xrange(0, len(Q)):
			walls.append((Q[j-1], Q[j]))

        while True:
            k = tg.keyboard.getch() # this will return a character from the keyboard if one is pressed otherwise None        
            if k == 'q':
                break # go until a user presses a key
            screen.draw_image(0, 0, bg)
            for u in xramge(0, screen.width):
            
            timer.wait_for_tick() # wait until the 1.0/10 second tick happens
            screen.show() # show the next frame
    finally:
        tg.quit()

if __name__ == "__main__":
    main()
