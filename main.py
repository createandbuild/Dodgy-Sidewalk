"""
TODO:

address questions (about purpose of variables) in comments
change format to match this repo: https://github.com/hasanIqbalAnik/q-learning-python-example/blob/master/main.py
change score interface to display penalties and total score (i.e. how many times it collided & overall score [ = rewards - penalty])
"""

import sys
import pygame
import random
from utils import *

running = True
botTurn = True

pedestrianAmt = 0   # amount of pedestrians created
playerCounter = 0   # score for bot (based on how many turns it survived for)
pedestrianCounter = 0   # what is this for?

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
def updateCounter():
   font = pygame.font.Font('freesansbold.ttf', 20)
   text = font.render(str(playerCounter), True, BLACK, WHITE)
   textRect = text.get_rect()
   textRect.center = (100,290)
   screen.blit(text, textRect)

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

          screen.fill(WHITE)
          drawGrid()
          drawPlayer()
          drawPedestrian()
          updateCounter()
          pygame.display.update()
          botTurn = True
          # print(getPedestrianLocations())
          # print(getPedestrianLocations()[0][1])


if __name__ == '__main__':  # run the game
    main()
