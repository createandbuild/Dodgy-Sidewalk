# def maximum(a,b):
#     if a>b:
#         return a
#     else:
#         return b
#
# def minimum(a,b):
#     if a>b:
#         return b
#     else:
#         return a
#
# def clamp(number,lower_bound,upper_bound):
#     new_num = number
#     new_num = maximum(lower_bound,new_num)
#     new_num = minimum(upper_bound,new_num)
#     return new_num

import pygame
import pygame.surfarray

def combineFunc(screenUpdate, interceptScreen):
    def wrap(*args, **kwargs):
        screenUpdate(*args, **kwargs) # call the screen update func we intercepted so the screen buffer is updated
        interceptScreen() # call our own function to get the screen buffer
    return wrap

def on_screen_update():
    surface_array = pygame.surfarray.array3d(pygame.display.get_surface())
    print("We got the screen array")
    print(surface_array)

