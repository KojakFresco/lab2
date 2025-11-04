import pathlib
import os
from logging import Logger


def touch(logger: Logger, ops: list[str], args: list[str]) -> None:
    if ops or len(args) != 1:
        logger.error("Неверный синтаксис команды touch")
        return
    try:
        pathlib.Path(args[0]).touch()
        logger.debug("SUCCESS")
    except FileExistsError:
        logger.debug("SUCCESS")
    except OSError:
        logger.error(f"Невозможно создать файл с названием '{args[0]}'")

    return


def mkdir(logger: Logger, ops: list[str], args: list[str]) -> None:
    if ops and len(args) != 1:
        logger.error("Неверный синтаксис команды mkdir")
        return

    try:
        pathlib.Path(args[0]).mkdir()
        logger.debug("SUCCESS")
    except FileExistsError:
        if os.path.isdir(args[0]):
            logger.error(f"Директория '{args[0]}' уже существует")
        else:
            logger.error(f"Не удалось создать директорию: Существует файл с названием '{args[0]}'")
    except OSError:
        logger.error(f"Невозможно создать директорию с названием '{args[0]}'")

    return