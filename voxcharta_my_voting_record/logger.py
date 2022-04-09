import logging
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler

sh = RichHandler(
    level=logging.INFO, markup=True, log_time_format="[%X]", show_path=False
)


class LogClass:
    """
    Purpose:
      Main class to log information to stdout and ASCII logfile

    Note [1]: This code is identical to the one used in:
      https://github.com/ualibraries/LD_Cool_P

    Note [2]: Logging level is set for DEBUG for file and INFO for stdout

    To use:
    log = LogClass(logfile).get_logger()

    Parameters:
      logfile: Filename for exported log file
    """

    def __init__(self, logfile: Path):
        self.LOG_FILENAME = logfile

    def get_logger(self):
        log = logging.getLogger("main_logger")
        log.setLevel(logging.DEBUG)
        if not log.handlers:
            log.addHandler(sh)

            console = get_console(self.LOG_FILENAME)

            fh = RichHandler(
                console=console,
                level=logging.DEBUG,
                log_time_format="[%X]",
                markup=True,
            )
            log.addHandler(fh)
        return log


def get_console(filename: Path) -> Console:
    return Console(
        force_terminal=False, file=open(filename, "w"), log_time=True
    )


def log_stdout():
    log = logging.getLogger("stdout_logger")
    log.setLevel(logging.DEBUG)
    if not log.handlers:
        log.addHandler(sh)
        log.handler_set = True
        log.propagate = False
    return log
