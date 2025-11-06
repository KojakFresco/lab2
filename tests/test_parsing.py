from _pytest.logging import LogCaptureFixture

from src.parser import parse

def test_parsing_bad_cases(caplog: LogCaptureFixture):
    assert parse("", "") == 0

    assert parse("ls \"new file", "") == 0
    assert caplog.records[-1].message == "Некорректный ввод"

def test_parsing_separating():
    assert parse("ls  -l \"new file\"", "") == {"fun": "ls", "options": ["l"], "args": ["new file"]}