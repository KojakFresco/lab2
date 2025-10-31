import os

from config import LOGGING_CONFIG
from ubuntu import Ubuntu
import logging.config


def main() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    os.chdir("src/home")
    ubuntu = Ubuntu(logger)
    while True:
        cmd = input(f"{os.getcwd()}$ ")
        logger.debug(cmd)
        ubuntu.execute(cmd)


if __name__ == "__main__":
    main()
