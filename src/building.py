from colorama import Fore, Back, Style, init
init()

from os import system
from time import sleep, time
import math
import random 

class Building():
    def __init__(self, tuple, width, height, pixel, max_health, health):
        self.x, self.y, self.id = tuple

        # dimensions
        self.width = width
        self.height = height

        # color
        self.pixel = pixel

        # properties
        self.max_health = max_health
        self.health = health

    def reduce_health(self, amount):
        self.health -= amount
        
        if(self.health <= 0):
            self.health = 0

            return True            
        else:
            if   self.id <= 6 and self.health < self.max_health//2 and self.health >= self.max_health//5:
                self.pixel = Back.YELLOW + ' ' + Style.RESET_ALL
            elif self.id <= 6 and self.health < self.max_health//5:
                self.pixel = Back.RED    + ' ' + Style.RESET_ALL

            return False
