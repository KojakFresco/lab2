import os
from logging import Logger


def cd(logger: Logger, ops: list[str], args: list[str]) -> None:
    if not ops and len(args) == 1:
        path = args[0]
        try:
            os.chdir(path)
            logger.debug("SUCCESS")
        except FileNotFoundError:
            logger.error(f"Не удается найти указанный файл: '{path}'")
    else:
        logger.error("Неверный синтаксис команды cd")
    return