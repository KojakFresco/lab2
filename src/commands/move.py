import os
import shutil
import pathlib
from logging import Logger


def cp(logger: Logger, ops: list[str], args: list[str]) -> None:
    if len(args) != 2 or len(ops) > 1:
        logger.error(f"Неверный синтаксис команды cp")
        return
    if os.path.abspath(args[0]) == os.path.abspath(args[1]):
        logger.error(f"'{args[0]}' и '{args[1]}' - это один и тот же файл")
        return
    if len(ops) == 1 and ops[0] != "r":
        logger.error(f"Неверная опция '{ops[0]}'")
        return
    if not os.path.exists(args[0]):
        logger.error(f"'{args[0]}' не существует")
        return

    if len(ops) == 1 or os.path.isfile(args[0]):
        recursive_copy(logger, args[0], args[1])
    else:
        logger.error("Не указан ключ -r. Невозможно скопировать")

    return


def recursive_copy(logger: Logger, path: str, dest: str) -> int:
    # logger.debug(f"path: {os.path.abspath(path)}, dest: {os.path.abspath(dest)}")
    if os.path.isdir(path):
        if not pathlib.Path(dest).exists(): pathlib.Path(dest).mkdir()
        for el in os.listdir(path):
            if recursive_copy(logger, f"{path}/{el}", f"{dest}/{el}") == -1:
                return -1
    else:
        try:
            shutil.copy(path, dest)
        except PermissionError:
            logger.error("Отказано в доступе")
            return -1
    logger.debug("SUCCESS")
    return 0


def mv(logger: Logger, ops: list[str], args: list[str]) -> None:
    if len(args) != 2 or ops:
        logger.error(f"Неверный синтаксис команды mv")
        return

    file, dest = args
    if not os.path.exists(file):
        logger.error(f"'{file}' не существует")
        return

    try:
        shutil.move(file, dest)
    except shutil.Error:
        logger.error(f"Нельзя переместить директорию '{file}' в свою поддиректорию '{dest}'")
    except PermissionError:
        logger.error("Отказано в доступе")
        return
    logger.debug("SUCCESS")
    return


def rm(logger: Logger, ops: list[str], args: list[str]) -> None:
    if len(ops) > 1 or len(args) != 1:
        logger.error("Неверный синтаксис команды rm")
        return

    path = args[0]
    try:
        if len(ops) == 1:
            if ops[0] == "r":
                while True:
                    ans = input(f"Удалить директорию '{path}'? [y/n] ")
                    if ans == "y":
                        shutil.rmtree(path)
                        break
                    elif ans == "n":
                        break
                logger.debug("SUCCESS")
            else:
                logger.error(f"Неверная опция '{ops[0]}'")
        else:
            if os.path.isfile(path):
                os.remove(path)
                logger.debug("SUCCESS")
            else:
                logger.error(f"Невозможно удалить '{path}': это директория")
    except PermissionError:
        logger.error("Отказано в доступе")
    return