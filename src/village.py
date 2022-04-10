from distutils.command.build import build
import imp
from colorama import Fore, Back, Style, init

from troop import Troop
init()

import sys
sys.path.insert(0, './src')

import os
from os import system
from time import sleep, time
import math
import random

# objects required
from king import King
from building import Building
from spawn import Spawn_pt
from cannon import Cannon

# town hall props
th_w = 4
th_h = 3
th_maxh = 100
th_pix = Back.GREEN + ' ' + Style.RESET_ALL
th_dam = 0

# hut props
hut_w = 3
hut_h = 2
hut_maxh = 50
hut_pix = Back.GREEN + ' ' + Style.RESET_ALL
hut_dam = 0

# wall props
wall_w = 1
wall_h = 1
wall_maxh = 15
wall_pix = Back.WHITE + ' ' + Style.RESET_ALL
wall_dam = 0

no_of_cannons = 3

class Vill():

    def __init__(self):

        # dimensions of the village
        self.rows = 40
        self.cols = 90
        self.sc_bd_ht = 5   
        self.border = 1
        self.num_spawn_pts = 3
        self.number_of_files = len( os.listdir('replays') )

        self.bar_style = Back.GREEN + Fore.BLACK + Style.BRIGHT + ' ' + Style.RESET_ALL
        # basic timekeeping
        self.start_t = time()
        self.cur_t = time()

        # background color
        self.bg_color = Back.BLACK  + ' ' + Style.RESET_ALL
        self.borders  = Back.YELLOW + ' ' + Style.RESET_ALL

        # checking end of game
        self.game_end = 0

        # troops in general
        self.troops = []

        # king
        king_loc = ( 4 + 4*(self.cols - 8)//(self.num_spawn_pts+2), 1 )
        self.king = King(king_loc[0], king_loc[1])
        self.health_bar = self.king.max_health      # king's health bar
        self.troops.append( self.king )# king_loc[0], king_loc[1], self.king.id, self.king.width, self.king.height, self.king.max_health, self.king.max_health, self.king.pixel ) )

        #spawn pts for troops
        spawn_loc = [ ( 4 + (i+1)*(self.cols - 8)//(self.num_spawn_pts+2), 2 ) for i in range(self.num_spawn_pts) ]
        self.spawn_pts = [ Spawn_pt(spawn_loc[i]) for i in range(self.num_spawn_pts) ]

        # hall 
        build_loc = [ (self.cols//2, self.rows//2, 1) ]
        self.buildings = [ Building( loc, th_w, th_h, th_pix, th_maxh, th_maxh, th_dam ) for loc in build_loc ]
        
        # huts
        self.num_huts = 5
        build_loc = build_loc + [ ( (self.cols - 8)//4, (self.rows + self.sc_bd_ht - 8)//2, 2 ), ( 3*(self.cols)//4, (self.rows + self.sc_bd_ht - 8)//2, 3 ) ]

        for i in range(0, self.num_huts - 2):
            build_loc.append( ( (i+1)*(self.cols//(self.num_huts - 1)), 3*(self.rows//4), i + 4 ) ) 

        self.buildings = self.buildings + [ Building( loc, hut_w, hut_h, hut_pix, hut_maxh, hut_maxh, hut_dam ) for loc in build_loc[1:] ]
        
        # walls
        for i in range (4, self.rows - 4 + 1):
            build_loc.append( (self.cols - 4, i, len(build_loc) + 1) )
            build_loc.append( (4, i, len(build_loc) + 1) )
            # print( self.num_huts + 2 + (i-4)*2, self.num_huts + 2 + (i-4)*2 + 1 )

        for i in range (4, self.cols - 4 ):
            build_loc.append( (i, 4, len(build_loc) + 1) )
            build_loc.append( (i, self.rows - 4, len(build_loc) + 1) )
            # print( self.num_huts + 2*self.rows - 12 + (i-4)*2, self.num_huts + 2*self.rows - 12 + (i-4)*2 + 1 )

        self.buildings = self.buildings + [ Building( loc, wall_w, wall_h, wall_pix, wall_maxh, wall_maxh, wall_dam ) for loc in build_loc[self.num_huts+1:] ] 

        # cannons 
        self.num_cannons = no_of_cannons
        tmp = len(build_loc) + 1
        cannon_loc = [ ( 4 + (i+1)*(self.cols - 8)//(self.num_cannons+1), (4 + self.rows)//4, tmp + i ) for i in range(self.num_cannons)  ]
        self.cannons = [ Cannon( loc ) for loc in cannon_loc ]

        self.buildings = self.buildings + [ x for x in self.cannons ]
        self.total_buildings = len(self.buildings)
        
        # a 2d array of all the objects in the village
        self.grid = [ [0 for i in range(self.cols)] for j in range(self.rows) ]

        # renders the village
        self.render()

    def add_troop(self, pt):
        x, y = self.spawn_pts[pt].x, self.spawn_pts[pt].y 
        id = len(self.troops) + 1

        tr_att = 3
        tr_sp = 1
        tr_heal = 15

        tr_wid = 1
        tr_ht = 1

        barb_pix = Back.RED + Fore.BLACK + ' ' + Style.RESET_ALL

        self.troops.append( Troop(x, y, id, tr_wid, tr_ht, tr_heal, tr_heal, barb_pix, tr_att, tr_sp) )

    def rm_build(self, b):
        # remove from grid
        for r in range(b.y, b.y + b.height):
            for c in range(b.x, b.x + b.width):
                self.village[r][c] = self.bg_color
                self.grid[r][c] = 0
            
            if b.id > self.total_buildings - no_of_cannons:
                # print(b.id, self.total_buildings - self.num_cannons)
                for x in self.cannons:
                    if b.id == x.id:
                        self.cannons.remove(x)

                self.num_cannons -= 1
        
        self.buildings.remove(b)
    
    def rm_troop(self, id):
        for x in self.troops:
            if x.id == id:
                self.troops.remove(x)
                break
        
        if len(self.troops) == 0:
            self.game_end = -1        

    def render(self):
        # barbarians move to nearest buildings
        for troop in self.troops[1:]:
            # print(self.game_end)
            self.game_end = troop.move_and_attack(self)

            if self.game_end != 0:
                break

        for c in self.cannons:
            c.deal_damage(self)

        system('clear')      
        self.village = [[self.bg_color for x in range(self.cols)] for y in range(self.rows)]
        
        # render troops
        for troop in self.troops:
            for r in range(troop.y, troop.y+troop.height):
                for c in range(troop.x, troop.x+troop.width):
                    self.village[r][c] = troop.pixel
        
        # render buildings
        for b in self.buildings:
            # print(b.id)
            if b.health > 0:
                for r in range(b.y, b.y + b.height):
                    for c in range(b.x, b.x + b.width):
                        self.village[r][c] = b.pixel
                        self.grid[r][c] = b.id

        # render spawn pts
        for spawn_pt in self.spawn_pts:
            for r in range(spawn_pt.y, spawn_pt.y + spawn_pt.height):
                for c in range(spawn_pt.x, spawn_pt.x + spawn_pt.width):
                    self.village[r][c] = spawn_pt.pixel
                
        self.output = [[self.borders for i in range(self.cols+2*self.border)] for j in range(self.sc_bd_ht+self.rows+2*self.border)]

        # display title
        title = "Clash of Deadlines"
        title_offset = (self.cols+self.border-len(title)) // 2
        for j in range(0, len(title)):
            self.output[1][title_offset+j] = Back.YELLOW + Fore.BLACK + Style.BRIGHT + title[j] + Style.RESET_ALL

        # display king's health bar
        health_bar = "Health: "
        health_bar_offset = (self.cols+self.border-len(health_bar)) // 4
        for j in range(0, len(health_bar)):
            self.output[3][health_bar_offset+j] = Back.YELLOW + Fore.BLACK + Style.BRIGHT + health_bar[j] + Style.RESET_ALL
        
        # display king's health
        health_offset = health_bar_offset + len(health_bar)
        for j in range(0, self.king.health//2):
            self.output[3][health_offset+j] = self.bar_style
                
        # render the village excluding the borders + score board
        for j in range(0, self.rows):
            for i in range(0, self.cols):
                self.output[j + self.sc_bd_ht + self.border][i + self.border] = self.village[j][i]

        # if game has ended
        if self.game_end != 0:
            game_end_screen_height = 8
            game_end_screen_width = self.cols//2
            self.game_end_screen = [[wall_pix for i in range(game_end_screen_width)] for j in range(game_end_screen_height)]
            # game_end_screen_offset = (self.cols - game_end_screen_width) // 2

            # display game over
            game_over = ""
            if self.game_end == 1:
                game_over = game_over + "Victory!"
            else:
                game_over = game_over + "You Lose!"
            game_over_offset = (game_end_screen_width - len(game_over)) // 2

            for j in range(0, len(game_over)):
                self.game_end_screen[1][game_over_offset+j] = Back.WHITE + Fore.BLACK + Style.BRIGHT + game_over[j] + Style.RESET_ALL

            height_offset = self.sc_bd_ht+((self.rows//2)-(game_end_screen_height//2)+1)
            width_offset = 2*1+((self.cols//2)-(game_end_screen_width//2))
            for row in range(0, game_end_screen_height):
                for col in range(0, game_end_screen_width):
                    self.output[height_offset+row][width_offset+col] = self.game_end_screen[row][col]
            

        print("\n".join(["".join(row) for row in self.output]))

        # sys.path.insert(0, '../replays')
        replay_f = 'replays/replay' + str(self.number_of_files + 1) + '.txt' 
        with open(replay_f, 'a+') as f:        
            for row in self.output:
                for col in row:
                    f.write(col)
                f.write('\n')
            f.write("\n")
            f.write("demarcation\n")

        if self.game_end ==  0:
            self.cur_t = time()
        else:
            print("Thank you")
            exit()
        # self.bar_style = self.king.take_damage(10, self)

        # print grid
        # for row in self.grid:
        #     print(row)
