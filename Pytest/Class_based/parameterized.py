import pytest

def func_add(x,y):
    return x+y

@pytest.mark.parametrize("x,y",[(10,20)])
def test_add(x,y):
    assert 10 == func_add(x,y)

@pytest.mark.skip
def test_add():
    assert 10 == func_add(10,10)