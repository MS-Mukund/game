import sys
sys.path.insert(0, './src')

from village import Vill

vill = Vill()

# In order to follow coordinate system, (x,y) needs to be written in [y][x] format, where y grows downwards.

while( True ):
    
    vill.king.move(vill)
    
    if vill.render() == True:
        break
    