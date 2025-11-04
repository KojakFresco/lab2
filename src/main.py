import os

from config import LOGGING_CONFIG
import logging.config

from parser import parse
import commands.create
import commands.move
import commands.ls
import commands.cd
import commands.cat
import commands.archive
import commands.grep

import colorama
colorama.init(autoreset=True)


def main() -> None:

    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)

    if not os.path.exists("home"):
        os.mkdir("home")
        os.chmod("home", 0o555)
    os.chdir("home")
    root = os.getcwd()

    functions = {
        "ls": commands.ls.ls,
        "touch": commands.create.touch,
        "mkdir": commands.create.mkdir,
        "cd": commands.cd.cd,
        "cat": commands.cat.cat,
        "cp": commands.move.cp,
        "mv": commands.move.mv,
        "rm": commands.move.rm,
        "zip": commands.archive.zip,
        "unzip": commands.archive.unzip,
        "tar": commands.archive.tar,
        "untar": commands.archive.untar,
        "grep": commands.grep.grep,
    }

    while True:
        print(colorama.Fore.BLUE + f"{os.getcwd().replace(root, "~")}", end="")
        try:
            cmd = input("$ ")
        except KeyboardInterrupt:
            print()
            continue
        if cmd: logger.debug(cmd)

        tokens = parse(cmd, root)

        if tokens["fun"] in ["exit", "quit"]:
            break

        if tokens:
            try:
                functions[tokens["fun"]](logger, tokens["options"], tokens["args"])
            except KeyError:
                logger.error(f"Команда '{tokens["fun"]}' не найдена")


if __name__ == "__main__":
    main()
