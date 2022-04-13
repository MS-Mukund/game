from troop import Troop
from input import input_to
from time import sleep, time
from os import system
from colorama import Fore, Back, Style, init
from sqlalchemy import false

from building import Building
init()


class King():

    def __init__(self, x, y, type):

        id = 1
        width, height = 2, 2
        max_h = 100

        li_pix = Back.LIGHTBLUE_EX + Style.BRIGHT + ' ' + Style.RESET_ALL
        pixel = Back.BLUE + Style.BRIGHT + ' ' + Style.RESET_ALL
        speed = 2
        attack = 10

        self.iteration = 0
        if type == 'queen':
            attack = 8

        Troop.__init__(self, x, y, id, width, height, max_h,
                       max_h, li_pix, pixel, pixel, speed, attack, type)

    def change_to_queen(self):
        self.attack = 8
        self.tr_type = 'queen'

    def v_attack(self, vill, prev_move):

        if self.tr_type == 'king':
            ids = set([])

        # if len(ids) == 0:
            for w in range(self.width):
                if vill.grid[self.y - 1][self.x + w] != 0:
                    ids.add(vill.grid[self.y - 1][self.x + w])

        # if len(ids) == 0:
            for w in range(self.width):
                if vill.grid[self.y + self.height][self.x + w] != 0:
                    ids.add(vill.grid[self.y + self.height][self.x + w])

        # if len(ids) == 0:
            for h in range(self.height):
                if vill.grid[self.y + h][self.x + self.width] != 0:
                    ids.add(vill.grid[self.y + h][self.x + self.width])

        # if len(ids) == 0:
            for h in range(self.height):
                if vill.grid[self.y + h][self.x - 1] != 0:
                    ids.add(vill.grid[self.y + h][self.x - 1])

            for id in ids:
                for b in vill.buildings:
                    if(b.id == id):
                        value = b.reduce_health(self.attack)

                        if value == True:
                            vill.rm_build(b)  

            if len(vill.buildings) == 0 or ( vill.buildings[0].id > 6 and vill.num_cannons <= 0 ): 
                return 1        # 1 indicates victory

            return 0
                
            
        else:
            ids = set([])
            sign = 1
            if prev_move < 0:
                sign = -1
            # scan a 5 tile radius around the queen
            for i in range(self.y - sign * ( abs(prev_move) % 2)*8  - 5, self.y - sign * ( abs(prev_move) % 2)*8 + 6):
                for j in range(self.x + sign * ( abs(prev_move) // 2)*8 - 5, self.x + sign * ( abs(prev_move) // 2)*8 + 6):
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
        if vill.raged == False:
            Troop.rage(self, vill)
            vill.raged = True             
        
    def heal(self, vill):
        if vill.healed == False:
            Troop.heal(self, vill)
            vill.healed = True

    def eagle_att(self, vill, prev_move):
        ids = set([])
        # scan a 9 tile radius around the queen
        for i in range(self.y + (prev_move % 2)*16  - 9, self.y + (prev_move % 2)*16 + 10):
            for j in range(self.x + (prev_move // 2)*16 - 9, self.x + (prev_move // 2)*16 + 10):
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

    def move(self, vill):
        char = input_to()
        if vill.is_king == -1:
            if char == None:
                return
            elif str(char).lower() == 'q':
                vill.is_king = 0
                self.change_to_queen()
            else:
                vill.is_king = 1
            
            # print(str(char), vill.is_king)
            # exit()
            return 0        

        if(char == 'd'):   
            vill.prev_move = 2         
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
            vill.prev_move = -2
            for sp in range(self.speed):
                if self.x > 0:
                    for h in range(self.height):
                        if vill.grid[self.y + h][self.x - 1] != 0:
                            return

                    self.x -= 1

        elif(char == 's'):
            vill.prev_move = -1
            for sp in range(self.speed):
                if( self.y + self.height < vill.rows ):
                    for w in range(self.width):
                        if vill.grid[self.y + self.height][self.x + w] != 0:
                            return

                    self.y += 1

        elif(char == 'w'):
            vill.prev_move = 1
            for sp in range(self.speed):
                if self.y > 0:
                    for w in range(self.width):
                        if vill.grid[self.y - 1][self.x + w] != 0:
                            return

                    self.y -= 1
        
        elif(char == ' '):
            vill.game_end = self.v_attack(vill, vill.prev_move)

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
        
        elif char == 'e':
            if self.tr_type == 'queen':
                self.eagle_att(vill, vill.prev_move)

        return char    
