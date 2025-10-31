import os
import pathlib
import time
from logging import Logger
from parser import Parser


class Ubuntu:
    def __init__(self, logger: Logger):
        self.root = os.getcwd()
        self.logger = logger
        self.parser = Parser()
        self.functions = {
            "ls": self.ls,
            "touch": self.touch,
            "mkdir": self.mkdir,
            "cd": self.cd
        }

    def execute(self, cmd: str):
        tokens = self.parser.parse(cmd)
        try:
            self.functions[tokens["fun"]](tokens["options"], tokens["args"])
        except KeyError:
            self.logger.error(f"ERROR: Command '{cmd}' not found")

    def check_access(self, path) -> str:
        res = ("r" if os.access(path, os.R_OK) else "-") + \
              ("w" if os.access(path, os.W_OK) else "-") + \
              ("x" if os.access(path, os.X_OK) else "-")
        return res

    def ls(self, ops, args) -> None:
        if len(args) > 1 or len(ops) > 1:
            self.logger.error(f"Неверный синтаксис команды ls")
            return

        path = args[0] if len(args) > 0 else os.getcwd()

        try:
            assert os.listdir(path)
        except FileNotFoundError:
            self.logger.error(f"Директории '{path}' не существует")
            return

        if len(ops) == 1:
            if ops[0] == "l":
                for f in os.listdir(path):
                    f_path = path + "/" + f
                    print(self.check_access(f_path), os.path.getsize(f_path),
                          time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(f_path))), f)
                    self.logger.debug("SUCCESS")
            else:
                self.logger.error(f"Неверная опция '{ops[0]}'")
        else:
            self.logger.info("  ".join(os.listdir(path)))
        return

    def touch(self, ops, args) -> None:
        if not ops and len(args) == 1:
            pathlib.Path(os.getcwd() + "/" + args[0]).touch()
            self.logger.debug("SUCCESS")
        else:
            self.logger.error(f"Неверный синтаксис команды touch")
        return

    def mkdir(self, ops, args) -> None:
        if not ops and len(args) == 1:
            pathlib.Path(os.getcwd() + "/" + args[0]).mkdir()
            self.logger.debug("SUCCESS")
        else:
            self.logger.error("Неверный синтаксис команды mkdir")
        return

    def cd(self, ops, args) -> None:
        if not ops and len(args) == 1:
            path = args[0]
            try:
                match path:
                    case "~":
                        os.chdir(self.root)
                    case _:
                        os.chdir(path)
                self.logger.debug("SUCCESS")
            except FileNotFoundError:
                self.logger.error(f"Не удается найти указанный файл: '{path}'")
        else:
            self.logger.error("Неверный синтаксис команды cd")
        return

    def cat(self, ops, args) -> None:
        return

    def cp(self, ops, args) -> None:
        return

    def mv(self, ops, args) -> None:
        return

    def rm(self, ops, args) -> None:
        return
