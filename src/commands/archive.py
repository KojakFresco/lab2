import tarfile
import os
import shutil
import logging


def zip(ops: list[str], args: list[str]) -> None:
    if len(args) != 2 or ops:
        logging.getLogger(__name__).error(f"Неверный синтаксис команды zip")
        return

    file, dest = args
    if not os.path.exists(file):
        logging.getLogger(__name__).error(f"'{file}' не существует")
        return

    try:
        if dest.rfind(".zip") != -1:
            dest = dest[:dest.rfind(".zip")]

        shutil.make_archive(dest, "zip", root_dir=os.getcwd(), base_dir=file)
    except PermissionError:
        logging.getLogger(__name__).error("Отказано в доступе")
        return
    logging.getLogger(__name__).debug("SUCCESS")
    return


def unzip(ops: list[str], args: list[str]) -> None:
    if len(args) != 1 or ops:
        logging.getLogger(__name__).error(f"Неверный синтаксис команды unzip")
        return

    file = args[0]
    if not os.path.exists(file):
        logging.getLogger(__name__).error(f"'{file}' не существует")
        return

    try:
        shutil.unpack_archive(file)
    except shutil.ReadError:
        logging.getLogger(__name__).error("Неверный формат файла")
        return
    except PermissionError:
        logging.getLogger(__name__).error("Отказано в доступе")
        return
    logging.getLogger(__name__).debug("SUCCESS")
    return


def tar(ops: list[str], args: list[str]) -> None:
    if len(args) != 2 or ops:
        logging.getLogger(__name__).error(f"Неверный синтаксис команды tar")
        return

    file, dest = args
    if not os.path.exists(file):
        logging.getLogger(__name__).error(f"'{file}' не существует")
        return

    try:
        if dest.rfind(".tar.gz") != -1:
            dest = dest[:dest.rfind(".tar.gz")] + ".tar.gz"
        else: dest += ".tar.gz"

        with tarfile.open(dest, "w:gz") as t:
            t.add(file, arcname=os.path.basename(file))

    except PermissionError:
        logging.getLogger(__name__).error("Отказано в доступе")
        return

    logging.getLogger(__name__).debug("SUCCESS")
    return


def untar(ops: list[str], args: list[str]) -> None:
    if len(args) != 1 or ops:
        logging.getLogger(__name__).error(f"Неверный синтаксис команды untar")
        return

    file = args[0]
    if not os.path.exists(file):
        logging.getLogger(__name__).error(f"'{file}' не существует")
        return

    try:
        tarfile.open(file, "r:gz").extractall(path=os.getcwd())
        shutil.unpack_archive(file)
    except tarfile.ReadError:
        logging.getLogger(__name__).error("Неверный формат файла")
        return
    except PermissionError:
        logging.getLogger(__name__).error("Отказано в доступе")
        return

    logging.getLogger(__name__).debug("SUCCESS")
    return