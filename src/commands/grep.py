import os
import re
from logging import Logger

from colorama import Fore


def grep(logger: Logger, ops: list[str], args: list[str]) -> None:
    if len(args) != 2 or len(ops) > 2:
        logger.error(f"Неверный синтаксис команды grep")
        return

    pattern, path = args

    if not os.path.exists(path):
        logger.error(f"'{path}' не существует")
        return
    if any(op not in "ri" for op in ops):
        logger.error(f"Неверная опция '{ops[0]}'")
        return

    if "r" in ops or os.path.isfile(path):

        if os.path.isfile(path):
            find(pattern, path, ops)
        else:
            for root, dirs, files in os.walk(path):
                for file in files:
                    find(pattern, f"{root}{os.sep}{file}", ops)

        logger.debug("SUCCESS")

    else:
        logger.error("Не указан ключ -r. Невозможно осуществить поиск")

    return


def find(pattern: str, f_path: str, ops: list[str]) -> None:
    with open(f_path) as f:
        try:

            for n, line in enumerate(f.read().splitlines()):
                res = list(re.finditer(pattern, line, re.IGNORECASE if "i" in ops else 0))
                if not res:
                    continue

                pos = 0
                print(Fore.LIGHTMAGENTA_EX + f"{f_path} на строке {n + 1}", Fore.CYAN + ":", sep="",
                      end="")
                for m in res:
                    print(line[pos:m.start()], Fore.RED + line[m.start():m.end()], sep="", end="")
                    pos = m.end()
                print(line[pos:])

        except UnicodeDecodeError:
            return
    return