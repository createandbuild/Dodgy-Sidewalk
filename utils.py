import random
import pygame as pg
from initializers import *
from classes import *
from main import getPedestrianLocations

'''
returns the new state with new positions of the player bot and the pedestrians
'''


def transition(state, action):
    botX = None
    botY = None

    # action = 0: stay, 1: right, -1: left, 2: up, -2: down
    if action == 1:
        if state.bot.botX >= 195:
            botX = state.bot.botX
        else:
            botX = state.botX + 25
    elif action == -1:
        if state.bot.botX <= 5:
            botX = state.bot.botX
        else:
            botX = state.botX - 25
    elif action == 2:
        if state.bot.botY <= 5:
            botY = state.bot.botY
        else:
            botY = state.bot.botY + 25
    elif action == -2:
        if state.bot.botY >= 295:
            botY = state.bot.botY
        else:
            botY = state.bot.botY - 25
    else:
        botX = state.botX
        botY = state.botY

    allPedestrianPos = []   #add in random action for pedestrians
    for key in getPedestrianLocations():
        allPedestrianPos.append(getPedestrianLocations()[key])

    botPos = Bot(botX, botY)
    pedestrianPos = Pedestrian(allPedestrianPos)

    return State(botPos, pedestrianPos)


'''
returns new position of the player bot
'''

def newBotPos(bot, action):
    if action == 1:
        if bot.botX >= 195:
            return bot
        else:
            bot.botX += 25
            return bot
    elif action == -1:
        if bot.botX <= 5:
            return bot
        else:
            bot.botX -= 25
            return bot
    elif action == 2:
        if bot.botY <= 5:
            return bot
        else:
            bot.botY += 25
            return bot
    elif action == -2:
        if bot.botY >= 295:
            return bot
        else:
            bot.botY -= 25
            return bot
    else:
        return bot


'''
calculates the reward based of collision of pedestrian and bot
'''


def getReward(bot, pedestrian):
    botPos = [(bot.botX, bot.botY)]
    pedestrianPos = pedestrian.pedestrianList

    for pedestrian in range(len(pedestrianPos)):
        if botPos == pedestrian:    # -1 penalty for collision
            return -1
    return 1    # +1 reward for survival


'''
numpy array can't work with custom objects as indices.
that's why we must create an integer representation of the states
the position of the rectangle and circle combined should give us a unique
identifier. we are storing the value in another dictionary which would hold the unique
indices.
'''


def stateEncoder(state):
    b_x = state.bot.botX
    b_y = state.bot.botY
    p = state.pedestrian
    sum_pedestrian = 0
    for i in range(len(p)):
        if 0 <= i[0] <= 200 and 0 <= i[1] <= 300:
            sum_pedestrian = sum_pedestrian + i[0] + i[1]

    n = int(str(b_x) + str(b_y) + str(sum_pedestrian))  # unique identifier: sum of x,y coordinates of bot and all pedestrians (that are within the board)

    if n in QIDic:
        return QIDic[n]
    else:
        if len(QIDic):
            maximum = max(QIDic, key=QIDic.get)  # Just use 'min' instead of 'max' for minimum.
            QIDic[n] = QIDic[maximum] + 1
        else:
            QIDic[n] = 1
    return QIDic[n]


def optimalAction(state):
    return np.argmax(Q[stateEncoder(state), :])
