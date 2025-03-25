import pytest
import os
from scr.decorators import log

def test_log_file():
    @log(filename="mylog.txt")
    def add(x, y):
        return x + y

    result = add(1, 2)
    assert result == 3

    with open("mylog.txt", "r") as f:
        assert "add ok" in f.read()

    os.remove("mylog.txt")

def test_log_console(capsys):
    @log()
    def add(x, y):
        return x + y

    result = add(1, 2)
    assert result == 3

    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_error(capsys):
    @log()
    def divide(x, y):
        return x / y

    result = divide(1, 0)
    assert result is None

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.err
