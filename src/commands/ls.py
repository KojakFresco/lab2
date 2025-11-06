import os
import colorama
import time
import logging

def ls(ops: list[str], args: list[str]) -> None:
    if len(args) > 1 or len(ops) > 1:
        logging.getLogger(__name__).error(f"Неверный синтаксис команды ls")
        return

    l = False
    if len(ops) == 1:
        if ops[0] == "l":
            l = True
        else:
            logging.getLogger(__name__).error(f"Неверная опция '{ops[0]}'")
            return

    path = args[0] if len(args) > 0 else os.getcwd()
    if not os.path.exists(path) or os.path.isfile(path):
        logging.getLogger(__name__).error(f"Директории '{path}' не существует")
        return

    for f in os.listdir(path):
        f_path = path + "/" + f
        if " " in f:
            f = f"\'{f}\'"
        name = colorama.Fore.BLUE + f if os.path.isdir(f_path) else \
            colorama.Fore.RED + f if f.endswith(".zip") or f.endswith(".tar.gz") else f
        if l:
            print(check_access(f_path), os.path.getsize(f_path),
                  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(f_path))), name)
        else:
            print(name, end="  ")
    if not l and len(os.listdir(path)) > 0: print()
    logging.getLogger(__name__).debug("SUCCESS")

    return


def check_access(path: str) -> str:
    st = bin(os.stat(path).st_mode)
    res = ("r" if int(st[-9]) else "-") + \
          ("w" if int(st[-8]) else "-") + \
          ("x" if int(st[-7]) else "-") + \
          ("r" if int(st[-6]) else "-") + \
          ("w" if int(st[-5]) else "-") + \
          ("x" if int(st[-4]) else "-") + \
          ("r" if int(st[-3]) else "-") + \
          ("w" if int(st[-2]) else "-") + \
          ("x" if int(st[-1]) else "-")
    return res