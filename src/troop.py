from colorama import Fore, Back, Style, init
init()

from os import system
from time import sleep, time

class Troop():
    
    def __init__(self, x, y, id, width, height, max_health, health, li_pix, og_pix, pixel, speed, attack, type):
        self.id = id
        self.x = x
        self.y = y

        self.tr_type = type

        self.width = width
        self.height = height

        self.max_health = max_health
        self.health = health

        self.li_pix = li_pix
        self.og_pix = og_pix
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
        
        if self.health > self.max_health//2:
            self.pixel = self.og_pix    # restore original color

        if self.id == 1 and  self.health <= self.max_health//2 and self.health > self.max_health//5:
            vill.bar_style = Back.CYAN + ' ' + Style.RESET_ALL
        elif self.id == 1 and self.health > self.max_health//2:
            vill.bar_style = Back.GREEN + ' ' + Style.RESET_ALL

    def take_damage(self, amount, vill):
        self.health -= amount

        if self.health <= 0:
            self.health = 0 
            self.pixel = Back.BLACK + ' ' + Style.RESET_ALL 

            if id != vill.king.id:           
                vill.rm_troop(self.id)
        else:
            if self.health <= self.max_health//2:
                self.pixel = self.li_pix
        # self.pixel = Back.YELLOW + Fore.BLACK + ' ' + Style.RESET_ALL
    
    def deal_damage(self, vill, b_id):            
        for b in vill.buildings:
            if b.id == b_id:
                value = b.reduce_health(self.attack)
                
                if value == True:
                    vill.rm_build(b)  

        if len(vill.buildings) == 0 or ( vill.buildings[0].id > 6 and len(vill.cannons) <= 0 ): 
            return 1        # 1 indicates victory

        return 0

    def move_and_attack(self, vill):
        if self.tr_type == 'barb':
            m_dist = vill.rows + vill.cols
            for b in vill.buildings:
                if b.id > vill.num_huts + 1 + vill.num_wiz:
                    break
                
                if abs(self.x - b.x) + abs(self.y - b.y) < m_dist:
                    m_dist = abs(self.x - b.x) + abs(self.y - b.y)
                    m_x = b.x
                    m_y = b.y

            for c in vill.cannons:
                if abs(self.x - c.x) + abs(self.y - c.y) < m_dist:
                    m_dist = abs(self.x - c.x) + abs(self.y - c.y)
                    m_x = c.x
                    m_y = c.y

            # right movement
            if m_x > self.x:           
                for sp in range(self.speed):
                    if m_x > self.x:
                        for h in range(self.height):
                            if vill.grid[self.y + h][self.x + self.width] != 0:
                                return self.deal_damage(vill, vill.grid[self.y + h][self.x + self.width])                            
                        self.x += 1
                    else:
                        return 0

                return 0

            # left movement
            elif m_x < self.x:
                for sp in range(self.speed):
                    if m_x < self.x:
                        for h in range(self.height):
                            if vill.grid[self.y + h][self.x - 1] != 0:
                                return self.deal_damage(vill, vill.grid[self.y + h][self.x - 1])
                        self.x -= 1
                    else:
                        return 0
                return 0

            # up movement
            elif m_y > self.y:
                for sp in range(self.speed):
                    if m_y > self.y:
                        for w in range(self.width):
                            if vill.grid[self.y + self.height][self.x + w] != 0:
                                return self.deal_damage(vill, vill.grid[self.y + self.height][self.x + w])
                        self.y += 1
                    else:
                        return 0
                return 0

            # down movement
            elif m_y < self.y:
                for sp in range(self.speed):
                    if m_y < self.y:
                        for w in range(self.width):
                            if vill.grid[self.y - 1][self.x + w] != 0:
                                return self.deal_damage(vill, vill.grid[self.y - 1][self.x + w])
                        self.y -= 1
                    else:
                        return 0
                return 0

        else:
            m_dist = vill.rows + vill.cols
            tar_id = -1
            for b in vill.buildings:
                if b.id > vill.num_huts + 1 + vill.num_wiz:
                    break
                elif b.id <= vill.num_huts + 1 and ( vill.num_wiz > 0 or len(vill.cannons) > 0 ):
                    continue
                
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

            # right movement
            if m_x > self.x:           
                for sp in range(self.speed):
                    if m_x > self.x:
                        for h in range(self.height):
                            if vill.grid[self.y + h][self.x + self.width] == tar_id:
                                return self.deal_damage(vill, vill.grid[self.y + h][self.x + self.width])                            
                        self.x += 1
                    else:
                        return 0

                return 0

            # left movement
            elif m_x < self.x:
                for sp in range(self.speed):
                    if m_x < self.x:
                        for h in range(self.height):
                            if vill.grid[self.y + h][self.x - 1] == tar_id:
                                return self.deal_damage(vill, vill.grid[self.y + h][self.x - 1])
                        self.x -= 1
                    else:
                        return 0
                return 0


            # up movement
            elif m_y > self.y:
                for sp in range(self.speed):
                    if m_y > self.y:
                        for w in range(self.width):
                            if vill.grid[self.y + self.height][self.x + w] == tar_id:
                                return self.deal_damage(vill, vill.grid[self.y + self.height][self.x + w])
                        self.y += 1
                    else:
                        return 0
                return 0

            # down movement
            elif m_y < self.y:
                for sp in range(self.speed):
                    if m_y < self.y:
                        for w in range(self.width):
                            if vill.grid[self.y - 1][self.x + w] == tar_id:
                                return self.deal_damage(vill, vill.grid[self.y - 1][self.x + w])
                        self.y -= 1
                    else:
                        return 0
                return 0
