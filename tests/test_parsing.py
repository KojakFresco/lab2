import pytest
from src.parser import parse

def test_parser():
    assert parse("", "") == 0
    assert parse("ls  -l \"new file\"", "") == {"fun": "ls", "options": ["l"], "args": ["new file"]}
    assert parse("ls \"new file", "") == 0
