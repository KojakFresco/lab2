import os
import re
import logging

from colorama import Fore, Style


def grep(ops: list[str], args: list[str]) -> None:
    if len(args) != 2 or len(ops) > 2:
        logging.getLogger(__name__).error(f"Неверный синтаксис команды grep")
        return

    if any(op not in "ri" for op in ops):
        logging.getLogger(__name__).error(f"Неверная опция '{ops[0] if ops[0] not in "ri" else ops[1]}'")
        return

    pattern, path = args
    if not os.path.exists(path):
        logging.getLogger(__name__).error(f"'{path}' не существует")
        return

    if "r" in ops or os.path.isfile(path):

        if os.path.isfile(path):
            find(pattern, path, ops)
        else:
            for root, dirs, files in os.walk(path):
                for file in files:
                    find(pattern, f"{root}{os.sep}{file}", ops)

        logging.getLogger(__name__).debug("SUCCESS")

    else:
        logging.getLogger(__name__).error("Не указан ключ -r. Невозможно осуществить поиск")

    return


def find(pattern: str, f_path: str, ops: list[str]) -> None:
    with open(f_path) as f:
        try:

            for n, line in enumerate(f.read().splitlines()):
                res = list(re.finditer(pattern, line, re.IGNORECASE if "i" in ops else 0))
                if not res:
                    continue

                pos = 0
                print(Fore.LIGHTMAGENTA_EX + f"{f_path} на строке {n + 1}", Fore.CYAN + ":", Style.RESET_ALL, sep="",
                      end="")
                for m in res:
                    print(line[pos:m.start()], Fore.RED + line[m.start():m.end()], Style.RESET_ALL, sep="", end="")
                    pos = m.end()
                print(line[pos:])

        except UnicodeDecodeError:
            return
    return