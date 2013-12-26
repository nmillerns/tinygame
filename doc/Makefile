EXAMPLES:=doc/snake.html doc/tetris.html doc/breakout.html doc/life.html

all:	doc/tinygame.html $(EXAMPLES)

doc/tinygame.html: doc/tinygame.keyboard.html doc/tinygame.character_map.html doc/tinygame.character_display.html
	pydoc -w tinygame
	sed 's|$(PWD)|..|g' < tinygame.html > doc/tinygame.html
	rm tinygame.html

doc/tinygame.keyboard.html: doc/fcntl.html doc/select.html doc/termios.html doc/os.html doc/sys.html
	pydoc -w tinygame.keyboard
	sed 's|$(PWD)|..|g'  < tinygame.keyboard.html > doc/tinygame.keyboard.html
	rm tinygame.keyboard.html

doc/tinygame.character_map.html:
	pydoc -w tinygame.character_map
	sed 's|$(PWD)|..|g'  < tinygame.character_map.html > doc/tinygame.character_map.html
	rm tinygame.character_map.html

doc/tinygame.character_display.html:
	pydoc -w tinygame.character_display
	sed 's|$(PWD)|..|g'  < tinygame.character_display.html > doc/tinygame.character_display.html
	rm tinygame.character_display.html

doc/tetris.html: doc/random.html doc/copy.html
	pydoc -w examples/tetris.py
	sed 's|$(PWD)|..|g' < tetris.html > doc/tetris.html
	rm tetris.html

doc/breakout.html: doc/random.html
	pydoc -w examples/breakout.py
	sed 's|$(PWD)|..|g' < breakout.html > doc/breakout.html
	rm breakout.html

doc/%.html: examples/%.py
	pydoc -w  $<
	sed 's|$(PWD)|..|g' < $*.html > $@
	rm $*.html

doc/fcntl.html:
	pydoc -w fcntl
	mv fcntl.html doc

doc/os.html:
	pydoc -w os
	mv os.html doc

doc/sys.html:
	pydoc -w sys
	mv sys.html doc

doc/termios.html:
	pydoc -w termios
	mv termios.html doc

doc/select.html:
	pydoc -w select
	mv select.html doc
	
doc/random.html:
	pydoc -w random
	mv random.html doc

doc/copy.html:
	pydoc -w copy
	mv copy.html doc

clean:
	-rm *.html
	-rm doc/*.html
