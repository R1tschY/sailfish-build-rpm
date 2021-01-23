import contextlib
import os
import sys
import uuid
from typing import Optional

# Github Action Functions
# https://docs.github.com/en/actions/reference/workflow-commands-for-github-actions


def set_output(name: str, value: str):
    print(f"::set-output name={name}::{value}")


def debug(message: str):
    print(f"::debug::{message}", flush=True)


def info(message: str):
    print(message, flush=True)


def warning(message: str):
    print(f"::warning::{message}", flush=True)


def error(message: str):
    print(f"::error::{message}", flush=True)


def set_failed(message: str):
    error(message)
    sys.exit(1)


@contextlib.contextmanager
def group(title: str):
    print(f"::group::{title}", flush=True)
    yield
    print(f"::endgroup::", flush=True)


@contextlib.contextmanager
def stop_commands():
    endtoken = uuid.uuid4().hex
    print(f"::stop-commands::{endtoken}", flush=True)
    yield
    print(f"::{endtoken}::", flush=True)


def read_str_input(
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
        return value
    else:
        if required:
            set_failed(f"Input `{name}` is required")
        return default
