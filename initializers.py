import numpy as np

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TEXTCOLOR = (0, 0, 0)

display_width = 200
display_height = 300

QIDic = {}  # dictionary for the q-table

Q = np.zeros([768, 3])  # q-table to store state-action pair
