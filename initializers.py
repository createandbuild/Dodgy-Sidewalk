import numpy as np

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TEXTCOLOR = (0, 0, 0)

display_width = 200
display_height = 300

pedestrianX = 150
pedestrianY = 0

possibleAct = [2, -2, 1, -1]    # up, down, right, left
pedestrianAct = np.random.choice(possibleAct, 1, p=[0.1, 0.7, 0.1, 0.1])


QIDic = {}  # dictionary (index) for the q-table

Q = np.zeros([768, 3])  # q-table to store state-action pair
