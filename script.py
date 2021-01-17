#!/usr/bin/env python3
import contextlib
import os
import shlex
import subprocess
import sys
import textwrap
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


@contextlib.contextmanager
def group(title: str):
    print(f"::group::{title}", flush=True)
    yield
    print(f"::endgroup::", flush=True)


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

def call(args, stdin: Optional[bytes] = None):
    proc = subprocess.run(args, input=stdin)
    if proc.returncode != 0:
        cmd = ' '.join(shlex.quote(arg) for arg in args)
        print(f"command failed with {proc.returncode}: {cmd}",
              file=sys.stderr)
        sys.exit(proc.returncode)


def main():
    arch = read_str_input("arch", required=True)
    release = read_str_input("release", required=True)
    check = read_bool_input("check", default=False)
    source_dir = read_str_input("source-dir")
    image = read_str_input("image", default="r1tschy/sailfishos-platform-sdk")
    enable_debug = read_bool_input("enable-debug", default=False)
    output_dir = read_str_input("output-dir")
    specfile = read_str_input("specfile")
    fix_version = read_bool_input("fix-version")

    uid = os.getuid()
    cwd = os.getcwd()
    cusername = "mersdk"  # TODO: use nemo in coderus images

    # TODO: do only once when already modified
    # with group("Preparation"):
    #     call(["docker", "build", "-t", f"{image}:{release}", "-"],
    #          stdin=textwrap.dedent(f"""
    #             FROM {image}:{release}
    #             RUN sudo usermod -u {uid} {cusername}""").encode("utf-8"))

    mb2_base = ["mb2"]
    if fix_version is True:
        mb2_base.append("--fix-version")
    elif fix_version is False:
        mb2_base.append("--no-fix-version")

    if output_dir:
        os.makedirs(output_dir, mode=0o777, exist_ok=True)
        if output_dir.startswith(cwd):
            output_dir = output_dir.replace(cwd, f"/home/{cusername}/project")

        mb2_base.append("--output-dir")
        mb2_base.append(output_dir)

    if specfile:
        if specfile.startswith(cwd):
            specfile = specfile.replace(cwd, f"/home/{cusername}/project")
        mb2_base.append("--specfile")
        mb2_base.append(specfile)

    mb2_base.append("-t")
    mb2_base.append(f"SailfishOS-{release}-{arch}")

    mb2_build = mb2_base.copy()
    mb2_build.append("build")

    if enable_debug is True:
        mb2_build.append("--enable-debug")

    mb2_build.append("-j2")  # TODO: check for processor count
    if source_dir:
        mb2_build.append(source_dir)

    call(["docker", "run", "--rm", "--privileged",
            "--volume", f"{cwd}:/home/{cusername}/project",
            "--workdir", f"/home/{cusername}/project",
            f"{image}:{release}"] + mb2_build)

    if check:
        mb2_check = mb2_base.copy()
        mb2_check.append("check")

        call(["docker", "run", "--rm", "--privileged",
                "--volume", f"{cwd}:/home/{cusername}/project",
                "--workdir", f"/home/{cusername}/project",
                f"{image}:{release}"] + mb2_check)


if __name__ == "__main__":
    main()
