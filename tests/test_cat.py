import shutil

import pytest
from _pytest.logging import LogCaptureFixture
from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.cat import cat

def test_cat_wrong_syntax_error(caplog: LogCaptureFixture):
    cat(["i"], ["path"])
    assert caplog.records[-1].message == "Неверный синтаксис команды cat"

    cat([], ["path1", "path2"])
    assert caplog.records[-1].message == "Неверный синтаксис команды cat"


def test_cat_on_dir(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_dir("dir")

    cat([], ["dir"])
    assert caplog.records[-1].message == "'dir' это директория"


def test_cat_on_nonexisting_file(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_file("existing")

    cat([], ["nonexisting"])
    assert caplog.records[-1].message == "'nonexisting' не существует"


def test_cat_on_wrong_encoding(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_file("file", contents="Hello world")

    shutil.make_archive("file", "zip")

    cat([], ["file.zip"])
    assert caplog.records[-1].message == "Не получилось расшифровать файл в кодировке utf-8"


def test_cat_correct_output(capsys: pytest.CaptureFixture, fs: FakeFilesystem):
    fs.create_file("file", contents="Hello world")

    cat([], ["file"])
    assert capsys.readouterr().out == "Hello world\n"