from distutils.command.build import build
import imp
from colorama import Fore, Back, Style, init
init()

import sys
sys.path.insert(0, './src')

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

# hut props
hut_w = 3
hut_h = 2
hut_maxh = 50
hut_pix = Back.GREEN + ' ' + Style.RESET_ALL

# wall props
wall_w = 1
wall_h = 1
wall_maxh = 15
wall_pix = Back.WHITE + ' ' + Style.RESET_ALL

class Vill():

    def __init__(self):

        # dimensions of the village
        self.rows = 40
        self.cols = 90
        self.sc_bd_ht = 8
        self.border = 1
        self.num_spawn_pts = 3

        # basic timekeeping
        self.start_t = time()
        self.cur_t = time()

        # background color
        self.bg_color = Back.BLACK  + ' ' + Style.RESET_ALL
        self.borders  = Back.YELLOW + ' ' + Style.RESET_ALL

        # checking end of game
        self.game_end = False

        # king
        king_loc = ( 4 + (4)*(self.cols - 8)//(self.num_spawn_pts+2), 1 )
        self.king = King(king_loc[0], king_loc[1])

        #spawn pts for troops
        spawn_loc = [ ( 4 + (i+1)*(self.cols - 8)//(self.num_spawn_pts+2), 2 ) for i in range(self.num_spawn_pts) ]

        self.spawn_pts = [ Spawn_pt(spawn_loc[i]) for i in range(self.num_spawn_pts) ]

        # hall 
        build_loc = [ (self.cols//2, self.rows//2, 1) ]
        self.buildings = [ Building( loc, th_w, th_h, th_pix, th_maxh, th_maxh ) for loc in build_loc ]
        
        # huts
        self.num_huts = 5
        build_loc = build_loc + [ ( (self.cols - 8)//4, (self.rows + self.sc_bd_ht - 8)//2, 2 ), ( 3*(self.cols)//4, (self.rows + self.sc_bd_ht - 8)//2, 3 ) ]

        for i in range(0, self.num_huts - 2):
            build_loc.append( ( (i+1)*(self.cols//(self.num_huts - 1)), 3*(self.rows//4), i + 4 ) ) 

        self.buildings = self.buildings + [ Building( loc, hut_w, hut_h, hut_pix, hut_maxh, hut_maxh ) for loc in build_loc[1:] ]
        
        # walls
        for i in range (4, self.rows - 4 + 1):
            build_loc.append( (4, i, self.num_huts + 2 + (i-4)*2) )
            build_loc.append( (self.cols - 4, i, self.num_huts + 2 + (i-4)*2 + 1) )
            # print( self.num_huts + 2 + (i-4)*2, self.num_huts + 2 + (i-4)*2 + 1 )

        for i in range (4, self.cols - 4 ):
            build_loc.append( (i, 4, self.num_huts + 2*self.rows - 12 + (i-4)*2) )
            build_loc.append( (i, self.rows - 4, self.num_huts + 2*self.rows - 12 + (i-4)*2 + 1) )
            # print( self.num_huts + 2*self.rows - 12 + (i-4)*2, self.num_huts + 2*self.rows - 12 + (i-4)*2 + 1 )

        self.buildings = self.buildings + [ Building( loc, wall_w, wall_h, wall_pix, wall_maxh, wall_maxh ) for loc in build_loc[self.num_huts+1:] ] 

        # cannons 
        self.num_cannons = 3
        cannon_loc = [ ( 4 + (i+1)*(self.cols - 8)//(self.num_cannons+1), (4 + self.rows)//4 ) for i in range(self.num_cannons)  ]
        self.cannons = [ Cannon( (loc) ) for loc in cannon_loc ]
        
        # a 2d array of all the objects in the village
        self.grid = [ [0 for i in range(self.cols)] for j in range(self.rows) ]

        # renders the village
        self.render()
    
    def rm_build(self, b):
        # remove from grid
        for r in range(b.y, b.y + b.height):
                    for c in range(b.x, b.x + b.width):
                        self.village[r][c] = self.bg_color
                        self.grid[r][c] = 0
        
        self.buildings.remove(b)

    def render(self):
        system('clear')
        self.village = [[self.bg_color for x in range(self.cols)] for y in range(self.rows)]

        # render king
        for r in range(self.king.y, self.king.y+self.king.height):
            for c in range(self.king.x, self.king.x+self.king.width):
                print(self.grid[r][c])
                self.village[r][c] = self.king.pixel
        
        # render buildings
        for b in self.buildings:
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
        
        # render cannons
        for cannon in self.cannons:
            for r in range(cannon.y, cannon.y + cannon.height):
                for c in range(cannon.x, cannon.x + cannon.width):
                    self.village[r][c] = cannon.pixel
        
        self.output = [[self.borders for i in range(self.cols+2*self.border)] for j in range(self.sc_bd_ht+self.rows+2*self.border)]

        title = "Clash of Deadlines"
        title_offset = (self.cols+self.border-len(title)) // 2
        for j in range(0, len(title)):
            self.output[1][title_offset+j] = Back.YELLOW + Fore.BLACK + Style.BRIGHT + title[j] + Style.RESET_ALL
        
        # render the village excluding the borders + score board
        for j in range(0, self.rows):
            for i in range(0, self.cols):
                self.output[j + self.sc_bd_ht + self.border][i + self.border] = self.village[j][i]

        # if game has ended
        if self.game_end == True:
            game_end_screen_height = 8
            game_end_screen_width = self.cols//2
            self.game_end_screen = [[self.borders for i in range(game_end_screen_width)] for j in range(game_end_screen_height)]

        print("\n".join(["".join(row) for row in self.output]))

        # print grid
        # for row in self.grid:
        #     print(row)

        if(self.game_end ==  False):
            self.cur_t = time()
