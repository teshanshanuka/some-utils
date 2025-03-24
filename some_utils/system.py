import subprocess
import sys
from typing import Callable, List, NoReturn

from .text import TermColors


def err_exit(msg="", code=1) -> NoReturn:
    if msg:
        print(TermColors.red(msg))
    sys.exit(code)


def _raise_runtime(s: str):
    raise RuntimeError(s)


def run_cmd(cmd: List[str], on_err: Callable[[str], None] = _raise_runtime, echo=False):
    if echo:
        print(TermColors.okgreen(f"+ Running: {' '.join(cmd)}"))
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            if stderr := res.stderr.decode():
                on_err(f"Process returned with error code {res.returncode}. Err: {stderr}")
                return
            else:
                on_err(f"Process returned with error code {res.returncode}")
                return

        return res.stdout.decode()
    except FileNotFoundError as err:
        on_err(f"Command not supported\nErr: {err}")
        return
    except Exception as err:
        on_err(f"Err: {err}")
