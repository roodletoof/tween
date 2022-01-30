'''
A collection of ease_out functions.
All functions use the ease.helper.clamp_decorator.
'''

from ease.helper import invert_decorator, clamp_decorator
from ease.inn import sine, quad, cubic, quart, quint, expo, circ, back, elastic

sine    = invert_decorator( sine    )
quad    = invert_decorator( quad    )
cubic   = invert_decorator( cubic   )
quart   = invert_decorator( quart   )
quint   = invert_decorator( quint   )
expo    = invert_decorator( expo    )
circ    = invert_decorator( circ    )
back    = invert_decorator( back    )
elastic = invert_decorator( elastic )


@clamp_decorator
def bounce(x: float) -> float:
    n1 = 7.5625
    d1 = 2.75
    if x<1/d1:
        return n1*x**2
    elif x<2/d1:
        x -= 1.5 / d1
        return n1 * x**2 + 0.75
    elif x<2.5/d1:
        x -= 2.25 / d1
        return n1 * x**2 + 0.9375
    else:
        x -= 2.625 / d1
        return n1 * x**2 + 0.984375
