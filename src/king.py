from colorama import Fore, Back, Style, init
init()

from os import system
from time import sleep, time
import math
import random 

from input import input_to

class King():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        # dimensions of king cell
        self.width = 2
        self.height = 2

        # color of king
        self.pixel = Back.BLUE + Style.BRIGHT + ' ' + Style.RESET_ALL

        # properties of king
        self.max_health = 100
        self.health = self.max_health

        self.attack = 10
        self.speed  = 2

    def update_position(self, x, y):
        self.x = x
        self.y = y

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
                    b.health -= self.attack
                    if(b.health <= 0):
                        vill.buildings.remove(b)
                        vill.grid[b.y][b.x] = 0
                        break

                        
        

    def move(self, vill):
        char = input_to()
        if(char == 'd'):
            if((self.x + self.width) <= (vill.cols - self.speed)): 
                for sp in range(self.speed): 
                    if vill.grid[self.y][self.x + self.width] == 0:
                        self.x += 1
                    else:
                        break
                
            elif((self.x + self.width) - vill.cols <= 0):   
                while( self.x < vill.cols - self.width):
                    if vill.grid[self.y][self.x + self.width] == 0:
                        self.x += 1
                    else:
                        break

        elif(char == 'a'):
            if(self.x >= self.speed):
                for sp in range(self.speed):
                    if vill.grid[self.y][self.x - self.width + 1] == 0:
                        self.x -= 1
                    else:
                        break
            elif (self.x >= 0):  
                while(self.x > 0):
                    if vill.grid[self.y][self.x - self.width + 1] == 0:
                        self.x -= 1
                    else:
                        break

        elif(char == 's'):
            if((self.y + self.height) <= (vill.rows-self.speed)):
                for sp in range(self.speed):
                    if vill.grid[self.y + self.height][self.x] == 0:
                        self.y += 1
                    else:
                        break
            elif((self.y + self.height) - vill.rows <= 0 ):  
                while( self.y < vill.rows - self.height):
                    if vill.grid[self.y + self.height][self.x] == 0:
                        self.y += 1
                    else:
                        break

        elif(char == 'w'):
            if(self.y >= self.speed):
                for sp in range(self.speed):
                    if vill.grid[self.y - self.height + 1][self.x] == 0:
                        self.y -= 1
                    else:
                        break
            elif (self.y >= 0): 
                while( self.y > 0):
                    if vill.grid[self.y - self.height + 1][self.x] == 0:
                        self.y -= 1
                    else:
                        break
        
        elif(char == ' '):
            self.v_attack(vill)

        elif(char == 'q'):
            print('Quitting...')
            exit()
    
        return char    
