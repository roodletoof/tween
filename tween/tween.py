from __future__ import annotations
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
    def __init__(self, container, key, is_object: bool, end_value: float, time: float, ease_type: str, delay: float, tween_instances_list: list[Tween]):
        self.container = container # A list, dictionary or other object
        self.key = key
        self.container_not_dict_or_list = is_object
        
        self.target_time = time
        self.time_lived = 0.0
        self.delay = delay
        
        self.ease_func = _function_dictionary[ease_type]
        
        self.end_value = end_value
        self.delete = False
        self.tween_instances_list = tween_instances_list
        self._first_time_this_runs = _make_generator_callable(_1_True_rest_is_False())


    def _ready_for_garbage_collection(self):
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
            if tween_instance is not self\
            and tween_instance.container is self.container\
            and tween_instance.key == self.key:
                tween_instance._ready_for_garbage_collection()
            

    def _update(self, dt):
        if self.delay > 0:
            self.delay -= dt
            return
        
        dt -= self.delay
        self.delay = 0

        if self._first_time_this_runs():
            self._delete_colliding_tweens()

            if self.container_not_dict_or_list:
                self.start_value = getattr(self.container, self.key)
            else:
                self.start_value = self.container[self.key]
            self.difference = self.end_value - self.start_value

        if not self.delete:
            self.time_lived += dt
            tween_value = self.difference * self.ease_func(min(1, self.time_lived / self.target_time))
            self._set_container_value(self.start_value + tween_value)

        if self.time_lived >= self.target_time:
            self._set_container_value(self.end_value)
            self._ready_for_garbage_collection()
            

    def stop(self) -> None:
        self._ready_for_garbage_collection()


class TweenController:
    def __init__(self, tweengroup: Group, *args, **kwargs):
        self.tweengroup = tweengroup
        self.args = args
        self.kwargs = kwargs
        self.tween: Tween = None
    
    def play(self):
        self.stop_tweens = self.tweengroup.to(*self.args, **self.kwargs)

    def stop(self):
        self.stop_tweens()



class Group:
    def __init__(self):
        self.tweens: list[Tween] = []

   
    def controllable(self, container, keys_and_values:dict, time:float, ease_type:str = 'easeOutQuad', delay:float = 0.0) -> TweenController:
        return TweenController(self, container, keys_and_values, time, ease_type, delay)


    def to(self, container, keys_and_values:dict, seconds:float, ease_type:str = 'easeOutQuad', delay:float = 0.0) -> function:
        '''
        Starts the tween(s), and returns a function to stop the tweens that started when this function was called.
        '''
        new_tween_instances:list[Tween] = []
        
        for key, end_value in keys_and_values.items():
            is_object = True
            if isinstance(container, dict) or isinstance(container, list):
                is_object = False
            
            tween_instance = Tween(container, key, is_object, end_value, seconds, ease_type, delay, self.tweens)
            
            self.tweens.append(tween_instance)
            new_tween_instances.append(tween_instance)
        
        def stop_tweens():
            for tween in new_tween_instances:
                tween.stop()
        
        return stop_tweens
    

    def update(self, dt) -> None:
        for tween_instance in self.tweens:
            tween_instance._update(dt)

        # Remove all finished tweens from the tween list
        del_counter = 0
        for index, tween in enumerate(self.tweens):
            if tween.delete:
                del_counter += 1
            else:
                self.tweens[index - del_counter] = tween
        for _ in range(del_counter):
            self.tweens.pop()

_default_group = Group
def controllable(*args, **kwargs):
    _default_group(*args, **kwargs)
def to(*args, **kwargs):
    _default_group(*args, **kwargs)
def update(*args, **kwargs):
    _default_group.update(*args, **kwargs)


def get_ease_types() -> tuple[str]:
    '''
    Returns a tuple of all available ease types.
    '''
    return tuple(_function_dictionary.keys())


# TESTING
if __name__ == '__main__':
    t = Group()
    man = {
        'x' : 0,
        'y' : 0,
    }
    t.to(man, {'x': 200, 'y': 400}, 5)
    for _ in range(1,100):
        print(f'{t.tweens = }')
        t.update(.1)
        print(f'{man = }')
    print(get_ease_types())
