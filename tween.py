import inspect
import pytweening

function_dictionary = {} #Making all pytweening functions accessible as a str index
for item in inspect.getmembers(pytweening, inspect.isfunction):
    if not "_" == item[0][0]: #dismissing local functions
        #item[0] is function name of type str
        #item[1] id the actual function
        function_dictionary[item[0]] = item[1]


class Tween:

    def __init__(self, container, key, is_class: bool, end_value, time, ease_type, delay, tween_instances_list):
        self.container = container
        self.key = key
        self.is_class = is_class
        self.end_value = end_value
        self.time = time
        self.life = 0.0
        self.ease_type = ease_type
        self.delay = delay
        if self.is_class:
            self.start_value = getattr(container, key)
        else:
            self.start_value = container[key]
        self.difference = self.end_value - self.start_value
        self.delete = False

        self.has_started = False
        self.start_functions = []
        self.update_functions = []
        self.complete_functions = []

        for tween_instance in tween_instances_list:
            if tween_instance.container == self.container and tween_instance.key == self.key:
                tween_instance.delete = True


    def update(self, dt):
        if not self.delete:
            if self.delay <= 0.0:

                if self.has_started == False:
                    for function in self.start_functions:
                        function()
                    self.has_started = True

                for function in self.update_functions:
                    function()

                self.life += dt
                tween_value = self.difference * function_dictionary[self.ease_type](min(1, self.life / self.time))

                if self.is_class:
                    setattr(self.container, self.key, self.start_value + tween_value)
                    if self.life >= self.time:
                        setattr(self.container, self.key, self.end_value)
                        self.delete = True
                        for function in self.complete_functions:
                            function()
                else:
                    self.container[self.key] = self.start_value + tween_value
                    if self.life >= self.time:
                        self.container[self.key] = self.end_value
                        self.delete = True
                        for function in self.complete_functions:
                            function()
            else:
                self.delay -= dt

    def stop(self):
        self.delete = True

    def on_start(self, func):
        self.start_functions.append(func)

    def on_update(self, func):
        self.update_functions.append(func)

    def on_complete(self, func):
        self.complete_functions.append(func)


tweens = [] #Contains all instances of tween

def to(container, key, end_value, time, ease_type = "linear", delay = 0.0, _group = tweens):
    if isinstance(container, dict):
        if not isinstance(key, str):
            raise ValueError("You must index the dictionary with a string.")
        tween_instance = Tween(container, key, False, end_value, time, ease_type, delay, _group)
        _group.append(tween_instance)
        return tween_instance

    elif isinstance(container, list):
        if not isinstance(key, int):
            raise ValueError("You must index the list with an int.")
        tween_instance = Tween(container, key, False, end_value, time, ease_type, delay, _group)
        _group.append(tween_instance)
        return tween_instance

    else:
        if not isinstance(key, str):
            raise ValueError("You must index the class with a string.")
        tween_instance = Tween(container, key, True, end_value, time, ease_type, delay, _group)
        _group.append(tween_instance)
        return tween_instance


def update(dt, _group = tweens): #in seconds!
    for tween_instance in _group:
        tween_instance.update(dt)

    #delete all finished tweens
    _group = [tween for tween in _group if tween.delete == False]




class Group:
    def __init__(self):
        self.tweens = []
    def to(self, container, key, end_value, time, ease_type = "linear", delay = 0.0):
        to(container, key, end_value, time, ease_type, delay, self.tweens)
    def update(self, dt):
        update(dt, self.tweens)


def print_ease_type_functions():
    for item in inspect.getmembers(pytweening, inspect.isfunction):
        if not "_" == item[0][0]: #dismissing local functions
            print(item[0] + "(float between 0 and 1) --> float")


if __name__ == '__main__':
    print_ease_type_functions()
