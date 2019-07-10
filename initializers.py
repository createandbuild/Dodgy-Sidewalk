import numpy as np

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TEXTCOLOR = (0, 0, 0)

display_width = 200
display_height = 300

# specify circle properties
# crclCentreX = 400
# crclCentreY = 50
# crclRadius = 20
#
# crclYStepFalling = windowHeight / 10  # 40 pixels each time
#
# # specify rectangle properties
# rctLeft = 400
# rctTop = 350
# rctWidth = 200
# rctHeight = 50

QIDic = {}  # dictionary for index of the q-table

Q = np.zeros([768, 3])  # q-table to store state-action pair
