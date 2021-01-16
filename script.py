#!/usr/bin/env python3
import argparse
import os
import sys
from typing import Optional


# Github Action Functions

def set_output(id_: str, value: str):
    print("::set-output name={}::{}".format(id_, value))


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





if __name__ == "__main__":
    main()
