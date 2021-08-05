import tween

class My_class:
    def __init__(self):
        self.a = 0.0

def test_false():
    myobj = My_class()
    tween.to(myobj, "a", end_value = 10.0, time = 20.0)
    tween.update(10.0)
    assert myobj.a != 2.5

def test_true():
    myobj = My_class()
    tween.to(myobj, "a", end_value = 10.0, time = 20.0)
    tween.update(10.0)
    assert myobj.a == 5.0
