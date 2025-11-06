import logging
import shutil

import pytest
from _pytest.logging import LogCaptureFixture
from pyfakefs.fake_filesystem import FakeFilesystem

from colorama import Fore, Style
from src.commands.grep import grep

def test_grep_wrong_syntax_error(caplog: LogCaptureFixture):
    grep(["i", "r", "o"], ["pattern", "path"])
    assert caplog.records[-1].message == "Неверный синтаксис команды grep"

    grep(["i", "r"], ["path"])
    assert caplog.records[-1].message == "Неверный синтаксис команды grep"


def test_grep_wrong_option_error(caplog: LogCaptureFixture):
    grep(["i", "o"], ["pattern", "path"])
    assert caplog.records[-1].message == "Неверная опция 'o'"


def test_grep_nonexisting_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_file("existing")

    grep(["r"], ["pattern", "nonexisting"])
    assert caplog.records[-1].message == "'nonexisting' не существует"


def test_grep_on_dir_no_r_option_error(caplog: LogCaptureFixture, fs: FakeFilesystem):
    fs.create_dir("dir")

    grep([], ["pattern", "dir"])
    assert caplog.records[-1].message == "Не указан ключ -r. Невозможно осуществить поиск"


def test_grep_on_correct_case(capsys: pytest.CaptureFixture, fs: FakeFilesystem):
    fs.create_dir("dir")
    fs.create_file("dir\\file1", contents="4by37h45bu\n7934bf")
    fs.create_file("dir\\file2", contents="dgf9b34g")

    grep(["i", "r"], [r"\db", "dir"])
    assert (capsys.readouterr().out ==
            f"{Fore.LIGHTMAGENTA_EX + "dir\\file1 на строке 1"}{Fore.CYAN + ":" + Style.RESET_ALL}{Fore.RED + "4b" + Style.RESET_ALL}y37h4{Fore.RED + "5b" + Style.RESET_ALL}u\n" +
            f"{Fore.LIGHTMAGENTA_EX + "dir\\file1 на строке 2"}{Fore.CYAN + ":" + Style.RESET_ALL}793{Fore.RED + "4b" + Style.RESET_ALL}f\n" +
            f"{Fore.LIGHTMAGENTA_EX + "dir\\file2 на строке 1"}{Fore.CYAN + ":" + Style.RESET_ALL}dgf{Fore.RED + "9b" + Style.RESET_ALL}34g\n")
