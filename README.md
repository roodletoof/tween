# tween
A tweening library inspired by flux by rxi. Using the PyTweening module by AlSweigart.
### Installing
`pip install tween`

### Example using a pygame setup

```python
import sys
import pygame
from pygame.locals import *
import tween

pygame.init()
screen = pygame.display.set_mode(400,400)
clock = pygame.time.Clock()
dt = 0.0

class Character:
  def __init__(self, surface, x, y):
    self.sprite = surface
    self.x = x
    self.y = y

  def draw(surface):
    surface.blit(self.sprite, (self.x, self.y))

hero_image = pygame.image.load("path/to/image.png")
hero = Character(hero_image, 0, 200)
hero_tween = tween.to(hero, "x", 400, 5.0, "easeInOutQuad") #Starting a tween.

def say_message():
  print("Started moving!")
hero_tween.on_start(say_message) #Adding function that runs at the start of the tween-
  #.on_start() will only have an effect if you call it before the first time the tween is updated

def update(dt):
  tween.update(dt) #Updating all active tweens within the default group

def draw(surface):
  surface.fill(0,0,0)
  hero.draw(surface)
  pygame.display.flip()

while 1:
  for event in pygame.event.get():
    if event.type == QUIT:
     sys.exit()
  update(dt)
  draw(screen)
  dt = clock.tick(60) / 1000.0 #Divide by 1000.0 to get dt (time_passed) in seconds

```
Unless there is a typo in my code, the **hero** object should move from **(y = 200, x = 0) to (y = 200, x = 400)** in the span of exactly 5 seconds. Using **"easeInOutQuad"** the sprite will slowly accelerate and decelerate.


### Functions and classes
```python
tween.to(container, key, final_value, time, easing_type = "linear", _group = tween.tweens) --> tween.Tween
```

Creates and adds a Tween object to the default tween module group.

The **container** argument can be a list, dictionary or object.
1.  If the **container** is a list, the **key** must be an integer.
2.  If the **container** is a dictionary, the **key** must be a string.
3.  If the **container** is an object, the **key** must be a string.

**final_value** is the target value the tween will stop at.

**time** is how long the tween should take to finish in _seconds_.

**easing_type** is a string describing the easing function you want to use. There is a list of all types at the bottom of this readme.

 _The **_group** argument should not be passed._

Instead you should create an instance of the **tween.Group** class, and call its **.to** method

```python
tweening_group = tween.Group()

tweening_group.to(container, key, final_value, time_in_seconds, easing_type = "linear") --> tween.Tween
```

The tween module and all instances of **tween.Group** has an **update** function/method.

```python
tween.update(passed_time, _group = tween.tweens)
```
```python
tween.Group.update(passed_time)
```

_The **_group** argument should not be passed here either. The tween module will pick the rigth group for you._

**passed_time** is the time since the last update was called in _seconds_.

If you want to pause all tweens within a certain group, it is as simple as not calling the **.update** method for that group.

The **tween.Tween** object returned from the **.to** function/method has a couple methods of its own.

```python
tween.Tween.stop() #stops and deletes the tween from its group.
tween.Tween.on_start(func) #appends a function that runs at the start of the tween.
tween.Tween.on_update(func) #appends a function that runs every update.
tween.Tween.on_complete(func) #appends a function that runs at the end of the tween.
```

You can append as many functions as you like.

### Easing types
1. easeInBack
2. easeInBounce
3. easeInCirc
4. easeInCubic
5. easeInElastic
6. easeInExpo
7. easeInOutBack
8. easeInOutBounce
9. easeInOutCirc
10. easeInOutCubic
11. easeInOutElastic
12. easeInOutExpo
13. easeInOutQuad
14. easeInOutQuart
15. easeInOutQuint
16. easeInOutSine
17. easeInQuad
18. easeInQuart
19. easeInQuint
20. easeInSine
21. easeOutBack
22. easeOutBounce
23. easeOutCirc
24. easeOutCubic
25. easeOutElastic
26. easeOutExpo
27. easeOutQuad
28. easeOutQuart
29. easeOutQuint
30. easeOutSine
31. linear

If you want to get a list of all the easing types without reading this readme, you can do:
```python
tween.print_ease_types()
```
or simply run the module directly in the terminal: `python3 -m tween`
