from colorama import Fore, Back, Style, init
init()

from os import system
from time import sleep, time
import math
import random 

import sys
sys.path.insert(0, './src')
from building import Building 

class Hut(Building):
    
    def __init__(self, tuple):
        x, y, id = tuple
        Building.__init__(self, x, y, id, 3, 2, Back.GREEN + ' ' + Style.RESET_ALL, 40, 40)
        
        # dimensions of hut
        # self.width  = 3
        # self.height = 2

        # color of hut
        # self.pixel = Back.GREEN + ' ' + Style.RESET_ALL

        # properties of hut
        # self.max_health = 40
        # self.health = self.max_health

    
