# Dodgy Sidewalk
---
Final project for AI course at SPCS.

## Description
A bot that can optimally dodge “pedestrians” coming in from random positions
on the top and bottom of the screen; these pedestrians then move in random cartesian (NSEW) directions
(i.e. the bot has to navigate optimally through these walkers. If the bot hits a pedestrian, the “game” ends.
After certain time periods, the speed of the pedestrians will increase and how often they turn also increases.
More pedestrians will also begin to appear as time goes on. A score counter will gradually increase as time progresses.

## Method / Components
Basic game interface and infrastructure are built with pygame.
Due to the random nature of the "pedestrian" agents, the bot uses model-based reinforcement learning ~~and Hidden Markov models~~
to find the optimal path.

## Authors
Anthony Kim, Jedd Hui, Amy Dong
