import pygame
import random

WHITE =     (255, 255, 255)
BLACK =     (0  ,   0,  0)
BLUE =      (  0,   0, 255)
GREEN =     (  0, 255,   0)
RED =       (255,   0,   0)
TEXTCOLOR = (  0,   0,  0)

display_width = 200
display_height = 600

running = True

#turns - human player vs random bot (player turn is the human for now)
playerTurn = True

def drawGrid():
  #grids lol 25 x 25 squares : width 8, height 24
  for i in range(1,8):
      gridWidth = i*(display_width/8)
      pygame.draw.line(screen, BLACK, (gridWidth, 0), (gridWidth, display_height), 1)
  for i in range(1,24):
      gridLength = i*(display_height/24)
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
   textRect.center = (100,590)
   screen.blit(text, textRect)

#a dictionary storing all the pedestrians i guess
dWidth = {}
dHeight = {}
dDirection = {}

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

      if not playerTurn:
          for i in range(pedestrianAmt):
              #decisions on probabilities
              if (dDirection["startingPedestrianHeight"+str(i)]) == 0:
                  directions = ["n"]*10 + ["e"]*10 + ["w"]*10 + ["s"]*70
              elif (dDirection["startingPedestrianHeight"+str(i)]) == display_height:
                  directions = ["n"]*70 + ["e"]*10 + ["w"]*10 + ["s"]*10
              (pedestrianMove) = directions[random.randint(0,99)]
              if ((pedestrianMove) == "n"):
                  dHeight["startingPedestrianHeight"+str(i)] = dHeight["startingPedestrianHeight"+str(i)] - 25
              elif ((pedestrianMove) == "s"):
                  dHeight["startingPedestrianHeight"+str(i)] = dHeight["startingPedestrianHeight"+str(i)] + 25
              elif (pedestrianMove == "e") and (dWidth["startingPedestrianWidth"+str(i)] is not display_width):
                  dWidth["startingPedestrianWidth"+str(i)] = dWidth["startingPedestrianWidth"+str(i)] + 25
              elif (pedestrianMove == "w") and (dWidth["startingPedestrianWidth"+str(i)] is not 0):
                  dWidth["startingPedestrianWidth"+str(i)] = dWidth["startingPedestrianWidth"+str(i)] - 25
              #end game  #mendelssohn violin concerto in e minor
              if ((dWidth["startingPedestrianWidth"+str(i)]-5) <=startingPlayerWidth <= (dWidth["startingPedestrianWidth"+str(i)]+5)) and ((dHeight["startingPedestrianHeight"+str(i)]-5) <=startingPlayerHeight <= (dHeight["startingPedestrianHeight"+str(i)]+5)):
                  pygame.display.quit()
          screen.fill(WHITE)
          drawGrid()
          drawPlayer()
          drawPedestrian()
          updateCounter()
          pygame.display.update()
          playerTurn = True

      for event in ev:
          if event.type == pygame.KEYDOWN:
              if playerTurn:
                  #stuff the player does || catch me w that malfunctioning boundary code
                  if (event.key == pygame.K_LEFT) and not (startingPlayerWidth <= 1):
                      startingPlayerWidth = startingPlayerWidth - 25
                  elif (event.key == pygame.K_RIGHT) and not (startingPlayerWidth >= display_width):
                      startingPlayerWidth = startingPlayerWidth + 25
                  elif (event.key == pygame.K_UP) and not (startingPlayerHeight <= 1):
                      startingPlayerHeight = startingPlayerHeight - 25
                  elif (event.key == pygame.K_DOWN) and not (startingPlayerHeight >= display_height):
                      startingPlayerHeight = startingPlayerHeight + 25
                  playerTurn = False
                  playerCounter = playerCounter + 1
                  if (playerCounter % 3) == 0:
                       pedestrianAmt = pedestrianAmt + 1
                       addPedestrian()
                       pedestrianCounter = pedestrianCounter + 1
          if event.type == pygame.QUIT:
              running = False

if __name__ == '__main__':
  main()

