import pytest
from _pytest.logging import LogCaptureFixture
from pyfakefs.fake_filesystem import FakeFilesystem

import colorama
from src.commands.ls import ls

def test_ls_wrong_syntax_error(caplog: LogCaptureFixture):
    ls(["i", "l"], ["path"])
    assert caplog.records[-1].message == "Неверный синтаксис команды ls"

    ls([], ["path1", "path2"])
    assert caplog.records[-1].message == "Неверный синтаксис команды ls"


def test_ls_for_nonexisting_dir(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_dir("home")
    fs.create_dir("home\\existing")

    ls([], ["home\\nonexisting"])
    assert caplog.records[-1].message == "Директории 'home\\nonexisting' не существует"

    fs.create_file("home\\newfile", contents="test")

    ls([], ["home\\newfile"])
    assert caplog.records[-1].message == "Директории 'home\\newfile' не существует"


def test_ls_wrong_option(caplog: LogCaptureFixture):
    ls(["u"], ["path"])
    assert caplog.records[-1].message == "Неверная опция 'u'"

def test_ls_correct_output(capsys: pytest.CaptureFixture, fs: FakeFilesystem):
    fs.create_dir("home")
    fs.create_dir("home\\dir")
    fs.create_file("home\\file 1")
    fs.create_file("home\\file2.zip")

    ls([], ["home"])
    assert capsys.readouterr().out == f"{colorama.Fore.BLUE + "dir"}  'file 1'  {colorama.Fore.RED + "file2.zip"}  \n"

    #TODO ls(["l"], ["home"])