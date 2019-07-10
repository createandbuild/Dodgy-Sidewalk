"""
states: [agent_type, bot_x, bot_y, pedestrian_x, pedestrian_y]
    agent_type: {-1: pedestrian, +1: bot}
    bot_x: [0, 25, 50, 75, 100, 125, 150, 175, 200]
    bot_y: [0, 25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300]
    
    sparse matrix of the bot and pedestrians' location within the board

actions: 
    up
    down
    left
    right
    
agent_type:
    +1: bot
    -1: pedestrian

"""

# def getTransition(state, actionX, actionY):
#     output_state = []
#     bot_x = state[1]
#     bot_y = state[2]
#
#     if state[4] == 0 or state[4] == 299:
#         pedestrian_y = 0
#         bot_x = clamp(bot_x+actionX, 0, 199)
#         bot_y = clamp(bot_y+actionY, 0, 299)
#         for pedestrian_x in range(0, 200, 25):
#             for agent_type in (-1, 2, 2):
#                 output_state.append((agent_type, bot_x, bot_y, pedestrian_x, pedestrian_y))
#     else:

from utility import *

def reward():
    from game import playerCounter
    return playerCounter

def action():
    return playerDirection[-1]

def state():
