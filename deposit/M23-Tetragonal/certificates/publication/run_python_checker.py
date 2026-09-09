#!/usr/bin/env python3
"""Run one certificate script and force clean interpreter termination.

Some heavy symbolic checkers leave third-party cleanup state that can delay
interpreter shutdown when many checkers are chained by a shell wrapper.  This
helper executes the target as ``__main__``, preserves its arguments and exit
status, flushes both output streams, and calls ``os._exit`` only after the
checker has returned normally (or raised ``SystemExit``).  Unhandled
exceptions retain a nonzero exit status and traceback.
"""

from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: run_python_checker.py SCRIPT [ARG ...]", file=sys.stderr)
        return 2

    script = Path(sys.argv[1]).resolve()
    if not script.is_file():
        print(f"certificate script not found: {script}", file=sys.stderr)
        return 2

    script_args = sys.argv[2:]
    sys.argv = [str(script), *script_args]
    sys.path.insert(0, str(script.parent))

    try:
        runpy.run_path(str(script), run_name="__main__")
    except SystemExit as exc:
        code = exc.code
        if code is None:
            return 0
        if isinstance(code, int):
            return code
        print(code, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    exit_code = 1
    try:
        exit_code = main()
    finally:
        try:
            sys.stdout.flush()
        finally:
            sys.stderr.flush()
    os._exit(exit_code)
