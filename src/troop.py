from colorama import Fore, Back, Style, init
init()

from os import system
from time import sleep, time
import math
import random 

from input import input_to

class Troop():
    
    def __init__(self, x, y, id, width, height, max_health, health, pixel, speed, attack):
        self.id = id
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.max_health = max_health
        self.health = health

        self.pixel = pixel
        self.speed = speed
        self.attack = attack


    def update_position(self, x, y):
        self.x = x
        self.y = y   

    def rage(self, vill):
        self.attack *= 2
        self.speed *= 2
    
    def heal(self, vill):
        self.health += self.health//2
        if self.health > self.max_health:
            self.health = self.max_health

    def take_damage(self, amount, vill):
        self.health -= amount

        if self.health <= 0:
            self.health = 0 
            self.pixel = Back.BLACK + ' ' + Style.RESET_ALL 
            if id != vill.king.id:           
                vill.rm_troop(self.id)
        else:
            if self.health <= self.max_health//2:
                self.pixel = Back.LIGHTBLUE_EX + ' ' + Style.RESET_ALL
        # self.pixel = Back.YELLOW + Fore.BLACK + ' ' + Style.RESET_ALL
                