from __future__ import annotations
from tween.ease.helper import EASE_FUNCTION
from tween import ease

def _1_True_rest_is_False():
    yield True
    while True:
        yield False

def _make_generator_callable(gen):
    return lambda : next(gen)

class Tween:
    def __init__(self, container, key, is_object: bool, end_value: float, time: float, ease_func: EASE_FUNCTION, delay: float, tween_instances_list: list[Tween]):
        self.container = container # A list, dictionary or other object
        self.key = key
        self.delay = delay

        self.__container_not_dict_or_list = is_object
        
        self.__target_time = time
        self.__time_lived = 0.0
        
        self.__ease_func = ease_func
       
        self.__end_value = end_value
        self.__tween_instances_list = tween_instances_list
        self.__first_time_this_runs = _make_generator_callable(_1_True_rest_is_False())

        self.__on_complete_functions = []
        
        self.delete = False


    def __ready_for_garbage_collection(self):
        del self.container
        del self.__tween_instances_list
        self.delete = True


    def __set_container_value(self, value):
        if self.__container_not_dict_or_list:
            setattr(self.container, self.key, value)
        else:
            self.container[self.key] = value

    def __get_container_value(self):
        if self.__container_not_dict_or_list:
            return getattr(self.container, self.key)
        else:
            return self.container[self.key]


    def __delete_colliding_tweens(self):
        for tween_instance in self.__tween_instances_list:
            if tween_instance.delete\
            or tween_instance.delay > 0\
            or tween_instance is self:
                continue
            
            if tween_instance.container is self.container\
            and tween_instance.key == self.key:
                tween_instance.stop()
            

    def update(self, dt):
        if self.delay > 0:
            self.delay -= dt
            return
        
        dt -= self.delay
        self.delay = 0

        if self.__first_time_this_runs():
            self.__delete_colliding_tweens()
            self.__start_value = self.__get_container_value()
            self.__difference = self.__end_value - self.__start_value

        if not self.delete:
            self.__time_lived += dt
            tween_value = self.__difference * self.__ease_func(self.__time_lived / self.__target_time)
            self.__set_container_value(self.__start_value + tween_value)

        if self.__time_lived >= self.__target_time:
            self.__ready_for_garbage_collection()
            for func in self.__on_complete_functions:
                func()
            

    def stop(self) -> None:
        self.__ready_for_garbage_collection()

    def on_complete(self, func: callable) -> None:
        self.__on_complete_functions.append(func)


class Controller:
    def __init__(self, tweens:list[Tween]):
        self.tweens = tweens
    
    def stop(self) -> None:
        for tween in self.tweens:
            tween.stop()
    
    def on_complete(self, func:callable) -> None:
        self.tweens[0].on_complete(func)


class Group:
    def __init__(self):
        self.tweens: list[Tween] = []
        self.last_tween_finished_at = 0 #Seconds
        self.last_tween_started_at = 0 #Seconds
        # Both of these variables are relative to current time.
        # So if Group.update(3) was called widthout any tweens starting, these variables would be -3


    def to(self, container, seconds:float, keys_and_values:dict, ease_func:EASE_FUNCTION = ease.out.quad, delay:float = 0.0) -> Controller:
        '''
        Starts the tween(s), and returns a function to stop the tweens that started when this function was called.
        Returns Controller obj.
        '''
        is_object = True
        if isinstance(container, dict) or isinstance(container, list):
            is_object = False
        
        new_tween_instances:list[Tween] = []

        for key, end_value in keys_and_values.items():
            tween_instance = Tween(container, key, is_object, end_value, seconds, ease_func, delay, self.tweens)
            self.tweens.append(tween_instance)
            new_tween_instances.append(tween_instance)
        
        self.last_tween_finished_at = delay + seconds
        self.last_tween_started_at = delay

        return Controller(new_tween_instances)


    def after(self, container, seconds:float, keys_and_values:dict, ease_func:EASE_FUNCTION = ease.out.quad, delay:float = 0.0) -> Controller:
        '''
        Initiate a tween that starts when the last tween created ends + given delay.
        Returns function to stop tween.
        '''
        delay = delay + self.last_tween_finished_at
        return self.to(container, seconds, keys_and_values, ease_func, delay)
    
    def at(self, container, seconds:float, keys_and_values:dict, ease_func:EASE_FUNCTION = ease.out.quad, delay:float = 0.0) -> Controller:
        '''
        Initiate a tween that starts at the same time as the previous tween created + given delay.
        Returns function to stop tween.
        '''
        delay = delay + self.last_tween_started_at
        return self.to(container, seconds, keys_and_values, ease_func, delay)

    def update(self, dt) -> None:
        '''
        Update all tweens within this group.
        dt = time passed in seconds since last update.
        '''

        for tween_instance in self.tweens:
            tween_instance._update(dt)

        self.last_tween_finished_at -= dt
        self.last_tween_started_at -= dt

        # Remove all finished tweens from the tween list
        del_counter = 0
        for index, tween in enumerate(self.tweens):
            if tween.delete:
                del_counter += 1
            else:
                self.tweens[index - del_counter] = tween
        for _ in range(del_counter):
            self.tweens.pop()

main = Group()