from colorama import Fore, Back, Style, init
init()

from os import system
from time import sleep, time
import math

from colorama import Fore, Back, Style, init
init()

from os import system
from time import sleep, time
import math
import random 

import sys
sys.path.insert(0, './src')
from building import Building 

class THall(Building):
    
    def __init__(self, x, y, id):
        Building.__init__(self, x, y, id, 3, 4, Back.GREEN + ' ' + Style.RESET_ALL, 100, 100)

        # self.id = 1

        # dimensions of town hall
        # self.width  = 3
        # self.height = 4

        # color of town hall
        # self.pixel = Back.GREEN + ' ' + Style.RESET_ALL

        # properties of town_hall
        # self.max_health = 100
        # self.health = self.max_health

    
