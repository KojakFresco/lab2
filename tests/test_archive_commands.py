import logging
import shutil
import tarfile

from _pytest.logging import LogCaptureFixture
from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.archive import zip, unzip, tar, untar

def test_zip_wrong_syntax_error(caplog: LogCaptureFixture):
    zip(["i"], ["path", "path2"])
    assert caplog.records[-1].message == "Неверный синтаксис команды zip"

    zip([], ["path"])
    assert caplog.records[-1].message == "Неверный синтаксис команды zip"


def test_zip_nonexisting_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_dir("existing")

    zip([], ["nonexisting", "new"])
    assert caplog.records[-1].message == "'nonexisting' не существует"


def test_zip_on_correct_cases(caplog: LogCaptureFixture, fs: FakeFilesystem):
    caplog.set_level(logging.DEBUG)

    fs.create_dir("dir")

    zip([], ["dir", "new"])
    assert fs.exists("new.zip")
    assert caplog.records[-1].message == "SUCCESS"

    zip([], ["dir", "dir2.zip"])
    assert fs.exists("dir2.zip")
    assert caplog.records[-1].message == "SUCCESS"

# Why isn't working?
# def test_zip_access_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
#     fs.create_dir("dir")
#     fs.create_file("dir\\file")
#     fs.chmod("dir\\file", 0o000)
#
#     zip([], ["dir", "dir.zip"])
#     assert caplog.records[-1].message == "Отказано в доступе"


def test_unzip_wrong_syntax_error(caplog: LogCaptureFixture):
    unzip(["i"], ["path"])
    assert caplog.records[-1].message == "Неверный синтаксис команды unzip"

    unzip([], ["path", "path2"])
    assert caplog.records[-1].message == "Неверный синтаксис команды unzip"


def test_unzip_nonexisting_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_file("existing.zip")

    unzip([], ["nonexisting.zip"])
    assert caplog.records[-1].message == "'nonexisting.zip' не существует"


def test_unzip_wrong_format_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_file("file", contents="test")

    unzip([], ["file"])
    assert caplog.records[-1].message == "Неверный формат файла"


def test_unzip_access_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_file("file", contents="test_text")
    shutil.make_archive("file", "zip")
    fs.chmod("file.zip", 0o000)

    unzip([], ["file.zip"])
    assert caplog.records[-1].message == "Отказано в доступе"


def test_tar_wrong_syntax_error(caplog: LogCaptureFixture):
    tar(["i"], ["path", "path2"])
    assert caplog.records[-1].message == "Неверный синтаксис команды tar"

    tar([], ["path"])
    assert caplog.records[-1].message == "Неверный синтаксис команды tar"


def test_tar_nonexisting_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_dir("existing")

    tar([], ["nonexisting", "new"])
    assert caplog.records[-1].message == "'nonexisting' не существует"


def test_tar_on_correct_cases(caplog: LogCaptureFixture, fs: FakeFilesystem):
    caplog.set_level(logging.DEBUG)

    fs.create_dir("dir")

    tar([], ["dir", "new"])
    assert fs.exists("new.tar.gz")
    assert caplog.records[-1].message == "SUCCESS"

    tar([], ["dir", "dir2.tar.gz"])
    assert fs.exists("dir2.tar.gz")
    assert caplog.records[-1].message == "SUCCESS"


def test_untar_wrong_syntax_error(caplog: LogCaptureFixture):
    untar(["i"], ["path"])
    assert caplog.records[-1].message == "Неверный синтаксис команды untar"

    untar([], ["path", "path2"])
    assert caplog.records[-1].message == "Неверный синтаксис команды untar"


def test_untar_nonexisting_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_file("existing.tar.gz")

    untar([], ["nonexisting.tar.gz"])
    assert caplog.records[-1].message == "'nonexisting.tar.gz' не существует"


def test_untar_wrong_format_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_file("file", contents="test")

    untar([], ["file"])
    assert caplog.records[-1].message == "Неверный формат файла"