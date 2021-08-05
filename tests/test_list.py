import tween

def test_false():
    mylist = [0.0]
    tween.to(mylist, 0, end_value = 10.0, time = 20.0)
    tween.update(10.0)
    assert mylist[0] != 2.5

def test_true():
    mylist = [0.0]
    tween.to(mylist, 0, end_value = 10.0, time = 20.0)
    tween.update(10.0)
    assert mylist[0] == 5.0
