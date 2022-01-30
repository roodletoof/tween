'''
A collection of easing functions and helper functions to create your own easing functions.
Each easing function takes a single float argument and returns a float value.
The argument is always clamped between 0.0 and 1.0.
Some functions might return values higher than 1.0 or lower than 0.0.
But all functions will return 1.0 if 1.0 or higher is passed as an argument,
or return 0.0 if 0.0 or lower is passed as an argument.
'''

from ease import inn
from ease import out
from ease import inout
from ease import helper