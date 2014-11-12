#!/usr/bin/python
import sys
sys.path.extend(['.', '..'])
import tinygame as tg

def main():
    tg.initialize()
    try:
        layer0 = tg.character_map.load("examples/data/paralax_scroll/bg.txt")
        layer1 = tg.character_map.load("examples/data/paralax_scroll/mid.txt")
        layer2 = tg.character_map.load("examples/data/paralax_scroll/fg.txt")
        screen = tg.character_display.CharacterDisplay(80, layer0.height)
        timer = tg.Metronome(1.0/25) # continue at 10 frames per second
        frame = 0
        while True:
            k = tg.keyboard.getch() # this will return a character from the keyboard if one is pressed otherwise None        
            if k != None:
                break # go until a user presses a key
            screen.draw(0, 0, layer0,'#')
            screen.draw(0, 0, layer1,'#')
            screen.draw(0, 0, layer2,'#')
            timer.wait_for_tick() # wait until the 1.0/10 second tick happens
            screen.show() # show the next frame
            frame += 1
            if frame % 3 == 0: layer1.scroll_left()
            if frame % 1 == 0: layer2.scroll_left()

    finally:
        tg.quit()

if __name__ == "__main__":
    main()
