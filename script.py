#!/usr/bin/env python3

import os
import subprocess
import sys
from typing import Optional


# Github Action Functions
# https://docs.github.com/en/actions/reference/workflow-commands-for-github-actions

def set_output(name: str, value: str):
    print(f"::set-output name={name}::{value}")


def debug(message: str):
    print(f"::debug::{message}")


def warning(message: str):
    print(f"::warning::{message}")


def error(message: str):
    print(f"::error::{message}")


def begin_group(title: str):
    print(f"::group::{title}")


def end_group():
    print(f"::endgroup::")


# Input

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
            print(f"Input `{name}` is required", file=sys.stderr)
            sys.exit(2)
        return default


def read_bool_input(
        name: str,
        required: bool = False,
        default: Optional[bool] = None
) -> Optional[bool]:
    value = read_str_input(name, required)
    if not value:
        return default
    elif value == "true":
        return True
    elif value == "false":
        return False
    else:
        print(f"Value of input `{name}` is not `true` or `false`",
              file=sys.stderr)
        sys.exit(2)


# Utils

def fix_path(path):
    if path.startswith(os.getcwd()):
        return path.replace(os.getcwd(), "/home/nemo/project")
    else:
        return path


def main():
    arch = read_str_input("arch", default="armv7hl")
    release = read_str_input("release", default="latest")
    check = read_bool_input("check", default=False)
    source_dir = read_str_input("source-dir", default=".")
    image = read_str_input("image", default="r1tschy/sailfishos-platform-sdk")
    enable_debug = read_bool_input("enable-debug", default=False)
    output_dir = read_str_input("output-dir")
    specfile = read_str_input("specfile")
    fix_version = read_bool_input("fix-version")

    print(locals())

    target = f"SailfishOS-{release}-{arch}"

    mb2 = ["mb2"]

    if fix_version is True:
        mb2.append("--fix-version")
    elif fix_version is False:
        mb2.append("--no-fix-version")

    if output_dir:
        os.makedirs(output_dir, mode=0o777, exist_ok=True)
        output_dir = fix_path(output_dir)
        mb2.append("--output-dir")
        mb2.append(output_dir)

    if specfile:
        specfile = fix_path(specfile)
        mb2.append("--specfile")
        mb2.append(specfile)

    mb2.append("build")

    if enable_debug is True:
        mb2.append("--enable-debug")

    if enable_debug is True:
        mb2.append("--enable-debug")

    mb2.append("-j2")  # TODO: check for processor count
    mb2.append(source_dir)

    retcode = subprocess.call([
        "docker", "run", "--rm", "--privileged",
        "--volume", f"{os.getcwd()}:/home/nemo/project",
        "--workdir", "/home/nemo/project",
        f"{image}:{release}"] + mb2)

    if retcode != 0:
        sys.exit(retcode)


if __name__ == "__main__":
    main()
