import contextlib
import json
import os
import re
import sys
from typing import Any, Dict, Optional

# Github Action Functions
# https://docs.github.com/en/actions/reference/workflow-commands-for-github-actions


def command(cmd: str, params: Optional[Dict[str, str]], value: Any) -> None:
    if not cmd:
        cmd = "missing.command"

    if params:
        cmd_params = ",".join([
            f"{key}={_escape_property(value)}" for key, value in params.items()
        ])
        cmd_str = f"::{cmd} {cmd_params}::{_escape_data(value)}"
    else:
        cmd_str = f"::{cmd}::{_escape_data(value)}"

    print(cmd_str, flush=True)


def _to_command_value(input: Any) -> str:
    if input is None:
        return ""
    elif isinstance(input, str):
        return input
    else:
        return json.dumps(input, separators=(',', ':'))


def _escape_data(s: Any) -> str:
    return re.sub(
        r"[%\r\n]", lambda x: f"%{ord(x.group()):02X}", _to_command_value(s))


def _escape_property(s: Any) -> str:
    return re.sub(
        r"[%\r\n:,]", lambda x: f"%{ord(x.group()):02X}", _to_command_value(s))


def set_output(name: str, value: Any) -> None:
    command("set-output", {"name": name}, value)


def set_command_echo(enabled: bool) -> None:
    command("echo", None, "on" if enabled else "off")


def is_debug() -> bool:
    return os.environ.get("RUNNER_DEBUG") == "1"


def save_state(name: str, value: Any):
    command("save-state", {"name": name}, value)


def get_state(name: str) -> str:
    return os.environ.get(f"STATE_{name}", "")


def debug(message: str) -> None:
    print(f"::debug::{message}", flush=True)


def info(message: str) -> None:
    print(message, flush=True)


def warning(message: str) -> None:
    print(f"::warning::{message}", flush=True)


def error(message: str) -> None:
    print(f"::error::{message}", flush=True)


def set_failed(message: str) -> None:
    error(message)
    sys.exit(1)


@contextlib.contextmanager
def group(title: str):
    command("group", None, title)
    yield
    command("endgroup", None, None)


def get_input(
        name: str,
        required: bool = False,
        default: Optional[str] = None
) -> Optional[str]:
    env_var = f"INPUT_{name.upper().replace('-', '_')}"
    if env_var in os.environ:
        value = os.environ[env_var]
    else:
        value = None

    if value:
        return value.strip()
    else:
        if required:
            set_failed(f"Input required and not supplied: {name}")
        return default
