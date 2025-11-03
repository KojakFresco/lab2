import os
import colorama
import time

def ls(logger, ops: list[str], args: list[str]) -> None:
    if len(args) > 1 or len(ops) > 1:
        logger.error(f"Неверный синтаксис команды ls")
        return

    path = args[0] if len(args) > 0 else os.getcwd()

    if not os.path.exists(path) or os.path.isfile(path):
        logger.error(f"Директории '{path}' не существует")
        return

    l = False
    if len(ops) == 1:
        if ops[0] == "l":
            l = True
        else:
            logger.error(f"Неверная опция '{ops[0]}'")

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
    logger.debug("SUCCESS")

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