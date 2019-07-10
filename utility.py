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
import numpy
from pygame.constants import K_DOWN, K_UP, KEYDOWN, KEYUP, QUIT
import pygame.surfarray
import pygame.key

def combineFunc(screenUpdate, interceptScreen):
    def wrap(*args, **kwargs):
        screenUpdate(*args, **kwargs) # call the screen update func we intercepted so the screen buffer is updated
        interceptScreen() # call our own function to get the screen buffer
    return wrap

def on_screen_update():
    surface_array = pygame.surfarray.array3d(pygame.display.get_surface())
    print("We got the screen array")
    print(surface_array)

def getAction(incterceptFunc, receiveFunc):
    """
    Intercepts a method call and calls the supplied intercepting_func with the result of it's call and it's arguments
    Example:
        def get_event(result_of_real_event_get, *args, **kwargs):
            # do work
            return result_of_real_event_get
        pygame.event.get = function_intercept(pygame.event.get, get_event)
    :param intercepted_func: The function we are going to intercept
    :param intercepting_func:   The function that will get called after the intercepted func. It is supplied the return
    value of the intercepted_func as the first argument and it's args and kwargs.
    :return: a function that combines the intercepting and intercepted function, should normally be set to the
             intercepted_functions location
    """

    def wrap(*args, **kwargs):
        result = incterceptFunc(*args, **kwargs)  # call the function we are intercepting and get it's result
        interceptResult = receiveFunc(result, *args, **kwargs)  # call our own function a
        return interceptResult

    return wrap

