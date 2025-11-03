import os
from logging import Logger


def cat(logger: Logger, ops: list[str], args: list[str]) -> None:
    if not ops and len(args) == 1:
        path = args[0]
        if not os.path.exists(path):
            logger.error(f"{path} не существует")
            return
        if os.path.isdir(path):
            logger.error(f"{path} это директория")
            return
        print(open(path, encoding="utf-8").read())
        logger.debug("SUCCESS")
    else:
        logger.error("Неверный синтаксис команды cat")
    return