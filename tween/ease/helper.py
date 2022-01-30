'''
Helper functions for creating ease functions.
All of these functions takes a function or multiple functions, and returns a new function.
'''


from typing import Callable

EASE_FUNCTION = Callable[[float],float]

def clamp_decorator(func: EASE_FUNCTION) -> EASE_FUNCTION:
    '''
    Decorator that supports functions with 1 float argument.
    The new function clamps the argument between 0 and 1.
    Also if the argument is <= 0.0 or >= 1.0 then this new function 
    just returns 0.0 or 1.0 instead of running any calcualtions on it.
    '''
    def new_func(x: float) -> float:
        x = max(min(x, 1), 0)
        if 0 < x < 1:
            return func(x) 
        return float(x)
    return new_func

def invert_decorator(func: EASE_FUNCTION) -> EASE_FUNCTION:
    '''
    Inverts a given function.
    The new function's return value is: 1 - func(1-x).
    If the original function had a clamp decorator, there is no need to re-apply that
    decorator to the new function.
    '''
    def new_func(x: float) -> float:
        return 1 - func(1-x)
    return new_func

def make_inout_function(infunc: EASE_FUNCTION, outfunc: EASE_FUNCTION) -> EASE_FUNCTION:
    '''
    Takes an ease in function and an ease out function,
    and returns a new function that combines the two.
    This can be used to ease in using one method, and ease out using another.
    Only works if both functions have the clamp decorator.
    '''
    def new_func(x: float) -> float:
        x *= 2
        return (infunc(x) + outfunc(x-1)) / 2
    return new_func