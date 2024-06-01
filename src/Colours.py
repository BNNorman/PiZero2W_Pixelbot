# colour definitions
# can be included in PixelBot scripts

# you cannot use 'from Colours import *'
# to specify a single colour use 'from Colours import RED,MAGENTA'
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 150, 0)
PURPLE = (180, 0, 255)
MAGENTA=(255,0,255)
WHITE = (255, 255, 255)
BLACK = (0,0,0)

# to use a single import use 'from Colours import colour'
# then you can use colour.RED etc in your program
class colour:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    CYAN = (0, 255, 255)
    YELLOW = (255, 150, 0)
    PURPLE = (180, 0, 255)
    MAGENTA=(255,0,255)
    WHITE = (255, 255, 255)
    BLACK = (0,0,0)
    
# the following are convenience functions used by
# the neopixel functions
colourByLetter={
    "R":RED,
    "G":GREEN,
    "B":BLUE,
    "Y":YELLOW,
    "M":MAGENTA,
    "P":PURPLE,
    "C":CYAN,
    "W":WHITE,
    "K":BLACK
}

colourByName={
    "RED":RED,
    "GREEN":GREEN,
    "BLUE":BLUE,
    "CYAN":CYAN,
    "YELLOW":YELLOW,
    "MAGENTA":MAGENTA,
    "WHITE":WHITE,
    "BLACK":BLACK
    }

allNameColours=["RED","GREEN","BLUE","CYAN","MAGENTA","YELLOW","WHITE","BLACK"] 
allLetterColours=["R","G","B","C","M","Y","W","K"]


if __name__=="__main__":
    print(allNameColours)
    print(allLetterColours)
    
    print("colourByName",colourByName.keys())