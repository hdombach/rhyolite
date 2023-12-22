#! /usr/bin/env python3

""""
# Rhyolite
A program for generating a mirror of the source code
with the markdown comments rendered
"""

import argparse
from renderer import render
import jinja2

""""
# get_args
Parses the args provided by the user.
"""
def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
            prog="rhyolite",
            description="Generates html documentation for a project")
    parser.add_argument("-i", "--in-files", required=True, type=str, action="extend", nargs="+")
    parser.add_argument("-o", "--out-dir", required=True)
    return parser.parse_args()

""""
# code_gen
- in_file_url
- build_dir_url
- template: jinja2 template used to generate the final file
"""
def code_gen(in_file_url: str, build_dir_url: str, template: jinja2.Template):
    in_file = open(in_file_url, "r")
    out_file = open("./" + build_dir_url + "/" + in_file_url + ".html", "w")
    rendered_html = render(in_file)

    print(template.render(formatted_code = rendered_html), file=out_file)

def main():
    args = get_args()
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("codegen"))
    html_template = env.get_template("index.html")

    for in_file_url in args.in_files:
        code_gen(in_file_url, args.out_dir, html_template)

if __name__ == "__main__":
    main()
