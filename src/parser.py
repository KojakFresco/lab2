import logging
import re
import shlex


def parse(src: str, root: str) -> dict | int:
    """ Разбить строку на: функции, опции, аргументы"""
    out: dict = {"fun": "", "options": [], "args": []}

    if not src:
        return 0
    try:
        args = shlex.split(src)
    except ValueError:
        logging.getLogger(__name__).error(f"Некорректный ввод")
        return 0
    out["fun"] = args[0]
    del args[0]

    for arg in args:
        if arg[0] == "-":
            for a in arg[1:]:
                out["options"].append(a)
        else:
            if arg == "~":
                out["args"].append(root)
            else:
                out["args"].append(arg)
    return out