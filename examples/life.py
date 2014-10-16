"""
Life - John Conway's Game of Life

A tinygame implementation of the famous life cellular automata simulation.
Rules for implementation found from here: http://en.wikipedia.org/wiki/Conway%27s_life
"""
import sys
sys.path.extend(['.', '..'])
import tinygame as tg

DEFAULT_START = """
                                                                            





                                #
                              # #
                    ##      ##            ##
                   #   #    ##            ##
        ##        #     #   ##
        ##        #   # ##    # #
                  #     #       #
                   #   #
                    ##








"""

def main(args):
	"""
	The entrypoint to this game of life simulation. It is a non-interactive cellular automaton so the user simply sits back and watches.

	One optional command line argument supplies a file containing a character map of ' ' and '#' as an initial cell state. A default start is provided inside this module.

	args: command line argument list. Should be empty or exactly one string representing the path to a character map
	"""
	if len(args) not in [0,1]: # validate command line arguments
		print "Usage: python life.py [startmap.txt]"
		return

	tg.initialize()
	try:

		timer = tg.Metronome(1.0/7) # continue at 5 frames per second
		start = tg.character_map.parse(DEFAULT_START) # load the default map
		if len(args) == 1: start = tg.character_map.load(args[0]) # optionally load specified start maps
		screen = tg.character_display.CharacterDisplay(start.width, start.height) # create a screen of the board size to display stuff

		prev = tg.character_map.CharacterMap(screen.width, screen.height) # we store the previous
		next = prev.clone() # and next state in two successive maps

		prev.draw(0, 0, start)

		while True:
			k = tg.keyboard.getch() # this will return a character from the keyboard if one is pressed otherwise None
			if k == tg.keyboard.ESCAPE:
				break # go until a user presses escape key

			for y in xrange(0, prev.height):
				for x in xrange(0, prev.width):
					n = [(xo,yo) for (xo,yo) in [(-1, -1), (0, -1), (1,-1), (-1, 0), (1, 0), (-1,1), (0, 1), (1,1)] if prev[(x+xo)%prev.width,(y+yo)%prev.height] == '#']
					if prev[x,y] == '#':
						if len(n) < 2: next[x,y] = ' ' # cell dies from under-population
						elif len(n) in [2,3]: next[x, y] = '#' # it lives on with just the right density
						else: next[x,y] = ' ' # dies of overcrowding
					else:
						if len(n) == 3: next[x,y] = '#' # is born from reproduction
						else: next[x,y] = ' ' # no new generation
						
			screen.draw(0, 0, next)
			prev, next = next, prev # switch the next to the new previous
			timer.wait_for_tick() # wait until the 1.0/10 second tick happens
			screen.show()
	finally:
		tg.quit()

if __name__ == "__main__":
	main(sys.argv[1:])
