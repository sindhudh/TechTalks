import pytest

@pytest.fixture
def num():
    return [10,2,4]

def test_1(num):
    assert 10 == num[0]

def test_2(num):
    assert 9 in num