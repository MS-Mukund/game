import sys
from time import monotonic as clock, sleep
import os
sys.path.insert(0, './src')

from village import Vill
# works only for bash
os.system('stty -echo')

vill = Vill()

# In order to follow coordinate system, (x,y) needs to be written in [y][x] format, where y grows downwards.

while( True ):
    start = clock()
    
    vill.king.move(vill)
    
    if vill.render() == True:
        break
    
    while True:
        if clock() - start > 0.1:
            break

os.system('stty echo')
