def test():
    import ease
    import numpy as np
    
    EASE_FUNC = ease.inout.bounce

    WIDTH = 70
    HEIGHT = 30

    NP_RANGE = np.linspace(0, 1, WIDTH)
    coords = {
        (
            round( x * ( WIDTH - 1 ) ),
            round( EASE_FUNC(x) * ( HEIGHT - 1 ) )
        ) : '*'
        for x in NP_RANGE
    }

    for y in reversed(range(HEIGHT)):
        for x in range(WIDTH):
            print(coords.get((x,y), ' '), end='')
        print()

test()