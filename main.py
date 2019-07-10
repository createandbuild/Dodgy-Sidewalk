from utility import *
from game import *

pygame.display.update = combineFunc(pygame.display.update, on_screen_update)


if __name__ == '__main__':
  main()
