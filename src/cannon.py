from colorama import Fore, Back, Style, init

from building import Building
init()

from os import system
from time import sleep, time
import math
import random 

wid = 1
ht = 2
pix = Back.MAGENTA + ' ' + Style.RESET_ALL
max_h = 50
h = 50
dam = 3
range = 6

class Cannon(Building):
    
    def __init__(self, tuple):
        self.x, self.y, self.id = tuple

        # dimensions of cannon
        self.wid    = wid
        self.ht     = ht

        # color of cannon
        self.pixel  = pix

        # properties of cannon
        self.damage = dam
        self.range  = range
        self.max_h  = max_h
        self.h      = h

        # self.target = None

        Building.__init__(self, tuple, wid, ht, pix, max_h, h, dam) 
    
    def deal_damage(self, vill):
    # targets closest troop in range

        min_d = range + 1
        index = -1
        for troop in vill.troops:
            dist = min( abs(troop.x - self.x), abs(troop.x + troop.width - self.x) ) + min( abs(troop.y - self.y), abs(troop.y + troop.height - self.y) )
            # print(dist)
            if(dist < min_d):
                min_d = dist
                index = troop.id
                # print(min_d, index)

        if(index != -1 and index != 1):
            for troop in vill.troops:
                if(troop.id == index):
                    troop.take_damage(self.damage, vill)
                    break
        
        elif index == 1:
            vill.king.take_damage(self.damage, vill)
        