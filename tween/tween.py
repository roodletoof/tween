import inspect
import pytweening

function_dictionary = {} #Making all pytweening functions accessible by str name.
for item in inspect.getmembers(pytweening, inspect.isfunction):
    if not "_" == item[0][0] and\
    not "getLine" == item[0] and \
    not "getPointOnLine" == item[0]:
        #item[0] is function name of type str
        #item[1] id the actual function
        function_dictionary[item[0]] = item[1]


class Tween:
    def __init__(self, container, key, is_object: bool, end_value, time, ease_type, delay, tween_instances_list):
        self.is_object = is_object
        self.container = container
        self.key = key
        self.end_value = end_value
        self.time = time
        self.life = 0.0
        self.ease_type = ease_type
        self.delay = delay
        if self.is_object:
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
            if tween_instance.container is self.container and tween_instance.key == self.key:
                tween_instance._ready_for_garbage_collection()

    def _ready_for_garbage_collection(self):
        '''
        Do not call this function directly.
        '''
        del self.container
        del self.start_functions
        del self.update_functions
        del self.complete_functions
        self.delete = True

    def _update(self, dt):
        '''
        Do not call this function directly.
        Call tween.update() or Group.update()
        '''
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

                if self.is_object:
                    setattr(self.container, self.key, self.start_value + tween_value)
                    if self.life >= self.time:
                        setattr(self.container, self.key, self.end_value)
                        for function in self.complete_functions:
                            function()
                        self._ready_for_garbage_collection()
                else:
                    self.container[self.key] = self.start_value + tween_value
                    if self.life >= self.time:
                        self.container[self.key] = self.end_value
                        for function in self.complete_functions:
                            function()
                        self._ready_for_garbage_collection()
            else:
                self.delay -= dt

    def stop(self) -> None:
        '''
        Stops the tween from playing, and readies itself for garbage collection.
        '''
        self._ready_for_garbage_collection()

    def on_start(self, func) -> None:
        '''
        Add a function to run on the start of the tween.
        If the tween has already started, the function will not be called.
        The function will not be called with any arguments.
        You can add as many functions as you like.
        '''
        self.start_functions.append(func)

    def on_update(self, func) -> None:
        '''
        Add a function to run on every update.
        The function will not be called with any arguents.
        You can add as many functions as you like.
        '''
        self.update_functions.append(func)

    def on_complete(self, func) -> None:
        '''
        Add a function to run when the tween is completed.
        The function will not be called with any arguments.
        You can add as many functions as you like.
        '''
        self.complete_functions.append(func)


tweens = [] #Contains all instances of tween

def _to(container, key, end_value: float, time: float, ease_type: str, delay: float, group: list) -> Tween:
    if isinstance(container, dict):
        tween_instance = Tween(container, key, False, end_value, time, ease_type, delay, group)
        group.append(tween_instance)
        return tween_instance

    elif isinstance(container, list):
        if not isinstance(key, int):
            raise ValueError("You must index the list with an int.")
        tween_instance = Tween(container, key, False, end_value, time, ease_type, delay, group)
        group.append(tween_instance)
        return tween_instance

    else:
        if not isinstance(key, str):
            raise ValueError("You must index the object with a string.")
        tween_instance = Tween(container, key, True, end_value, time, ease_type, delay, group)
        group.append(tween_instance)
        return tween_instance

def to(container, key, end_value: float, time: float, ease_type: str = 'linear', delay: float = 0.0) -> Tween:
    '''
    Create a tween object and add it to the default tween group.
    The container argument can be a list, dictionary or object.
    The end_value is the final value of the containers key when the tween in finished.
    The time is how long the tween should take in seconds.
    The ease_type is the type if tweening that should be used. Run the tween module to get a list of all ease_types.
    The delay is how long the tween will wait to play.
    Only one tween per object attribute will ever be active.
    To restart a tween, this function must be called again.
    All tweens become unusable after they are finished, and ready themselves to be garbage collected.
    '''
    return _to(container, key, end_value, time, ease_type, delay, tweens)

def _update(passed_time: float, group: list): #in seconds!
    for tween_instance in group:
        tween_instance._update(passed_time)

    #delete all finished tweens
    del_counter = 0
    original_list_len = len(group)
    for item_key in range(original_list_len):
        item = group[item_key]
        if item.delete == True:
            del_counter += 1
        else:
            group[item_key - del_counter] = item
    for _ in range(del_counter):
        group.pop()

def update(passed_time: float) -> None:
    '''
    dt is the number of seconds since last update.
    Update all tweens in the default tween group.
    This will call all appropriate functions attatched to tweens, and end finished tweens.
    Finished tweens will be deleted from its group.
    '''
    _update(passed_time, tweens)


class Group:
    '''
    A group of tweens.
    The group has its own .to and .update methods.
    This is usefull if you want to continue playing some tweens while pausing other tweens.
    '''
    def __init__(self):
        self.tweens = []
    def to(self, container, key, end_value, time, ease_type = "linear", delay = 0.0) -> Tween:
        '''
        Create a tween object and add it to this tween group.
        The container argument can be a list, dictionary or object.
        The end_value is the final value of the containers key when the tween in finished.
        The time is how long the tween should take in seconds.
        The ease_type is the type if tweening that should be used. Run the tween module to get a list of all ease_types.
        The delay is how long the tween will wait to play.
        Only one tween per object attribute will ever be active.
        To restart a tween, this function must be called again.
        All tweens become unusable after they are finished, and ready themselves to be garbage collected.
        '''
        _to(container, key, end_value, time, ease_type, delay, self.tweens)
    def update(self, dt) -> None:
        '''
        dt is the number of seconds since last update.
        Update all tweens in this tween group.
        This will call all appropriate functions attatched to tweens, and end finished tweens.
        Finished tweens will be deleted from its group.
        '''
        _update(dt, self.tweens)


def get_ease_types() -> tuple[str]:
    '''
    Returns a tuple of all available ease types.
    '''
    return tuple(function_dictionary.keys())
