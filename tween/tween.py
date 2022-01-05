import inspect
import pytweening

_function_dictionary = {} #Making all pytweening functions accessible by str name.
for name, func in inspect.getmembers(pytweening, inspect.isfunction):
    if not "_" == name[0] and\
    not "getLine" == name and\
    not "getPointOnLine" == name:
        _function_dictionary[name] = func

def _1_True_rest_is_False():
    yield True
    while True:
        yield False

def _make_generator_callable(gen):
    return lambda : next(gen)

class Tween:
    def __init__(self, container, key, is_object: bool, end_value: float, time: float, ease_type: str, delay: float, tween_instances_list: list['Tween']):
        self.container = container
        self.key = key
        self.container_not_dict_or_list = is_object
        
        self.target_time = time
        self.time_lived = 0.0
        self.delay = delay
        
        self.ease_func = _function_dictionary[ease_type]
        
        if self.container_not_dict_or_list:
            self.start_value = getattr(container, key)
        else:
            self.start_value = container[key]
        self.end_value = end_value
        self.difference = self.end_value - self.start_value
        
        self.delete = False
        
        self.tween_instances_list = tween_instances_list
        
        self._first_time_this_runs = _make_generator_callable(_1_True_rest_is_False())

    def _ready_for_garbage_collection(self):
        '''
        Marks this tween to be deleted, and removes references to objects and list
        so that the tween can be garbage collected.
        '''
        del self.container
        del self.tween_instances_list
        self.delete = True


    def _set_container_value(self, value):
        if self.container_not_dict_or_list:
            setattr(self.container, self.key, value)
        else:
            self.container[self.key] = value

    def _delete_colliding_tweens(self):
        for tween_instance in self.tween_instances_list:
            if tween_instance.container is self.container\
            and tween_instance.key == self.key:
                tween_instance._ready_for_garbage_collection()
            

    def _update(self, dt):
        '''
        Update the current value based on time passed since last update.
        Will alter specified value of the container this Tween is attatched to.
        '''

        if self.delay >= 0:
            self.delay -= dt
            return

        if self._first_time_this_runs():
            self._delete_colliding_tweens()

        if not self.delete:
            self.time_lived += dt
            tween_value = self.difference * self.ease_func(min(1, self.time_lived / self.target_time))
            self._set_container_value(self.start_value + tween_value)

        if self.time_lived >= self.target_time:
            self._set_container_value(self.end_value)
            self._ready_for_garbage_collection()
            

    def stop(self) -> None:
        '''
        Stop and delete tween.
        '''
        self._ready_for_garbage_collection()



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

def _update(passed_time: float, group: list[Tween]): #in seconds!
    for tween_instance in group:
        tween_instance._update(passed_time)

    #delete all finished tweens
    del_counter = 0
    for index, tween in enumerate(group):
        if tween.delete:
            del_counter += 1
        else:
            group[index - del_counter] = tween
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
    return tuple(_function_dictionary.keys())
