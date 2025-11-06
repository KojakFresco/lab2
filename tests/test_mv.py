import logging

from _pytest.logging import LogCaptureFixture
from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.move import mv

def test_mv_wrong_syntax_error(caplog: LogCaptureFixture):
    mv(["i"], ["path", "path2"])
    assert caplog.records[-1].message == "Неверный синтаксис команды mv"

    mv([], ["path1"])
    assert caplog.records[-1].message == "Неверный синтаксис команды mv"


def test_mv_nonexisting_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_dir("path2")

    mv([], ["path1", "path2"])
    assert caplog.records[-1].message == "'path1' не существует"


def test_mv_subdir_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_dir("dir")
    fs.create_dir("dir\\sub")

    mv([], ["dir", "dir\\sub"])
    assert caplog.records[-1].message == "Нельзя переместить директорию 'dir' в свою поддиректорию 'dir\\sub'"


def test_mv_access_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_dir("dir", perm_bits=0o000)
    fs.create_dir("dir\\sub")

    mv([], ["dir", "dir2"])
    assert caplog.records[-1].message == "Отказано в доступе"


def test_mv_on_correct_case(caplog: LogCaptureFixture, fs: FakeFilesystem):
    caplog.set_level(logging.DEBUG)

    fs.create_dir("dir")
    fs.create_dir("dir2")

    mv([], ["dir", "dir2"])
    assert not fs.exists("dir") and fs.exists("dir2\\dir")
    assert caplog.records[-1].message == "SUCCESS"
