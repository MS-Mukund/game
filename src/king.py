from colorama import Fore, Back, Style, init
from sqlalchemy import false

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
        
        id = 1
        width, height = 2, 2
        max_h = 100
        
        li_pix = Back.LIGHTBLUE_EX + Style.BRIGHT + ' ' + Style.RESET_ALL
        pixel = Back.BLUE + Style.BRIGHT + ' ' + Style.RESET_ALL
        speed = 2
        attack = 10
        
        Troop.__init__(self, x, y, id, width, height, max_h, max_h, li_pix, pixel, pixel, speed, attack, 'king')

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

        if len(vill.buildings) == 0 or ( vill.buildings[0].id > 6 and vill.num_cannons <= 0 ): 
            return 1        # 1 indicates victory

        return 0    

    def take_damage(self, amount, vill):
        Troop.take_damage(self, amount, vill)
        
        # update health bar color
        style = Back.GREEN + Fore.BLACK + ' ' + Style.RESET_ALL

        if(self.health <= 0):
            self.health = 0
            vill.bar_style = Back.YELLOW + Fore.YELLOW + ' ' + Style.RESET_ALL
            vill.rm_troop(self.id)
        else:
            if   self.health <= self.max_health//2 and self.health > self.max_health//5:
                vill.bar_style = Back.CYAN + Fore.BLACK + ' ' + Style.RESET_ALL
            elif self.health <= self.max_health//5:
                vill.bar_style = Back.RED + Fore.BLACK + ' ' + Style.RESET_ALL

    def rage(self, vill):
        if self.raged == False:
            Troop.rage(self, vill)
            self.raged = True             
        
    def heal(self, vill):
        if vill.healed == False:
            Troop.heal(self, vill)
            vill.healed = True

    def move(self, vill):
        char = input_to()
        if(char == 'd'):            
            for sp in range(self.speed):
                if(self.x + self.width < vill.cols):
                    for h in range(self.height):
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
                            return

                    self.y -= 1
        
        elif(char == ' '):
            vill.game_end = self.v_attack(vill)

        elif(char == 'q'):
            print('Quitting...')
            exit()

        elif(char == 'p'):
            print('Pausing...')
            system('clear')
            print(len(vill.buildings))
            sleep(1)

        # rage spell
        elif(char == 'r'):
            [ troop.rage(vill) for troop in vill.troops ]

        # heal spell
        elif(char == 'h'):
            [ troop.heal(vill) for troop in vill.troops ]
        
        # spawn barbarians
        elif char == '1' or char == '2' or char == '3':
            vill.add_barbs(int(char) - 1)

        # spawn archers 
        elif char == '4' or char == '5' or char == '6':
            vill.add_arch(int(char) - 4)
        
        # spawn balloons 
        elif char == '7' or char == '8' or char == '9':
            vill.add_ball(int(char) - 7)

        return char    
