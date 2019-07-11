"""
TODO:

address questions (about purpose of variables) in comments ==> debug (main problems are likely with variables and how each
function is being called, which I don't know because I don't fully understand the original game code
"""

import sys
import pygame
import random
from utils import *

running = True
botTurn = True

action = -2     # bot initially moves downwards to avoid upward swarm of pedestrians

pedestrianAmt = 0   # amount of pedestrians created
playerCounter = 0   # score for bot (based on how many turns it survived for)
pedestrianCounter = 0   # what is this for?

score = 0
penalty = 0
reward = 0

alpha = 0.85    # learning rate
gamma = 0.99    # discount value
episode = 0     # number of episodes

def drawGrid(): # draws grid of 25 x 25 pixels: width 8, height 12
  for i in range(1, 8):
      gridWidth = i*(display_width/8)
      pygame.draw.line(screen, BLACK, (gridWidth, 0), (gridWidth, display_height), 1)
  for i in range(1, 12):
      gridLength = i*(display_height/12)
      pygame.draw.line(screen, BLACK, (0, gridLength), (display_width, gridLength), 1)

def drawPlayer():
  pygame.draw.circle(screen, BLUE, (startingPlayerWidth, startingPlayerHeight), 10)

def drawPedestrian():
  for i in range(pedestrianAmt):
      pygame.draw.circle(screen, RED, ((dWidth["startingPedestrianWidth"+str(i)]), (dHeight["startingPedestrianHeight"+str(i)])), 10)

