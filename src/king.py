from colorama import Fore, Back, Style, init

from building import Building
init()

from os import system
from time import sleep, time
import math
import random 

from input import input_to

from troop import Troop

class King():
    
    def __init__(self, x, y):
        # self.x = x
        # self.y = y

        pixel = Back.BLUE + Style.BRIGHT + ' ' + Style.RESET_ALL
        Troop.__init__(self, x, y, 1, 2, 2, 100, 100, pixel)

        # dimensions of king cell
        # self.id = 1
        # self.width = 2
        # self.height = 2

        # color of king
        # self.pixel = Back.BLUE + Style.BRIGHT + ' ' + Style.RESET_ALL

        # properties of king
        # self.max_health = 100
        # self.health = self.max_health

        self.attack = 10
        self.speed  = 2

    def v_attack(self, vill):

        ids = set([])
        # scan a 5 tile radius around the king
        for i in range(self.y - 5, self.y + 6):
            for j in range(self.x - 5, self.x + 6):
                if(i >= 0 and j >= 0 and i < vill.rows and j < vill.cols):
                    if(vill.grid[i][j] != 0):
                        ids.add(vill.grid[i][j])
        
        # if there are any buildings in the radius, attack them
        for id in ids:
            for b in vill.buildings:
                if(b.id == id):
                    value = b.reduce_health(self.attack)
                    
                    if value == True:
                        vill.rm_build(b)      

    def take_damage(self, amount, vill):
        # print("yes")
        Troop.take_damage(self, amount)
        # print("now")
        
        # update health bar color
        style = Back.GREEN + Fore.BLACK + ' ' + Style.RESET_ALL

        if(self.health <= 0):
            self.health = 0
        else:
            # print("nani " + str(self.health))
            if   self.health <= self.max_health//2 and self.health > self.max_health//5:
                vill.bar_style = Back.CYAN + Fore.BLACK + ' ' + Style.RESET_ALL
            elif self.health <= self.max_health//5:
                vill.bar_style = Back.RED + Fore.BLACK + ' ' + Style.RESET_ALL

        # print("what")              
        

    def move(self, vill):
        char = input_to()
        if(char == 'd'):            
            for sp in range(self.speed):
                if(self.x + self.width < vill.cols):
                    for h in range(self.height):
                        # print( self.y + h, self.x + self.width)
                        if vill.grid[self.y + h][self.x + self.width] != 0:
                            return

                    self.x += 1

        elif(char == 'a'):
            # if self.x >= self.speed:
            #     for sp in range(self.speed):
            #         if vill.grid[self.y][self.x - self.width + 1] == 0:
            #             self.x -= 1
            #         else:
            #             break
            # elif (self.x >= 0):  
            #     while(self.x > 0):
            #         if vill.grid[self.y][self.x - self.width + 1] == 0:
            #             self.x -= 1
            #         else:
            #             break

            for sp in range(self.speed):
                if self.x > 0:
                    for h in range(self.height):
                        if vill.grid[self.y + h][self.x - 1] != 0:
                            return

                    self.x -= 1

        elif(char == 's'):
            for sp in range(self.speed):
                if( self.y + self.height < vill.rows ):
                    for w in range(self.width):
                        if vill.grid[self.y + self.height][self.x + w] != 0:
                            return

                    self.y += 1

        elif(char == 'w'):
            for sp in range(self.speed):
                if self.y > 0:
                    for w in range(self.width):
                        if vill.grid[self.y - 1][self.x + w] != 0:
                            # print(w, vill.grid[self.y - 1][self.x + w])
                            return

                    self.y -= 1
        
        elif(char == ' '):
            self.v_attack(vill)

        elif(char == 'q'):
            print('Quitting...')
            exit()
        
        # self.update_position(self, self.x, self.y)    
        return char    
