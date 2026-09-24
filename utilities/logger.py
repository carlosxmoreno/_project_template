"""
{{PROJECT_NAME}} - Logger with timestamps, levels and caller name.
Version: 1.0.0
Component: utilities

Exposes:
    Level       -- enum with available log levels (INFO, ERROR, DEBUG)
    log()       -- single logging function; writes to stdout/stderr and to file
    configure() -- sets project_name and log_dir (call at project startup)

External dependencies: none
"""

import datetime
import inspect
import os
import sys
from enum import Enum
from pathlib import Path


class Level(Enum):
    INFO = "INFO"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


_config = {
    "project_name": "project",
    "log_dir": Path.cwd() / "logs",
    "stream": sys.stdout,
}

_LEVEL_ENABLED = {
    Level.INFO: True,
    Level.ERROR: True,
    Level.DEBUG: True,
}


def configure(project_name: str, log_dir: str = None, stream=None):
    """Configure project name, log directory and output stream.

    Args:
        project_name: Name used for the log file (project_name.log).
        log_dir: Directory where log files are written. Defaults to ./logs.
        stream: Output stream for non-error messages. Defaults to stdout.
    """
    _config["project_name"] = project_name
    _config["log_dir"] = Path(log_dir) if log_dir else Path.cwd() / "logs"
    if stream is not None:
        _config["stream"] = stream


def _get_caller_name() -> str:
    """Return the module and function name of the caller."""
    stack = inspect.stack()
    if len(stack) > 2:
        module = os.path.basename(stack[2].filename).replace(".py", "")
        return f"{module}.{stack[2].function}"
    return "unknown"


def _write_to_file(message: str):
    """Write message to the log file."""
    try:
        log_dir = _config["log_dir"]
        os.makedirs(log_dir, exist_ok=True)
        log_file = Path(log_dir) / f"{_config['project_name']}.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}", file=sys.stderr)


def log(level: Level, message: str):
    """Log a message with the given level, timestamp and caller.

    Args:
        level: Log level (INFO, ERROR, DEBUG).
        message: Message to log.
    """
    if not _LEVEL_ENABLED.get(level, True):
        return
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    caller = _get_caller_name()
    log_message = f"[{level.value:<5}] {now} - {caller} - {message}"
    if level == Level.ERROR:
        print(log_message, file=sys.stderr)
    else:
        print(log_message, file=_config["stream"])
    _write_to_file(log_message)
