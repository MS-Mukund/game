from colorama import Fore, Back, Style, init
init()

from os import system
from time import sleep, time
import math
import random 

from input import input_to

class Troop():
    
    def __init__(self, x, y, id, width, height, max_health, health, pixel):
        self.id = id
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.max_health = max_health
        self.health = health

        self.pixel = pixel


    def update_position(self, x, y):
        self.x = x
        self.y = y   

    def take_damage(self, amount):
        print("inside")
        self.health -= amount
        print(self.health)

        if self.health <= 0:
            print("hi")
            self.health = 0 
            self.pixel = Back.BLACK + ' ' + Style.RESET_ALL            
        else:
            if self.health <= self.max_health//2:
                print("hello")
                self.pixel = Back.LIGHTBLUE_EX + ' ' + Style.RESET_ALL
        # self.pixel = Back.YELLOW + Fore.BLACK + ' ' + Style.RESET_ALL
                