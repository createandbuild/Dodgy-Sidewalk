import sys

from pygame.locals import *
from utils import *

FPS = 20  # frames per second setting
fpsClock = pg.time.Clock()

pg.init()  # pygame initialization

window = pg.display.set_mode((windowWidth, windowHeight))  # width, height
pg.display.set_caption('Catch the ball!')

rct = pg.Rect(rctLeft, rctTop, rctWidth, rctHeight)  # Rect(left, top, width, height)

action = 1  # 0 means stay, 1 means left, 2 means right

score = 0
missed = 0
reward = 0
font = pg.font.Font(None, 30)

# set learning rate
lr = .85
y = .99

i = 0

while True:
    for event in pg.event.get():
        if event.type == QUIT:  # for the quitting button on the window
            pg.quit()
            sys.exit()

    window.fill(BLACK)  # window background

    # at this position, the rectangle should be here. else loses
    if crclCentreY >= windowHeight - rctHeight - crclRadius:  # check if the rectangle is under the circle or not
        reward = calculate_score(rct, Circle(crclCentreX, crclCentreY))  # +1 or -1
        crclCentreX = circle_falling(crclRadius)  #
        crclCentreY = 50
    else:
        reward = 0  # no reward if the ball wasn't missed
        crclCentreY += crclYStepFalling  # let the circle fall freely

    s = State(rct, Circle(crclCentreX, crclCentreY))
    act = get_best_action(s)  # get the best action so far in this state
    r0 = calculate_score(s.rect, s.circle)  # get the immediate reward of this step
    s1 = new_state_after_action(s, act)  # new state after taking the best action
    # build the Q table, indexed by (state, action) pair
    Q[state_to_number(s), act] += r0 + y * np.max(Q[state_to_number(s1), :])

    rct = new_rect_after_action(s.rect, act)  # new position of the rectangle
    crclCentreX = s.circle.circleX  # put the ball where it originally was before the experiment
    crclCentreY = s.circle.circleY

    pg.draw.circle(window, RED, (int(crclCentreX), int(crclCentreY)),
                   crclRadius)  # circle(Surface, color, pos(x, y), radius, width=0)
    pg.draw.rect(window, GREEN, rct)  # rect(Surface, color, Rect, width=0)

    if reward == 1:  # got it!
        score += reward  # add the reward to the total score
    elif reward == -1:  # missed
        missed += reward  # add the reward to the missed count

    text = font.render('score: ' + str(score), True, (238, 58, 140))  # update the score on the screen
    text1 = font.render('missed: ' + str(missed), True, (238, 58, 140))  # update the score on the screen
    window.blit(text, (windowWidth - 120, 10))  # render score
    window.blit(text1, (windowWidth - 280, 10))  # render missed

    pg.display.update()  # update display
    fpsClock.tick(FPS)
    if i == 10000:  # stopping condition
        break
    else:
        i += 1


###########################3

import pygame
import random

running = True

#turns - human player vs random bot (player turn is the human for now)
playerTurn = True

"""
to do
make it accessible for anthony
rewards, states, actions (directions)

playerCounter ... works with rewards (positives are alive, negatives for death)
states are the positions of bot (startingPlayerWidth, startingPlayerHeight)
actions - directions of bot (playerDirection)
"""

def drawGrid():
  #grids lol 25 x 25 squares : width 8, height 24
  for i in range(1,8):
      gridWidth = i*(display_width/8)
      pygame.draw.line(screen, BLACK, (gridWidth, 0), (gridWidth, display_height), 1)
  for i in range(1,12):
      gridLength = i*(display_height/12)
      pygame.draw.line(screen, BLACK, (0, gridLength), (display_width, gridLength), 1)

def drawPlayer():
  pygame.draw.circle(screen, RED, (startingPlayerWidth, startingPlayerHeight), 10)

def drawPedestrian():
  for i in range(pedestrianAmt):
      pygame.draw.circle(screen, BLUE, ((dWidth["startingPedestrianWidth"+str(i)]), (dHeight["startingPedestrianHeight"+str(i)])), 10)

#keep track of the amount of pedestrians onscreen lol
pedestrianAmt = 0

#how many turns has the player not died
playerCounter = 0

#everything ever i guess what the huh
pedestrianCounter = 0

#updates onscreen text based on the player counter number
def updateCounter():
   font = pygame.font.Font('freesansbold.ttf', 20)
   text = font.render(str(playerCounter), True, BLACK, WHITE)
   textRect = text.get_rect()
   textRect.center = (100,290)
   screen.blit(text, textRect)

#a dictionary storing all the pedestrians i guess
dWidth = {}
dHeight = {}
dDirection = {}

#list for player/bot directions- UP FOR ANTHONY REVISION
playerDirection = []

def addPedestrian():
   global dDirection, dHeight, dWidth, pedestrianAmt
   #can we use local variables
   dDirectionHolder = {}
   dHeightHolder = {}
   dWidthHolder = {}
   for i in range(1):
       dWidthHolder["startingPedestrianWidth{0}".format(pedestrianCounter)]= int(random.randint(1,9) * (display_width/8))
       dWidth.update(dWidthHolder)
   for i in range(1): #pedestrianAmt
       pedestrianOpt = [0,display_height]
       dHeightHolder["startingPedestrianHeight{0}".format(pedestrianCounter)]= pedestrianOpt[random.randint(0,1)]
       dHeight.update(dHeightHolder)
       dDirectionHolder = dHeightHolder.copy()
       dDirection.update(dDirectionHolder)

