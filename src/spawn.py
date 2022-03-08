from colorama import Fore, Back, Style, init
init()

from os import system
from time import sleep, time
import math

class Spawn_pt():

    def __init__(self, tuple):
        self.x, self.y = tuple
        self.pixel = Back.CYAN + ' ' + Style.RESET_ALL

        self.width  = 2
        self.height = 1