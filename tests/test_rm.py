import logging
import shutil

import pytest
from _pytest.logging import LogCaptureFixture
from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.move import rm

def test_rm_wrong_syntax_error(caplog: LogCaptureFixture):
    rm(["i", "r"], ["path"])
    assert caplog.records[-1].message == "Неверный синтаксис команды rm"

    rm([], ["path", "path2"])
    assert caplog.records[-1].message == "Неверный синтаксис команды rm"


def test_rm_nonexisting_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_dir("existing")

    rm([], ["nonexisting"])
    assert caplog.records[-1].message == "'nonexisting' не существует"


def test_rm_wrong_option_error(caplog: LogCaptureFixture):
    rm(["i"], ["dir"])
    assert caplog.records[-1].message == "Неверная опция 'i'"


def test_rm_dir_without_r_option_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_dir("dir")

    rm([], ["dir"])
    assert caplog.records[-1].message == "Невозможно удалить 'dir': это директория"


def test_rm_access_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_file("file")
    fs.chmod("file", 0o000)

    rm(["r"], ["file"])
    assert caplog.records[-1].message == "Отказано в доступе"

#TODO: correct case