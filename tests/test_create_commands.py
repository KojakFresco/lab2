import logging
from _pytest.logging import LogCaptureFixture
from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.create import touch, mkdir

def test_touch_wrong_syntax_error(caplog: LogCaptureFixture):
    touch(["i"], ["newfile"])
    assert caplog.records[-1].message == "Неверный синтаксис команды touch"

    touch([], ["newfile", "file"])
    assert caplog.records[-1].message == "Неверный синтаксис команды touch"


def test_touch_existing_file_is_ok(caplog: LogCaptureFixture, fs: FakeFilesystem):
    caplog.set_level(logging.DEBUG)

    fs.create_dir("home")
    fs.create_file("home\\newfile", contents="test")

    touch([], ["home\\newfile"])
    assert caplog.records[-1].message == "SUCCESS"


def test_touch_new_file_is_created(fs: FakeFilesystem):
    fs.create_dir("home")

    touch([], ["home\\newfile"])
    assert fs.exists("home\\newfile")


def test_mkdir_wrong_syntax_error(caplog: LogCaptureFixture):
    mkdir(["l"], ["dir"])
    assert caplog.records[-1].message == "Неверный синтаксис команды mkdir"

    mkdir([], ["dir", "newdir"])
    assert caplog.records[-1].message == "Неверный синтаксис команды mkdir"


def test_mkdir_existing_file_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_dir("home")
    fs.create_file("home\\newfile", contents="test")

    mkdir([], ["home\\newfile"])
    assert caplog.records[-1].message == "Не удалось создать директорию: Существует файл с названием 'home\\newfile'"

def test_mkdir_existing_dir_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_dir("home")
    fs.create_dir("home\\newdir")

    mkdir([], ["home\\newdir"])
    assert caplog.records[-1].message == "Директория 'home\\newdir' уже существует"

def test_mkdir_new_file_is_created(fs: FakeFilesystem):
    fs.create_dir("home")

    mkdir([], ["home\\newdir"])
    assert fs.exists("home\\newdir")