#updates onscreen text based on the player counter number
def updateScore():
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render(str(score), True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (75,290)
    screen.blit(text, textRect)
    text1 = font.render(str(penalty), True, BLACK, WHITE)
    textRect1 = text1.get_rect()
    textRect1.center = (125,290)
    screen.blit(text1, textRect)


# dictionaries containing position and action of pedestrians
dWidth = {}
dHeight = {}
dDirection = {}

# list containing actions of bot ==> replace? according to format; prob won't need it bc of bot class in classes.py
playerDirection = []

def addPedestrian():
   global dDirection, dHeight, dWidth, pedestrianAmt
   dDirectionHolder = {}
   dHeightHolder = {}
   dWidthHolder = {}
   for i in range(1):
       dWidthHolder["startingPedestrianWidth{0}".format(pedestrianCounter)] = int(random.randint(1, 9) * (display_width/8))
       dWidth.update(dWidthHolder)
   for i in range(1): #pedestrianAmt
       pedestrianOpt = [0,display_height]
       dHeightHolder["startingPedestrianHeight{0}".format(pedestrianCounter)] = pedestrianOpt[random.randint(0, 1)]
       dHeight.update(dHeightHolder)
       dDirectionHolder = dHeightHolder.copy()
       dDirection.update(dDirectionHolder)

# returns dictionary of x, y position of pedestrians
def getPedestrianLocations():
    if dHeight is None or dWidth is None or pedestrianAmt is None:
        return
    else:
        return {index: (ped_x, ped_y) for index, (ped_x, ped_y) in enumerate(list(zip(dWidth.values(), dHeight.values())))}

addPedestrian() # why is this called here?

def main():
  global running, screen, startingPlayerWidth, startingPlayerHeight, startingPedestrianWidth, startingPedestrianHeight, botTurn, pedestrianAmt, playerCounter, pedestrianCounter

  pygame.init()

  screen = pygame.display.set_mode((display_width, display_height))
  pygame.display.set_caption("Dodgy Sidewalk")

  drawGrid()
  drawPlayer()
  drawPedestrian()

  pygame.display.update()

  # coordinate of the center of the game screen (starting position of bot)
  startingPlayerWidth = int(display_width/2)+1
  startingPlayerHeight = int(display_height/2)+1

while running:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)

    collision = False
    botPos = [startingPlayerWidth, startingPlayerHeight]
    pedestrianPos = transition.allPedestrianPos
    for pedestrian in range(len(pedestrianPos)):
        if botPos == pedestrian:
            collision = True
            break

    if collision == False:
        reward = 1
        if (episode % 5) == 0:
            addPedestrian()
        pedestrianY = 0
    else:
        reward = 0
        if (episode % 5) == 0:
            addPedestrian()
        # change pedestrian's position (get random action)

    state = State(Bot(startingPlayerWidth, startingPlayerHeight), Pedestrian([pedestrianX, pedestrianY]))
    act = optimalAction(state)      # get the best action so far in the game
    r0 = getReward(state.bot, state.pedestrian)     # get immediate rewards of this step
    nextState = transition(state, act)  # new state after taking optimal action
    Q[stateEncoder(state), act] += alpha * (r0 + gamma * np.max(Q[stateEncoder(nextState), :]) - Q[stateEncoder(state), act])   # build the Q-table, index by (state, action) pair

    Bot = newBotPos(state.Bot, act)
    pedestrian = state.pedestrian.pedestrianList

    drawGrid()
    drawPlayer()
    drawPedestrian()

    if reward == 1:
        score += reward
    elif reward == -1:
        penalty += reward

    updateScore()

    pygame.display.update()
    if episode == 1000:
        break
    else:
        episode += 1


    #######################################

    # # random player bot - for now to map out the states for anthony
    # if botTurn:
    #     global playerDirection
    #     playerDirections = ["n"]*25 + ["e"]*25 + ["w"]*25 + ["s"]*25
    #     playerMove = playerDirections[random.randint(0,99)]
    #     playerDirection.append(playerMove)
    #
    #     if ((playerMove) == "n") and not (startingPlayerHeight <= 1):
    #         startingPlayerHeight = startingPlayerHeight - 25
    #     elif ((playerMove) == "s") and not (startingPlayerHeight >= display_height-1):
    #         startingPlayerHeight = startingPlayerHeight + 25
    #     elif (playerMove == "e") and not (startingPlayerWidth >= display_width):
    #         startingPlayerWidth = startingPlayerWidth + 25
    #     elif (playerMove == "w") and not (startingPlayerWidth <= 1):
    #         startingPlayerWidth = startingPlayerWidth - 25
    #
    #     botTurn = False
    #     playerCounter = playerCounter + 1
    #     if (playerCounter % 5) == 0:
    #         pedestrianAmt = pedestrianAmt + 1
    #         addPedestrian()
    #         pedestrianCounter = pedestrianCounter + 1
    #
    # if not botTurn:
    #     # here's to the random pedestrian code
    #     pygame.time.delay(500)
    #     for i in range(pedestrianAmt):
    #         #decisions on probabilities
    #         if (dDirection["startingPedestrianHeight"+str(i)]) == 0:
    #             directions = ["n"]*10 + ["e"]*10 + ["w"]*10 + ["s"]*70
    #         elif (dDirection["startingPedestrianHeight"+str(i)]) == display_height:
    #             directions = ["n"]*70 + ["e"]*10 + ["w"]*10 + ["s"]*10
    #         (pedestrianMove) = directions[random.randint(0,99)]
    #
    #         #no overlaps
    #         overlapWest = False
    #         overlapEast = False
    #         overlapNorth = False
    #         overlapSouth = False
    #
    #         for a in range(pedestrianAmt):
    #             if (i != a):
    #                 if ((dWidth["startingPedestrianWidth"+str(i)]+25) == (dWidth["startingPedestrianWidth"+str(a)])) and ((dHeight["startingPedestrianHeight"+str(i)]) == (dHeight["startingPedestrianHeight"+str(a)])):
    #                     overlapWest = True
    #                 elif ((dWidth["startingPedestrianWidth"+str(i)]-25) == (dWidth["startingPedestrianWidth"+str(a)])) and ((dHeight["startingPedestrianHeight"+str(i)]) == (dHeight["startingPedestrianHeight"+str(a)])):
    #                     overlapEast = True
    #                 elif ((dWidth["startingPedestrianWidth"+str(i)]) == (dWidth["startingPedestrianWidth"+str(a)])) and ((dHeight["startingPedestrianHeight"+str(i)]+25) == (dHeight["startingPedestrianHeight"+str(a)])):
    #                     overlapNorth = True
    #                 elif ((dWidth["startingPedestrianWidth"+str(i)]) == (dWidth["startingPedestrianWidth"+str(a)])) and ((dHeight["startingPedestrianHeight"+str(i)]-25) == (dHeight["startingPedestrianHeight"+str(a)])):
    #                     overlapSouth = True
    #
    #         if ((pedestrianMove) == "n") and not overlapNorth:
    #             dHeight["startingPedestrianHeight"+str(i)] = dHeight["startingPedestrianHeight"+str(i)] - 25
    #         elif ((pedestrianMove) == "s") and not overlapSouth:
    #             dHeight["startingPedestrianHeight"+str(i)] = dHeight["startingPedestrianHeight"+str(i)] + 25
    #         elif (pedestrianMove == "e") and (dWidth["startingPedestrianWidth"+str(i)] is not display_width) and not overlapEast:
    #             dWidth["startingPedestrianWidth"+str(i)] = dWidth["startingPedestrianWidth"+str(i)] + 25
    #         elif (pedestrianMove == "w") and (dWidth["startingPedestrianWidth"+str(i)] is not 0) and not overlapWest:
    #             dWidth["startingPedestrianWidth"+str(i)] = dWidth["startingPedestrianWidth"+str(i)] - 25
    #
    #         #end game
    #         if ((dWidth["startingPedestrianWidth"+str(i)]-5) <=startingPlayerWidth <= (dWidth["startingPedestrianWidth"+str(i)]+5)) and ((dHeight["startingPedestrianHeight"+str(i)]-5) <=startingPlayerHeight <= (dHeight["startingPedestrianHeight"+str(i)]+5)):
    #             playerCounter = -1
    #
    #     screen.fill(WHITE)
    #     drawGrid()
    #     drawPlayer()
    #     drawPedestrian()
    #     updateCounter()
    #     pygame.display.update()
    #     botTurn = True
    #     # print(getPedestrianLocations())
    #     # print(getPedestrianLocations()[0][1])
