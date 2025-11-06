import os
import shutil
import pathlib
import logging


def cp(ops: list[str], args: list[str]) -> None:
    if len(args) != 2 or len(ops) > 1:
        logging.getLogger(__name__).error(f"Неверный синтаксис команды cp")
        return
    if os.path.abspath(args[0]) == os.path.abspath(args[1]):
        logging.getLogger(__name__).error(f"'{args[0]}' и '{args[1]}' - это один и тот же путь")
        return
    if len(ops) == 1 and ops[0] != "r":
        logging.getLogger(__name__).error(f"Неверная опция '{ops[0]}'")
        return
    if not os.path.exists(args[0]):
        logging.getLogger(__name__).error(f"'{args[0]}' не существует")
        return

    if len(ops) == 1 or os.path.isfile(args[0]):
        if recursive_copy(args[0], args[1]):
            logging.getLogger(__name__).debug("SUCCESS")
    else:
        logging.getLogger(__name__).error("Не указан ключ -r. Невозможно скопировать")

    return


def recursive_copy(path: str, dest: str) -> int:
    # logging.getLogger(__name__).debug(f"path: {os.path.abspath(path)}, dest: {os.path.abspath(dest)}")
    if os.path.isdir(path):
        if not pathlib.Path(dest).exists(): pathlib.Path(dest).mkdir()
        for el in os.listdir(path):
            if not recursive_copy(f"{path}/{el}", f"{dest}/{el}"):
                return 0
    else:
        try:
            shutil.copy(path, dest)
        except PermissionError:
            logging.getLogger(__name__).error("Отказано в доступе")
            return 0
    return 1


def mv(ops: list[str], args: list[str]) -> None:
    if len(args) != 2 or ops:
        logging.getLogger(__name__).error(f"Неверный синтаксис команды mv")
        return

    file, dest = args
    if not os.path.exists(file):
        logging.getLogger(__name__).error(f"'{file}' не существует")
        return

    try:
        shutil.move(file, dest)
    except shutil.Error:
        logging.getLogger(__name__).error(f"Нельзя переместить директорию '{file}' в свою поддиректорию '{dest}'")
    except PermissionError:
        logging.getLogger(__name__).error("Отказано в доступе")
        return
    logging.getLogger(__name__).debug("SUCCESS")
    return


def rm(ops: list[str], args: list[str]) -> None:
    if len(ops) > 1 or len(args) != 1:
        logging.getLogger(__name__).error("Неверный синтаксис команды rm")
        return

    path = args[0]
    if not os.path.exists(path):
        logging.getLogger(__name__).error(f"'{path}' не существует")
        return

    try:

        if len(ops) == 1 and os.path.isdir(path):
            if ops[0] == "r":

                while True:
                    ans = input(f"Удалить директорию '{path}'? [y/n] ")
                    if ans == "y":
                        shutil.rmtree(path)
                        break
                    elif ans == "n":
                        break
                logging.getLogger(__name__).debug("SUCCESS")

            else:
                logging.getLogger(__name__).error(f"Неверная опция '{ops[0]}'")
        else:
            if os.path.isfile(path):
                os.remove(path)
                logging.getLogger(__name__).debug("SUCCESS")
            else:
                logging.getLogger(__name__).error(f"Невозможно удалить '{path}': это директория")

    except PermissionError:
        logging.getLogger(__name__).error("Отказано в доступе")
    return