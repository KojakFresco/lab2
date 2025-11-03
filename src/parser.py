import logging
import re
import shlex


def parse(src: str, root: str) -> dict | int:
    """ Разбить строку на токены: функции, опции, аргументы"""
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

    # TODO: check quotation marks and empty entry
    # while pos < len(src):
    #     m = Token.match(src, pos)
    #     if not m:
    #         logging.getLogger(__name__).error(f"Некорректный ввод около: '{src[pos:]}'")
    #         return 0
    #
    #     t = m.group(1)
    #
    #     if not t:
    #         logging.getLogger(__name__).error(f"Некорректный ввод около: '{src[pos:]}'")
    #         return 0
    #     pos = m.end()
    #
    #     if t[0] == "-":
    #         for a in t[1:]:
    #             out["options"].append(a)
    #     else:
    #         if "~" in t:
    #             out["args"].append(t.replace("~", root))
    #         else:
    #             out["args"].append(t)
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