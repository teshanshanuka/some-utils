import sys
import subprocess
from typing import Callable, TypeVar, Optional

from .text import TermColors


def err_exit(msg="", code=1):
    if msg:
        print(TermColors.red(msg))
    sys.exit(code)


def run_cmd(cmd: list[str], on_err: Callable[[str], None] = RuntimeError, echo=False):
    if echo:
        print(TermColors.okgreen(f"+ Running: {' '.join(cmd)}"))
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.stdout.decode()
    except FileNotFoundError as err:
        on_err(f"Command not supported\nErr: {err}")
    if stderr := res.stderr.decode():
        on_err(f"Err: {stderr}")
