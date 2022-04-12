from colorama import Fore, Back, Style, init
init()

from os import system
from time import sleep, time
import math
import random 

from input import input_to
from troop import Troop

arch_range = 3
class Archer():
    def __init__(self, x, y, id, width, height, max_health, health, li_pix, og_pix, pixel, speed, attack, type):
            
        self.range = arch_range
        Troop.__init__(self, x, y, id, width, height, max_health, health, li_pix, og_pix, pixel, speed, attack, type)

    def move_and_attack(self, vill):
        m_dist = vill.rows + vill.cols
        tar_id = -1
        for b in vill.buildings:
            if b.id > vill.num_huts + 1 + vill.num_wiz:
                break
            
            if abs(self.x - b.x) + abs(self.y - b.y) < m_dist:
                m_dist = abs(self.x - b.x) + abs(self.y - b.y)
                m_x = b.x
                m_y = b.y
                tar_id = b.id

        for c in vill.cannons:
            if abs(self.x - c.x) + abs(self.y - c.y) < m_dist:
                m_dist = abs(self.x - c.x) + abs(self.y - c.y)
                m_x = c.x
                m_y = c.y
                tar_id = c.id
        
        if tar_id == -1:
            return 0

        is_att = False
        # right movement
        if m_x > self.x:           
            for sp in range(self.speed):
                if m_x > self.x:
                    for i in range(self.range):
                        if self.x + self.width + i + 1 < vill.cols and vill.grid[self.y][self.x + i + 1] == tar_id:
                            is_att = True
                            break

                    for h in range(self.height):                          
                        if vill.grid[self.y + h][self.x + self.width] != 0 and is_att == False:
                            return Troop.deal_damage(self, vill, vill.grid[self.y + h][self.x + self.width]) 
                        elif vill.grid[self.y + h][self.x + self.width] != 0 and is_att == True:
                            return Troop.deal_damage(self, vill, tar_id)                            
                    self.x += 1
                else:
                    return 0

        # left movement
        elif m_x < self.x:
            for sp in range(self.speed):
                if m_x < self.x:
                    for i in range(self.range):
                        if self.x - i - 1 >= 0 and vill.grid[self.y][self.x - i - 1] == tar_id:
                            is_att = True
                            break

                    for h in range(self.height):
                        if vill.grid[self.y + h][self.x - 1] != 0 and is_att == False:
                            return Troop.deal_damage(self, vill, vill.grid[self.y + h][self.x - 1])
                        elif vill.grid[self.y + h][self.x - 1] != 0 and is_att == True:
                            return Troop.deal_damage(self, vill, tar_id)
                    self.x -= 1
                else:
                    return 0

        # up movement
        elif m_y > self.y:
            for sp in range(self.speed):
                if m_y > self.y:
                    for i in range(self.range):
                        if self.y + self.height + i + 1 < vill.rows and vill.grid[self.y + i + 1][self.x] == tar_id:
                            is_att = True
                            break
                    
                    for w in range(self.width):
                        if vill.grid[self.y + self.height][self.x + w] != 0 and is_att == False:
                            return Troop.deal_damage(self, vill, vill.grid[self.y + self.height][self.x + w])
                        if vill.grid[self.y + self.height][self.x + w] != 0 and is_att == True:                            
                            return Troop.deal_damage(self, vill, tar_id)                        
                    self.y += 1
                else:
                    return 0

        # down movement
        elif m_y < self.y:
            for sp in range(self.speed):
                if m_y < self.y:
                    for i in range(self.range):
                        if self.y - i - 1 >= 0 and vill.grid[self.y - i - 1][self.x] == tar_id:
                            is_att = True
                            break

                    for w in range(self.width):
                        if vill.grid[self.y - 1][self.x + w] != 0 and is_att == False:
                            return Troop.deal_damage(self, vill, vill.grid[self.y - 1][self.x + w])
                        elif vill.grid[self.y - 1][self.x + w] != 0 and is_att == True:
                            return Troop.deal_damage(self, vill, tar_id)
                    self.y -= 1
                else:
                    return 0
        
        if is_att == True:
            return Troop.deal_damage(self, vill, tar_id)
        return 0

    def take_damage(self, amount, vill):
        Troop.take_damage(self, amount, vill)