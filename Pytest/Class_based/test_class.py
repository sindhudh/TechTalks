import pytest
def func():
    return "Welcome"

class TestCases:
    @pytest.mark.one
    def test_1(self):
        assert func() == "Welcome"
    @pytest.mark.two
    def test_2(self):
        assert "x" in  func()