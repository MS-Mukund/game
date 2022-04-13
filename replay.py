''' display the replay of the game'''

import os
from os import system
from time import sleep, time
import sys
sys.path.insert(0, './replays')

num = int(input("Enter which game to display(for previous game press 1, and so on....): "))
number_of_files = len( os.listdir('replays') )

replay_f = 'replays/replay' + str(number_of_files - num + 1) + '.txt'

if num > number_of_files:

    print("No such file exists")
    exit()

with open( replay_f, "r") as replay:
    for line in replay:
        if line.strip() == "demarcation":
            sleep(0.3)
            system('clear')
        else:
            print(line, end="")
            # sleep(0.001)
