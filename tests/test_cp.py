import logging

from _pytest.logging import LogCaptureFixture
from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.move import cp

def test_cp_wrong_syntax_error(caplog: LogCaptureFixture):
    cp(["i"], ["path"])
    assert caplog.records[-1].message == "Неверный синтаксис команды cp"

    cp(["i", "o"], ["path1", "path2"])
    assert caplog.records[-1].message == "Неверный синтаксис команды cp"


def test_cp_same_path_error(caplog: LogCaptureFixture):
    cp(["r"], ["path", "path"])
    assert caplog.records[-1].message == "'path' и 'path' - это один и тот же путь"


def test_cp_wrong_option_error(caplog: LogCaptureFixture):
    cp(["i"], ["path", "path2"])
    assert caplog.records[-1].message == "Неверная опция 'i'"


def test_cat_nonexisting_file_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_file("existing")

    cp(["r"], ["nonexisting", "new"])
    assert caplog.records[-1].message == "'nonexisting' не существует"


def test_cat_no_r_key_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_dir("dir")

    cp([], ["dir", "new"])
    assert caplog.records[-1].message == "Не указан ключ -r. Невозможно скопировать"


def test_cat_no_access_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_dir("dir")
    fs.create_dir("dir\\dir2", perm_bits=0o000)
    fs.create_file("dir\\file2")

    cp(["r"], ["dir", "new"])
    assert len(caplog.records) == 1
    assert caplog.records[-1].message == "Отказано в доступе"


def test_cat_on_correct_case(caplog: LogCaptureFixture, fs: FakeFilesystem):
    caplog.set_level(logging.DEBUG)

    fs.create_dir("dir")
    fs.create_dir("dir\\dir2")
    fs.create_file("dir\\file")
    fs.create_file("dir\\dir2\\file", contents="text_test")

    cp(["r"], ["dir", "new"])
    assert fs.exists("new\\file")
    with open("new\\dir2\\file", 'r') as f:
        assert f.read() == "text_test"
    assert len(caplog.records) == 1
    assert caplog.records[-1].message == "SUCCESS"