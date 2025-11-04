import os
from logging import Logger


def cd(logger: Logger, ops: list[str], args: list[str]) -> None:
    if ops or len(args) != 1:
        logger.error("Неверный синтаксис команды cd")
        return

    path = args[0]
    if os.path.isfile(path):
        logger.error(f"'{path}' не директория")
        return

    try:
        os.chdir(path)
        logger.debug("SUCCESS")
    except FileNotFoundError:
        logger.error(f"Не удается найти указанную директорию: '{path}'")

    return