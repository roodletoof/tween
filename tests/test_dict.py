import tween

def test_false():
    mydict = {"a" : 0.0}
    tween.to(mydict, "a", end_value = 10.0, time = 20.0)
    tween.update(10.0)
    assert mydict["a"] != 2.5

def test_true():
    mydict = {"a" : 0.0}
    tween.to(mydict, "a", end_value = 10.0, time = 20.0)
    tween.update(10.0)
    assert mydict["a"] == 5.0
