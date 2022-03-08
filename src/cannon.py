from colorama import Fore, Back, Style, init
init()

from os import system
from time import sleep, time
import math
import random 

import sys
sys.path.insert(0, './src')

class Cannon():
    
    def __init__(self, tuple):
        self.x, self.y = tuple

        # dimensions of cannon
        self.height = 2
        self.width  = 1

        # color of cannon
        self.pixel = Back.MAGENTA + ' ' + Style.RESET_ALL

        # properties of cannon
        self.damage = 25
        self.range  = 7

        
    

