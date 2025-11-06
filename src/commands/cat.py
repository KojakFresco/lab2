import os
import logging


def cat(ops: list[str], args: list[str]) -> None:
    if ops or len(args) != 1:
        logging.getLogger(__name__).error("Неверный синтаксис команды cat")
        return

    path = args[0]
    if not os.path.exists(path):
        logging.getLogger(__name__).error(f"'{path}' не существует")
        return
    if os.path.isdir(path):
        logging.getLogger(__name__).error(f"'{path}' это директория")
        return

    try:
        print(open(path, encoding="utf-8").read())
        logging.getLogger(__name__).debug("SUCCESS")
    except UnicodeDecodeError:
        logging.getLogger(__name__).error("Не получилось расшифровать файл в кодировке utf-8")

    return