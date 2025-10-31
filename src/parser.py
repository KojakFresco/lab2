class Parser:
    def parse(self, src: str) -> dict:
        """ Разбить строку на токены: функции, опции, аргументы"""
        out: dict = {"fun": "", "options": [], "args": []}

        args = src.split()
        out["fun"] = args[0]
        del args[0]
        # TODO: check quotation marks
        for arg in args:
            if arg[0] == "-":
                for a in arg[1:]:
                    out["options"].append(a)
            else:
                out["args"].append(arg)
        return out
