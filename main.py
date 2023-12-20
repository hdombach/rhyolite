#! /usr/bin/env python3

""""
# Rhyolite
A program for generating a mirror of the source code
with the markdown comments rendered
"""

import argparse
from renderer import render

""""
## get_args
Parses the args provided by the user.
"""
def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
            prog="rhyolite",
            description="Generates html documentation for a project")
    parser.add_argument("-i", "--in-files", required=True, type=str, action="extend", nargs="+")
    parser.add_argument("-o", "--out-dir", required=True)
    return parser.parse_args()

def main():
    args = get_args()

    for in_file_url in args.in_files:
        in_file = open(in_file_url, "r")
        out_file = open("./" + args.out_dir + "/" + in_file_url + ".html", "w")
        render(in_file, out_file)


if __name__ == "__main__":
    main()
