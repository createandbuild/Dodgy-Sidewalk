import numpy as np

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TEXTCOLOR = (0, 0, 0)

display_width = 200
display_height = 300

possibleX = [0, 25, 50, 75, 100, 125, 150, 175, display_width]
pedestrianX = np.random.choice(possibleX, 1, p=[0.1, 0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1])

possibleY = [0, display_height]
pedestrianY = np.random.choice(possibleY, 1, p=[0.5, 0.5])

possibleAct = [2, -2, 1, -1]    # up, down, right, left

if pedestrianY[0] == 0:
    pedestrianAct = np.random.choice(possibleAct, 1, p=[0.7, 0.1, 0.1, 0.1])
elif pedestrianY[0] == display_height:
    pedestrianAct = np.random.choice(possibleAct, 1, p=[0.1, 0.7, 0.1, 0.1])

pedestrianXStep = 0
pedestrianYStep = 0

if possibleAct[0] == 2:
    pedestrianYStep = 25
elif possibleAct[0] == -2:
    pedestrianYStep = -25
elif possibleAct[0] == 1:
    pedestrianXStep = 25
elif possibleAct[0] == -1:
    pedestrianXStep = -25


QIDic = {}  # dictionary (index) for the q-table

Q = np.zeros([768, 3])  # q-table to store state-action pair
