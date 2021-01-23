#!/usr/bin/env python3
import os
import shlex
import subprocess
from typing import Optional

from action import group, read_str_input, set_failed


# Input


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
        set_failed(f"Value of input `{name}` is not `true` or `false`")


# Utils

def call(args, stdin: Optional[bytes] = None):
    cmd = ' '.join(shlex.quote(arg) for arg in args)
    print(f"[command]{cmd}", flush=True)
    proc = subprocess.run(args, input=stdin)
    if proc.returncode != 0:
        set_failed(f"command failed with {proc.returncode}: {cmd}")


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
    tagged_image = f"{image}:{release}-{arch}"
    docker_args = [
        "docker", "run", "--rm", "--privileged",
        "--volume", f"{cwd}:/home/{cusername}/project",
        "--workdir", f"/home/{cusername}/project",
        tagged_image]

    with group(f"Pull image {tagged_image}"):
        call(["docker", "image", "pull", tagged_image])

    # TODO: do only once when already modified
    # with group("Preparation"):
    #     call(["docker", "build", "-t", f"{image}:{release}", "-"],
    #          stdin=textwrap.dedent(f"""
    #             FROM {image}:{release}
    #             RUN sudo usermod -u {uid} {cusername}""").encode("utf-8"))

    mb2_args = ["mb2"]
    if fix_version is True:
        mb2_args.append("--fix-version")
    elif fix_version is False:
        mb2_args.append("--no-fix-version")

    if output_dir:
        os.makedirs(output_dir, mode=0o777, exist_ok=True)
        if output_dir.startswith(cwd):
            output_dir = output_dir.replace(cwd, f"/home/{cusername}/project")

        mb2_args.append("--output-dir")
        mb2_args.append(output_dir)

    if specfile:
        if specfile.startswith(cwd):
            specfile = specfile.replace(cwd, f"/home/{cusername}/project")
        mb2_args.append("--specfile")
        mb2_args.append(specfile)

    mb2_args.append("-t")
    mb2_args.append(f"SailfishOS-{release}-{arch}")

    mb2_build = ["build"]

    if enable_debug is True:
        mb2_build.append("--enable-debug")

    mb2_build.append(f"-j{len(os.sched_getaffinity(0))}")
    if source_dir:
        mb2_build.append(source_dir)

    call(docker_args + mb2_args + mb2_build)
    if check:
        call(docker_args + mb2_args + ["check"])


if __name__ == "__main__":
    main()
