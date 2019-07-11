import sys
import pygame
import random
from initializers import *
from classes import *

# pygame.init()

running = True
botTurn = True

action = -2     # bot initially moves downwards to avoid upward swarm of pedestrians

pedestrianAmt = 0   # amount of pedestrians created
pedestrianCounter = 0   # what is this for? #'if it aint broke'

score = 0
penalty = 0
reward = 0

alpha = 0.85    # learning rate
gamma = 0.99    # discount value
episode = 0     # number of episodes

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
        botX = state.bot.botX
        botY = state.bot.botY

    allPedestrianPos = []   #add in random action for pedestrians
    for key in getPedestrianLocations():
        allPedestrianPos.append(getPedestrianLocations()[key])

    botPos = Player(botX, botY)
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
    for i in range(pedestrianAmt):
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
    screen.blit(text1, textRect1)


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
       dWidthHolder["startingPedestrianWidth{0}".format(pedestrianAmt)] = int(random.randint(1, 9) * (display_width/8))
       dWidth.update(dWidthHolder)
   for i in range(1):
       pedestrianOpt = [0,display_height]
       dHeightHolder["startingPedestrianHeight{0}".format(pedestrianAmt)] = pedestrianOpt[random.randint(0, 1)]
       dHeight.update(dHeightHolder)
       dDirectionHolder = dHeightHolder.copy()
       dDirection.update(dDirectionHolder)

# returns dictionary of x, y position of pedestrians
def getPedestrianLocations():
    if dHeight is None or dWidth is None or pedestrianAmt is None:
        return
    else:
        return {index: (ped_x, ped_y) for index, (ped_x, ped_y) in enumerate(list(zip(dWidth.values(), dHeight.values())))}

addPedestrian()

def main():
  global running, screen, startingPlayerWidth, startingPlayerHeight, startingPedestrianWidth, startingPedestrianHeight, botTurn, pedestrianAmt, pedestrianCounter, episode, score, penalty

  pygame.init()

  screen = pygame.display.set_mode((display_width, display_height))
  pygame.display.set_caption("Dodgy Sidewalk")

  # coordinate of the center of the game screen (starting position of bot)
  startingPlayerWidth = int(display_width/2)+1
  startingPlayerHeight = int(display_height/2)+1

  drawGrid()
  drawPlayer()
  drawPedestrian()

  pygame.display.update()

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
    pedestrianPos = []
    for key in getPedestrianLocations():
        pedestrianPos.append(getPedestrianLocations()[key])
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
        startingPedestrianWidth += pedestrianXStep
        startingPedestrianHeight += pedestrianYStep

    state = State(Player(startingPlayerWidth, startingPlayerHeight), Pedestrian([pedestrianX, pedestrianY]))
    act = optimalAction(state)      # get the best action so far in the game
    r0 = getReward(state.bot, state.pedestrian)     # get immediate rewards of this step
    nextState = transition(state, act)  # new state after taking optimal action
    Q[stateEncoder(state), act] += alpha * (r0 + gamma * np.max(Q[stateEncoder(nextState), :]) - Q[stateEncoder(state), act])   # build the Q-table, index by (state, action) pair

    Bot = newBotPos(state.bot, act)
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

main()
