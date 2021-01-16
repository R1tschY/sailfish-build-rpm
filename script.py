#!/usr/bin/env python3

import os

def set_output(id_: str, value: str):
    print("::set-output name={}::{}".format(id_, value))


def main():
    print(os.environ.items())



if __name__ == "__main__":
    main()