from colorama import Fore, Back, Style, init
init()

from os import system
from time import sleep, time
import math
import random 

class Building():
    def __init__(self, x, y, id, width, height, pixel, max_health, health):
        self.id = id
        
        # location
        self.x = x
        self.y = y

        # dimensions
        self.width = width
        self.height = height

        # color
        self.pixel = pixel

        # properties
        self.max_health = max_health
        self.health = health
        
