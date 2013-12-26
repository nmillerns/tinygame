"""
keyboard
A submodule inside tinygame that provides more game like keyboard input
This code is based largley on the post at http://effbot.org/pyfaq/how-do-i-get-a-single-keypress-at-a-time.htm
"""
# to get game keyboard control, first we load some low level operating system modules/libraries for terminal control 
import termios	# module get and set terminal attributes
import fcntl	# module to manipulate a file descriptor (ie the standard input file descriptor)
import sys, os	# opersting system wrapper module
import select	# a module exposing the lowleve select() call which allows a program to monitor multiple file  descriptors,  waiting  until  one or more of the file descriptors become "ready" for some class of I/O operation (e.g., input possible).

from character_display import ESCAPE, CSI # we read ANSI escape sequences for special keys similar to printing them for display. See character_display.py

KEY_ESCAPE = ESCAPE
KEY_TAB = chr(9)
KEY_ENTER = chr(10)
KEY_DELETE = CSI + "3~"
KEY_UP = CSI + "A"
KEY_DOWN = CSI + "B"
KEY_RIGHT = CSI + "C"
KEY_LEFT = CSI + "D"
KEY_BACKSPACE = chr(127)

def initialize():
	"""
	Initializes the keyboard submodule. 

	This is important since we need to change the mode of the keyboard attributes to read non-blocking etc
	"""
	# since there is only one keyboard we store keyboard in these global variables
	global __keyboard_file_descriptor # the filedesciptor of standard in (keyboard)
	global __old_attributes # we store the attributes at start-up so we can restore them when we leave
	global __old_flags # same for flags

	__keyboard_file_descriptor = sys.stdin.fileno() # assign the filedescriptor to standard in

	__old_attributes = termios.tcgetattr(__keyboard_file_descriptor) # read the old attributes
	__new_attributes = __old_attributes[:] # make a copy of the attributes using the slice operator for list copy
	__new_attributes[3] = __new_attributes[3] & ~termios.ICANON & ~termios.ECHO # turn off canonical mode and character echo for the keyboard
	termios.tcsetattr(__keyboard_file_descriptor, termios.TCSANOW, __new_attributes) # commit the changed attributes

	__old_flags = fcntl.fcntl(__keyboard_file_descriptor, fcntl.F_GETFL) # get the old flags
	fcntl.fcntl(__keyboard_file_descriptor, fcntl.F_SETFL, __old_flags | os.O_NONBLOCK) # turn off non-blocking mode. IMPORTANT! This will allow us to check for keyboard input but continue handling the game without waiting for user input

def getch(timeout = 0):
	"""
	Reads one most resent key hit by the user.

	Styled after the getch() function in <conio.h> in C
	It is a nonblocking call to read the keyboard. You call it and wait for a maximum amount of time for a key press. If a key has already been pressed it returns immediately.
	The name can be misleading sinc key hits are sometimes escape sequences containing several characters. eg ESC[A is the Up key. Nevertheless the most recent full key character string is returned

	timeout: a floating point value representing the maximum amount of time (in second units) to wait for a key press. If it is 0, the function returns immediately and reports the most recent key
	return: a string representing the key pressed may be None if no key was pressed. eg 'x' for the x key or 'ESC[A' for the up arrow key
	"""
	# since there is only one keyboard we store keyboard in these global variables
	global __keyboard_file_descriptor # the filedesciptor of standard input (keyboard)

	r, w, e = select.select([__keyboard_file_descriptor], [], [], timeout) # wait at most timeout for reads to be available on standard input
	if r: # check if it returned because input is available
		q = sys.stdin.read() # if so read a key from standard in
		tokens = q.split(CSI) # get escape sequences
		if len(tokens) == 1: # check if there is no escape sequence
			return tokens[0] # if so simply return the key
		else:
			return CSI + tokens[-1] # otherwise return only the most recent escape sequence
	return None # no input

def quit():
	"""
	De-initializes the keyboard module. This is important since we need to restore the keyboard attributes
	"""
	# since there is only one keyboard we store keyboard in these global variables
	global __keyboard_file_descriptor # the filedesciptor of standard in (keyboard)
	global __old_attributes # we store the attributes at start-up so we can restore them when we leave
	global __old_flags # same for flags

	termios.tcsetattr(__keyboard_file_descriptor, termios.TCSAFLUSH, __old_attributes) # resture the keyboard attributes from before we started
	fcntl.fcntl(__keyboard_file_descriptor, fcntl.F_SETFL, __old_flags) # same for the flags
	#everything should be back to normal

