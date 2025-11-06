import pathlib
import os
import logging


def touch(ops: list[str], args: list[str]) -> None:
    if ops or len(args) != 1:
        logging.getLogger(__name__).error("Неверный синтаксис команды touch")
        return
    try:
        pathlib.Path(args[0]).touch()
        logging.getLogger(__name__).debug("SUCCESS")
    except FileExistsError:
        logging.getLogger(__name__).debug("SUCCESS")
    except OSError:
        logging.getLogger(__name__).error(f"Невозможно создать файл с названием '{args[0]}'")

    return


def mkdir(ops: list[str], args: list[str]) -> None:
    if ops or len(args) != 1:
        logging.getLogger(__name__).error("Неверный синтаксис команды mkdir")
        return

    try:
        pathlib.Path(args[0]).mkdir()
        logging.getLogger(__name__).debug("SUCCESS")
    except FileExistsError:
        if os.path.isdir(args[0]):
            logging.getLogger(__name__).error(f"Директория '{args[0]}' уже существует")
        else:
            logging.getLogger(__name__).error(f"Не удалось создать директорию: Существует файл с названием '{args[0]}'")
    except OSError:
        logging.getLogger(__name__).error(f"Невозможно создать директорию с названием '{args[0]}'")

    return