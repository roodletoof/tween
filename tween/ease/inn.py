'''
Collection of ease_in functions.
All functions use the ease.helper.clamp_decorator.
Named 'inn' because 'in' is a keyword.
'''


import math
from ease.helper import clamp_decorator, invert_decorator

@clamp_decorator
def sine(x: float) -> float:
    return 1 - math.cos((x * math.pi) / 2)

@clamp_decorator
def quad(x: float) -> float:
    return x**2

@clamp_decorator
def cubic(x: float) -> float:
    return x**3

@clamp_decorator
def quart(x: float) -> float:
    return x**4

@clamp_decorator
def quint(x: float) -> float:
    return x**5

@clamp_decorator
def expo(x: float) -> float:
    return 2**(10*x-10)

@clamp_decorator
def circ(x: float) -> float:
    return 1 - math.sqrt(1-x**2)

@clamp_decorator
def back(x: float) -> float:
    c1 = 1.70158
    c3 = c1 + 1
    return c3 * x**3 - c1 * x**2

@clamp_decorator
def elastic(x: float) -> float:
    c4 = 2*math.pi/3
    return -2**(10*x-10) * math.sin((x*10-10.75) * c4)


from ease.out import bounce
bounce = invert_decorator(bounce)