addPedestrian()

def main():
  global running, screen, startingPlayerWidth, startingPlayerHeight, startingPedestrianWidth, startingPedestrianHeight, playerTurn, pedestrianAmt, playerCounter, pedestrianCounter
  pygame.init()

  #the middle coordinates lmao
  startingPlayerWidth = int(display_width/2)+1
  startingPlayerHeight = int(display_height/2)+1

  screen = pygame.display.set_mode((display_width, display_height))

  pygame.display.set_caption("dodgy")
  screen.fill(WHITE)
  drawGrid()
  drawPlayer()
  drawPedestrian()
  pygame.display.update()

  while running:

      ev = pygame.event.get()

      #random player bot - for now to map out the states for anthony
      if playerTurn:
          global playerDirection
          playerDirections = ["n"]*25 + ["e"]*25 + ["w"]*25 + ["s"]*25
          playerMove = playerDirections[random.randint(0,99)]
          playerDirection.append(playerMove)

          if ((playerMove) == "n") and not (startingPlayerHeight <= 1):
              startingPlayerHeight = startingPlayerHeight - 25
          elif ((playerMove) == "s") and not (startingPlayerHeight >= display_height):
              startingPlayerHeight = startingPlayerHeight + 25
          elif (playerMove == "e") and not (startingPlayerWidth >= display_width):
              startingPlayerWidth = startingPlayerWidth + 25
          elif (playerMove == "w") and not (startingPlayerWidth <= 1):
              startingPlayerWidth = startingPlayerWidth - 25

          playerTurn = False
          playerCounter = playerCounter + 1
          if (playerCounter % 5) == 0:
              pedestrianAmt = pedestrianAmt + 1
              addPedestrian()
              pedestrianCounter = pedestrianCounter + 1

      if not playerTurn:
          #here's to the random pedestrian code
          pygame.time.delay(500)
          for i in range(pedestrianAmt):
              #decisions on probabilities
              if (dDirection["startingPedestrianHeight"+str(i)]) == 0:
                  directions = ["n"]*10 + ["e"]*10 + ["w"]*10 + ["s"]*70
              elif (dDirection["startingPedestrianHeight"+str(i)]) == display_height:
                  directions = ["n"]*70 + ["e"]*10 + ["w"]*10 + ["s"]*10
              (pedestrianMove) = directions[random.randint(0,99)]

              #no overlaps
              overlapWest = False
              overlapEast = False
              overlapNorth = False
              overlapSouth = False

              for a in range(pedestrianAmt):
                  if (i != a):
                      if ((dWidth["startingPedestrianWidth"+str(i)]+25) == (dWidth["startingPedestrianWidth"+str(a)])) and ((dHeight["startingPedestrianHeight"+str(i)]) == (dHeight["startingPedestrianHeight"+str(a)])):
                          overlapWest = True
                      elif ((dWidth["startingPedestrianWidth"+str(i)]-25) == (dWidth["startingPedestrianWidth"+str(a)])) and ((dHeight["startingPedestrianHeight"+str(i)]) == (dHeight["startingPedestrianHeight"+str(a)])):
                          overlapEast = True
                      elif ((dWidth["startingPedestrianWidth"+str(i)]) == (dWidth["startingPedestrianWidth"+str(a)])) and ((dHeight["startingPedestrianHeight"+str(i)]+25) == (dHeight["startingPedestrianHeight"+str(a)])):
                          overlapNorth = True
                      elif ((dWidth["startingPedestrianWidth"+str(i)]) == (dWidth["startingPedestrianWidth"+str(a)])) and ((dHeight["startingPedestrianHeight"+str(i)]-25) == (dHeight["startingPedestrianHeight"+str(a)])):
                          overlapSouth = True

              if ((pedestrianMove) == "n") and not overlapNorth:
                  dHeight["startingPedestrianHeight"+str(i)] = dHeight["startingPedestrianHeight"+str(i)] - 25
              elif ((pedestrianMove) == "s") and not overlapSouth:
                  dHeight["startingPedestrianHeight"+str(i)] = dHeight["startingPedestrianHeight"+str(i)] + 25
              elif (pedestrianMove == "e") and (dWidth["startingPedestrianWidth"+str(i)] is not display_width) and not overlapEast:
                  dWidth["startingPedestrianWidth"+str(i)] = dWidth["startingPedestrianWidth"+str(i)] + 25
              elif (pedestrianMove == "w") and (dWidth["startingPedestrianWidth"+str(i)] is not 0) and not overlapWest:
                  dWidth["startingPedestrianWidth"+str(i)] = dWidth["startingPedestrianWidth"+str(i)] - 25

              #end game #mendelssohn violin concerto in e minor
              if ((dWidth["startingPedestrianWidth"+str(i)]-5) <=startingPlayerWidth <= (dWidth["startingPedestrianWidth"+str(i)]+5)) and ((dHeight["startingPedestrianHeight"+str(i)]-5) <=startingPlayerHeight <= (dHeight["startingPedestrianHeight"+str(i)]+5)):
                  pedestrianCounter = -10000
                  pygame.display.quit()

          screen.fill(WHITE)
          drawGrid()
          drawPlayer()
          drawPedestrian()
          updateCounter()
          pygame.display.update()
          playerTurn = True

      for event in ev:
          if event.type == pygame.QUIT:
              running = False

