import subprocess
import sys
from argparse import ArgumentParser
from itertools import accumulate


def main():
    argparser = ArgumentParser()
    argparser.add_argument("version")
    args = argparser.parse_args()

    version = args.version
    if not args.version.startswith("v"):
        print("version should start with `v`")
        sys.exit(1)

    parts = version[1:].split(".")
    vparts = [
        "v" + ".".join(vpart)
        for vpart in accumulate(parts, lambda acc, arg: acc + [arg], initial=[])
        if vpart
    ]

    for vpart in vparts:
        subprocess.check_call([
            "git", "tag",
            "-f",
            "-a", vpart,
            "-m", f"Release of {version}"])

    subprocess.check_call(["git", "push", "-f", "origin"] + vparts)


if __name__ == '__main__':
    main()
