# Dodgy Sidewalk
Final project for AI course at SPCS.
Pretty dodgy.

## Description
A bot that optimally dodges "pedestrian" agents by finding an optimal path through them. The "pedestrian" agents
enter the game screen from the top and bottom and move in random (NSEW) directions. The program ends once the bot
cannot find a path (i.e. trapped) and cannot dodge a "pedestrian." After certain turns of moves, the speed and randomness
of the agents' motion will increase, making it harder for the bot to navigate through them. A score counter will add points/rewards
for the bot as turns progress.

## Method / Components
Basic game interface and infrastructure are built with pygame.
Due to the random nature of the "pedestrian" agents, the bot uses model-based reinforcement learning ~~and Hidden Markov models~~
to find the optimal path.

## Team
Anthony Kim, Jedd Hui, Amy Dong
