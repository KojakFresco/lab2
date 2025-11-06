import logging
from _pytest.logging import LogCaptureFixture
from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.cd import cd

def test_cd_wrong_syntax_error(caplog: LogCaptureFixture):
    cd(["i"], ["path"])
    assert caplog.records[-1].message == "Неверный синтаксис команды cd"

    cd([], [])
    assert caplog.records[-1].message == "Неверный синтаксис команды cd"


def test_cd_on_file(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_file("new_file")

    cd([], ["new_file"])
    assert caplog.records[-1].message == "'new_file' не директория"


def test_cd_on_nonexisting_dir(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_dir("existing_dir")

    cd([], ["nonexisting_dir"])
    assert caplog.records[-1].message == "Не удается найти указанную директорию: 'nonexisting_dir'"


def test_cd_on_existing_dir(caplog: LogCaptureFixture, fs: FakeFilesystem):
    caplog.set_level(logging.DEBUG)
    fs.create_dir("existing_dir")

    cd([], ["existing_dir"])
    assert caplog.records[-1].message == "SUCCESS"