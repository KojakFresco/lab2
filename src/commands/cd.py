import os
import logging


def cd(ops: list[str], args: list[str]) -> None:
    if ops or len(args) != 1:
        logging.getLogger(__name__).error("Неверный синтаксис команды cd")
        return

    path = args[0]
    if os.path.isfile(path):
        logging.getLogger(__name__).error(f"'{path}' не директория")
        return

    try:
        os.chdir(path)
        logging.getLogger(__name__).debug("SUCCESS")
    except FileNotFoundError:
        logging.getLogger(__name__).error(f"Не удается найти указанную директорию: '{path}'")

    return